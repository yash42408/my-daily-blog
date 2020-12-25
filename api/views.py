from rest_framework.views import APIView
from rest_framework.response import Response 
from django.contrib.auth import authenticate
from .serializers import (
    PostSerializer,UserSerializer,CommentSerializer
)
from blog.models import Post,User,Comment
from django.http import Http404,JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)
import json   

from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
# Create your views here.
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.core import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from django.db.models import Count


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
               
class PostView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    def get(self,request,*args,**kwargs):
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

    def post(self,request,*args,**kwargs):
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
    
    def put(self,request,pk,format=None):
        # if not request.data.get('blogger'):
            post = self.get_object(pk)
            if request.user.id is post.blogger.id:
                serializer = PostSerializer(post, data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save(blogger=request.user)
                    return Response(serializer.data)
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':'You are not Authorized to Update this post'}, status=HTTP_400_BAD_REQUEST)
        # else:
            # return Response({'error':'dont provide blogger id'},status=HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        post = self.get_object(pk)
        if request.user.id is post.blogger.id:
            post.delete()
            return Response({'mssg':'Post successfully delete'},status=HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'you are not authorized for delete this post'})

        
class PostDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self,request,pk,format=None):
        post = get_object_or_404(Post,pk=pk)
        post.post_view+=1
        post.save()
        comment = post.comments.all()
        serializer = PostSerializer(post)
    
        return Response(data=serializer.data,status=HTTP_200_OK)

class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def post(self,request,format=None):
        data ={
            'post':request.data.get('post_id'),
            'comment_content':request.data.get('comment_content'),
        }
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        comment = get_object_or_404(Comment,pk=pk)
        if comment.user.id is request.user.id:
            comment.delete()
            return Response({'mssg':'Comment Deleted successfully'},status=HTTP_200_OK)
        else:
            return Response({'error':'You are Not Authorized To Delete This Comment'},status=HTTP_400_BAD_REQUEST)

class MyPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
        if request.user.is_blogger:
            post = Post.objects.filter(is_archive=False,blogger=request.user.id)
            serializer = PostSerializer(post,many=True)
            return Response(data=serializer.data,status=HTTP_200_OK)
        else:
            return Response({'error':'You are Not Blogger please Request For blogger'},status=HTTP_400_BAD_REQUEST)

class MyPublishPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
        if request.user.is_blogger:
            post = Post.objects.filter(is_archive=False,status='Publish',blogger=request.user.id)
            serializer = PostSerializer(post,many=True)
            return Response(data=serializer.data,status=HTTP_200_OK)
        else:
            return Response({'error':'You are Not Blogger Please Request For Blogger'},status=HTTP_400_BAD_REQUEST)

class MyUnpublishPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
        if request.user.is_blogger:
            post = Post.objects.filter(is_archive=False,status='Unpublish',blogger=request.user.id)
            serializer = PostSerializer(post,many=True)
            return Response(data=serializer.data,status=HTTP_200_OK)
        else:
            return Response({'error':'You are Not Blogger Please Request For Blogger'},status=HTTP_400_BAD_REQUEST)

class MyArchivePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
        if request.user.is_blogger:
            post = Post.objects.filter(is_archive=True,blogger=request.user.id)
            serializer = PostSerializer(post,many=True)
            return Response(data=serializer.data,status=HTTP_200_OK)
        else:
            return Response({'error':'You are Not Blogger Please Request For Blogger'},status=HTTP_400_BAD_REQUEST)

class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,pk,format=None):
        post = get_object_or_404(Post,pk=pk)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user.id)
            post.save()
        else:
            post.likes.add(request.user)
            post.save()
        total_likes=post.likes.count()
        return Response(data={'total_likes':total_likes},status=HTTP_200_OK)

class MakePublishView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,format=None):
        post = get_object_or_404(Post,pk=request.data.get('post_id'))
        if request.user.id is post.blogger.id: 
            post.status = "Publish"
            post.save()
            return Response({'mssg':'publish successfully'},status=HTTP_200_OK)
        else:
            return Response({'error':'You are Not Authorized To Perform action on this post'},status=HTTP_400_BAD_REQUEST)

class MakeUnpublishView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,format=None):
        post = get_object_or_404(Post,pk=request.data.get('post_id'))
        if request.user.id is post.blogger.id: 
            post.status = "Unpublish"
            post.save()
            return Response({'mssg':'Unpublish successfully'},status=HTTP_200_OK)
        else:
            return Response({'error':'You are Not Authorized To Perform action on this post'},status=HTTP_400_BAD_REQUEST)

class RecentLoadPage(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self,request,format=None):
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

class LikeLoadPage(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self,request,format=None):

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

class ViewLoadPage(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self,request,format=None):
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

class MyLoadPage(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
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

class BloggerRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
        if not request.user.is_request:
           user = get_object_or_404(User,id=request.user.id)
           user.is_request=True
           user.save()
           return Response({'mssg':'You are successfully request for blogger'},status=HTTP_200_OK)
        else:
            return Response({'error':'You are already request for blogger wait for approve request'},status=HTTP_400_BAD_REQUEST)

class MakeArchivePost(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,pk,format=None):
        post = get_object_or_404(Post,id=pk)
        if not post.is_archive:   
           post.is_archive = True
           post.save()
           return Response({'mssg':'Post Archive Succesfully'},status=HTTP_200_OK)
        else:
           return Response({'error':'No Post available'},status=HTTP_404_NOT_FOUND)

