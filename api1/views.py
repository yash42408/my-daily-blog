from django.shortcuts import render
from .serializers import PostSerializer,CommentSerializer
# Create your views here.
from rest_framework import viewsets
from blog.models import Post,Comment,User
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)
class GenerateTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
              
class PostViewSet(viewsets.ViewSet):
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        def list(self,request):
            posts = Post.objects.filter(status='Publish',is_archive=False).order_by('-id')[:3]
            seralizer1 = PostSerializer(posts,many=True)
            likes_post = Post.objects.filter(status='Publish',is_archive=False).annotate(like_count=Count('likes')).order_by('-like_count')[:3]
            seralizer2 = PostSerializer(likes_post,many=True)
            views_post = Post.objects.filter(status='Publish',is_archive=False).order_by('post_view').reverse()[:3]
            seralizer3 = PostSerializer(views_post,many=True)
            result = {
                'most_recent':seralizer1.data,
                'most_likes':seralizer2.data,
                'most_views':seralizer3.data,
            }
            return Response(result)
        
        def create(self,request):
            if request.user.is_blogger:
                data={
                    'title':request.data.get('title'),
                    'blogger':request.user.id,
                    'body':request.data.get('body'),
                }
                serializer = PostSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=HTTP_200_OK)
                return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':'You are not blogger please request for blogger'},status=HTTP_400_BAD_REQUEST)

        def retrieve(self,request,pk=None):
            post = get_object_or_404(Post,pk=pk)
            post.post_view+=1
            post.save()
            serializer = PostSerializer(post)
            return Response(data=serializer.data,status=HTTP_200_OK)

        def destroy(self,request,pk=None):
            post = get_object_or_404(Post,pk=pk)
            if request.user.id is post.blogger.id:
               post.delete()
               return Response({'mssg':'Post successfully delete'},status=HTTP_204_NO_CONTENT)
            else:
               return Response({'error':'you are not authorized for delete this post'})
        
        def update(self,request,pk=None):
            post = get_object_or_404(Post,pk=pk)
            if request.user.id is post.blogger.id:
                serializer = PostSerializer(post, data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save(blogger=request.user)
                    return Response(serializer.data)
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':'You are not Authorized to Update this post'}, status=HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ViewSet):
        permission_classes = [permissions.IsAuthenticated]

        def create(self,request):
            data ={
            'post':request.data.get('post_id'),
            'comment_content':request.data.get('comment_content'),
             }
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
               serializer.save(user=request.user)
               return Response(serializer.data,status=HTTP_200_OK)
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

        def destroy(self,request,pk=None):
            comment = get_object_or_404(Comment,pk=pk)
            post =  get_object_or_404(Post,pk=comment.post.id)
            if post.blogger.id is request.user.id:
               comment.delete()
               return Response({'mssg':'Comment Deleted successfully'},status=HTTP_200_OK)
            else:
               return Response({'error':'You are Not Authorized To Delete This Comment'},status=HTTP_400_BAD_REQUEST)


class MyPostViewSet(viewsets.ViewSet):
      permission_classes = [permissions.IsAuthenticated]

      def list(self ,request):
          if request.user.is_blogger:
             post = Post.objects.filter(is_archive=False,blogger=request.user.id)
             serializer = PostSerializer(post,many=True)
             return Response(data=serializer.data,status=HTTP_200_OK)
          else:
             return Response({'error':'You are Not Blogger please Request For blogger'},status=HTTP_400_BAD_REQUEST)


class MyPublishPostViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def list(self,request):
        if request.user.is_blogger:
            post = Post.objects.filter(is_archive=False,status='Publish',blogger=request.user.id)
            serializer = PostSerializer(post,many=True)
            return Response(data=serializer.data,status=HTTP_200_OK)
        else:
            return Response({'error':'You are Not Blogger Please Request For Blogger'},status=HTTP_400_BAD_REQUEST)

class MyUnpublishPostViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def list(self,request):
         if request.user.is_blogger:
            post = Post.objects.filter(is_archive=False,status='Unpublish',blogger=request.user.id)
            serializer = PostSerializer(post,many=True)
            return Response(data=serializer.data,status=HTTP_200_OK)
         else:
            return Response({'error':'You are Not Blogger Please Request For Blogger'},status=HTTP_400_BAD_REQUEST)


class MyArchivePostViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def list(self,request):
         if request.user.is_blogger:
            post = Post.objects.filter(is_archive=True,blogger=request.user.id)
            serializer = PostSerializer(post,many=True)
            return Response(data=serializer.data,status=HTTP_200_OK)
         else:
            return Response({'error':'You are Not Blogger Please Request For Blogger'},status=HTTP_400_BAD_REQUEST)

class LikeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def retrieve(self,request,pk=None):
        post = get_object_or_404(Post,pk=pk)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user.id)
            post.save()
        else:
            post.likes.add(request.user)
            post.save()
        total_likes=post.likes.count()
        return Response(data={'total_likes':total_likes},status=HTTP_200_OK)

class MakePublishViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def retrieve(self,request,pk=None):
        post = get_object_or_404(Post,pk=pk)
        if request.user.id is post.blogger.id: 
            post.status = "Publish"
            post.save()
            return Response({'mssg':'publish successfully'},status=HTTP_200_OK)
        else:
            return Response({'error':'You are Not Authorized To Perform action on this post'},status=HTTP_400_BAD_REQUEST)

class MakeUnpublishViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def retrieve(self,request,pk=None):
        post = get_object_or_404(Post,pk=pk)
        if request.user.id is post.blogger.id: 
            post.status = "Unpublish"
            post.save()
            return Response({'mssg':'Unpublish successfully'},status=HTTP_200_OK)
        else:
            return Response({'error':'You are Not Authorized To Perform action on this post'},status=HTTP_400_BAD_REQUEST)


class MakeArchiveViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def retrieve(self,request,pk=None):
        post = get_object_or_404(Post,pk=pk)
        if request.user.id is post.blogger.id: 
            post.is_archive = True
            post.save()
            return Response({'mssg':'Archive successfully'},status=HTTP_200_OK)
        else:
            return Response({'error':'You are Not Authorized To Perform action on this post'},status=HTTP_400_BAD_REQUEST)



class RecentPageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def list(self,request):
        offset = request.data.get('offset')
        limit = 3
        newoffset = offset+limit
        posts = Post.objects.filter(status='Publish',is_archive=False).order_by('-id')[offset:newoffset]
        totalpost=posts.count()
        totalData = Post.objects.filter(status='Publish',is_archive=False).count()   
        data ={}
        posts_json = PostSerializer(posts,many=True)
        return Response(data={
            'posts':posts_json.data,
            'totalResult':totalData,
            'newoffset':totalpost,
        })

class LikePageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def list(self,request):

        offset = request.data.get('offset')
        limit = 3
        newoffset = offset+limit
        posts = Post.objects.filter(status='Publish',is_archive=False).annotate(like_count=Count('likes')).order_by('-like_count')[offset:newoffset]
        totalpost=posts.count()
        totalData = Post.objects.filter(status='Publish',is_archive=False).annotate(like_count=Count('likes')).order_by('-like_count').count()   
        posts_json = PostSerializer(posts,many=True)
        return JsonResponse(data={
            'posts':posts_json.data,
            'totalResult':totalData,
            'newoffset':totalpost,
        })

class ViewPageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def list(self,request):
        offset = request.data.get('offset')
        limit = 3
        newoffset = offset+limit
        posts = Post.objects.filter(status='Publish',is_archive=False).order_by('post_view').reverse()[offset:newoffset]
        totalpost=posts.count()
        totalData = Post.objects.filter(status='Publish',is_archive=False).order_by('post_view').reverse().count()   
        posts_json = PostSerializer(posts,many=True)
        return JsonResponse(data={
            'posts':posts_json.data,
            'totalResult':totalData,
            'newoffset':totalpost,
        })

class MyPageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def list(self,request):
        offset = request.data.get('offset')
        limit = 3
        newoffset = offset+limit
        posts = Post.objects.filter(blogger_id=request.user.id,is_archive=False).order_by('-id')[offset:newoffset]
        totalpost=posts.count()
        totalData = Post.objects.filter(blogger_id=request.user.id,is_archive=False).order_by('-id').count()   
        posts_json = PostSerializer(posts,many=True)
        return JsonResponse(data={
            'posts':posts_json.data,
            'totalResult':totalData,
            'newoffset':totalpost,
        })

class BloggerRequestViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def list(self,request):
        if not request.user.is_request:
           user = get_object_or_404(User,id=request.user.id)
           user.is_request=True
           user.save()
           return Response({'mssg':'You are successfully request for blogger'},status=HTTP_200_OK)
        else:
            return Response({'error':'You are already request for blogger wait for approve request'},status=HTTP_400_BAD_REQUEST)


    

