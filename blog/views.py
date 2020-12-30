from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post,Comment,User
from .forms import PostForms
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db.models import Count
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
import logging

# Get an instance of a logger
logger = logging.getLogger('django')

# Create your views here.


# def home(request):
#     return render(request,'home.html')

# home view for user and blogger
class HomeView(View):

   def get(self,request,*args,**kwargs):
        recent_post = Post.objects.filter(status='Publish',is_archive=False).order_by('-id')
        paginator = Paginator(recent_post, 3) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        if recent_post.count()>3:
            is_data =True
        else:
            is_data=False
        page_obj = paginator.get_page(page_number)
        likes_post = Post.objects.filter(status='Publish',is_archive=False).annotate(like_count=Count('likes')).order_by('-like_count')[:3]
        paginator1 = Paginator(likes_post, 3) # Show 25 contacts per page.
        page_number1 = request.GET.get('page')
        page_obj1 = paginator1.get_page(page_number1)

        views_post = Post.objects.filter(status='Publish',is_archive=False).order_by('post_view').reverse()[:3]
        paginator2 = Paginator(views_post, 3) # Show 25 contacts per page.
        page_number2 = request.GET.get('page')
        page_obj2 = paginator2.get_page(page_number2)

        context ={
            'most_recent_post':page_obj,
            'most_likes_post':page_obj1,
            'most_views_post':page_obj2,
            'is_more_data':is_data,

        }
        return render(request,'home.html',context)
        
    
#show particular post in detail view
 
class ArticleDetailsView(DetailView):
    model = Post
    def get_object(self):
        obj = super().get_object()
        obj.post_view += 1
        obj.save()
        logger.info('ssssssssssss')
        return obj
    template_name = 'articleview.html'

# Add post view
class AddPostView(CreateView):
    model = Post
    form_class = PostForms
    template_name = 'addpost.html'

# add comment view for post
# class AddCommentView(LoginRequiredMixin,CreateView):
#     model = Comment
#     form_class = CommentForm
#     # fields = '__all__'
#     template_name ='postcomment.html'
#     def form_valid(self,form):
#         form.instance.post_id = self.kwargs['pk']
#         post = Post.objects.filter(id=form.instance.post_id)
#         # post.get().blogger.email
#         send_mail(
#              'Comment From %s' % (self.request.user),
#              'Comment on Your Post :%s' % (post.get().title),
#              'from@example.com',
#              [post.get().blogger.email],
#              fail_silently=False,
#          )
#         return super().form_valid(form)
#     success_url = reverse_lazy('home')

# function based view for add comment optimize

class AddCommentView(View):
       def post(self,request,*args,**kwargs):
                postid=request.POST.get('post_id')
                userid=request.POST.get('user_id')
                content=request.POST.get('content')
                post = Post.objects.get(id=postid)
                user = User.objects.get(id=userid)
                comment = Comment.objects.create(comment_content=content,post=post,user=user)
                comment.save()
                # send_mail(
                #       'Comment From %s' % (request.user),
                #       '''Dear %s,
                #          Greetings of the day!
                #          Comment on Your Post :%s
                #       '''% (post.blogger.username,post.title),
                #       'from@example.com',
                #       [post.blogger.email],
                #       fail_silently=False,
                #   )
                return JsonResponse({'data':'Comment added Successfully','date':comment.comment_date,'username':user.username,'status':200,'content':content})


# update post
class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForms
    template_name = 'updatepost.html'

# Delete post view

# class DeletePostView(DeleteView):
#     model = Post
#     template_name = 'deletepost.html'
#     success_url = reverse_lazy('home')


# def DeletePostView(request,pk):

#     post = get_object_or_404(Post,id=pk)
#     if request.method=="POST":
#         post.delete()
#         return HttpResponseRedirect(reverse('mypost',kwargs={'id': request.user.id}))
        
#     context ={
#         'post':post
#     }
#     return render(request,"deletepost.html",context)

class DeletePostView(View):
    def get(self,request):
        post = get_object_or_404(Post,pk=request.GET['post_id'])
        post.delete()
        new_posts = Post.objects.filter(is_archive=False)
        json_new_post = serializers.serialize('json',new_posts)
        return JsonResponse(data={
            'success':'success',
            'posts':json_new_post
        })

# show particular user post
class MyPostView(View):
      def get(self,request,id):
          post_list = Post.objects.filter(blogger_id=id,is_archive=False).order_by('-id')
          paginator = Paginator(post_list,3)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          if post_list.count()>3:
             is_data =True
          else:
             is_data=False
          return render(request, 'mypost.html', {'page_obj': page_obj,'is_more_data':is_data})
   
class LikeView(View):

   def get(self,request,*args,**kwargs):
       print(request.GET.get('post_id'))
       if request.user.is_anonymous:
           return JsonResponse({'data':'unsuccess'})
       else:
            post = get_object_or_404(Post,id=request.GET.get('post_id'))
            liked = False
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                post.save()
                liked=False
            else:
                post.likes.add(request.user)
                post.save()
                liked=True
            total_likes=post.likes.count()
            return JsonResponse({'data':total_likes})
    # return render(request,'home.html',{'liked':liked})

# remove comment view
class RemoveComment(View):
    def get(self,request,*args,**kwargs):
        comment = get_object_or_404(Comment,id=request.GET.get('comment_id'))
        comment.delete()
        return JsonResponse(data={
            'success':'success'
        })

# publish post view
class PublishPost(View):
    def get(self,request,*args,**kwargs):

        post = get_object_or_404(Post,pk=request.GET['post_id'])
        post.status='Publish'

        post.save()
        return JsonResponse(data={
            'status':post.status
        })
#unpublish post view 
class UnpublishPost(View):
    def get(self,request,*args,**kwargs):
        post = get_object_or_404(Post,pk=request.GET['post_id'])
        post.status='Unpublish'
        post.save()
        return JsonResponse(data={
            'status':post.status
        })

# user profile view
class UserProfile(View):
    def get(self,request):
        return render(request,'userprofile.html')

# approve request view
class ApproveRequest(View):
    def get(self,request,id):
        user = get_object_or_404(User,id=id)
        user.is_request=True
        user.save()
        return HttpResponseRedirect(reverse('userprofile'))

# mypublish post view
class MyPublishPostView(View):
    def get(self,request):
        post_list = Post.objects.filter(blogger_id=request.user.id).exclude(status='Unpublish')
        
        return render(request, 'mypublishpost.html', {'page_obj': post_list})
    # context = {
    #     'mypost':Post.objects.filter(blogger_id=id)
    # }
    # return render(request,'mypost.html',context)

# my unpublish post view

class MyUnpublishPostView(View):
    def get(self,request,*args,**kwargs):
        post_list = Post.objects.filter(blogger_id=request.user.id).exclude(status='Publish')
        paginator = Paginator(post_list, 3) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'myunpublishpost.html', {'page_obj': page_obj})

# archive post view
class ArchivePost(View):
    def get(self,request,id):
        post = get_object_or_404(Post,id=id)
        post.is_archive = True
        post.save()
        return HttpResponseRedirect(reverse('mypost',kwargs={'id': request.user.id}))


class MyArchivePost(View):
    def get(self,request,*args,**kwargs):
        post_list = Post.objects.filter(blogger_id=request.user.id).exclude(is_archive=False)
        paginator = Paginator(post_list, 3) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'myarchivepost.html', {'page_obj': page_obj})

class SearchByTitle(View):
    def post(self,request,*args,**kwargs):
        title = request.POST.get('title')
        post = Post.objects.filter(title__icontains=title)
        context = {
            'showpost':post
        }
        return render(request,'searchbytitle.html',context)

class RecentLoadPage(View):
    def get(self,request,*args,**kwargs):
        offset = int(request.GET['offset'])
        limit = 3
        newoffset = offset+limit
        posts = Post.objects.filter(status='Publish',is_archive=False).order_by('-id')[offset:newoffset]
        totalpost=posts.count()
        totalData = Post.objects.filter(status='Publish',is_archive=False).count()   
        users= User.objects.all().only('username')
        data ={}
        posts_json = serializers.serialize('json',posts)
        user_json = serializers.serialize('json',users)
        return JsonResponse(data={
            'posts':posts_json,
            'totalResult':totalData,
            'newoffset':totalpost,
            'users':user_json,


        })

class LikeLoadPage(View):

    def get(self,request,*args,**kwargs):

        offset = int(request.GET['offset'])
        limit = 3
        newoffset = offset+limit
        posts = Post.objects.filter(status='Publish',is_archive=False).annotate(like_count=Count('likes')).order_by('-like_count')[offset:newoffset]
        totalpost=posts.count()
        totalData = Post.objects.filter(status='Publish',is_archive=False).annotate(like_count=Count('likes')).order_by('-like_count').count()   
        users= User.objects.all().only('username')
        data ={}
        posts_json = serializers.serialize('json',posts)
        user_json = serializers.serialize('json',users)
        return JsonResponse(data={
            'posts':posts_json,
            'totalResult':totalData,
            'newoffset':totalpost,
            'users':user_json,
        })

class ViewLoadPage(View):
    def get(self,request,*args,**kwargs):
        offset = int(request.GET['offset'])
        limit = 3
        newoffset = offset+limit
        posts = Post.objects.filter(status='Publish',is_archive=False).order_by('post_view').reverse()[offset:newoffset]
        totalpost=posts.count()
        totalData = Post.objects.filter(status='Publish',is_archive=False).order_by('post_view').reverse().count()   
        users= User.objects.all().only('username')
        data ={}
        posts_json = serializers.serialize('json',posts)
        user_json = serializers.serialize('json',users)
        return JsonResponse(data={
            'posts':posts_json,
            'totalResult':totalData,
            'newoffset':totalpost,
            'users':user_json,
        })
    
class MyLoadPage(View):
    def get(self,request,*args,**kwargs):
        offset = int(request.GET['offset'])
        limit = 3
        newoffset = offset+limit
        posts = Post.objects.filter(blogger_id=request.user.id,is_archive=False).order_by('-id')[offset:newoffset]
        totalpost=posts.count()
        totalData = Post.objects.filter(blogger_id=request.user.id,is_archive=False).order_by('-id').count()   
        users= User.objects.all().only('username')
        data ={}
        posts_json = serializers.serialize('json',posts)
        user_json = serializers.serialize('json',users)
        return JsonResponse(data={
            'posts':posts_json,
            'totalResult':totalData,
            'newoffset':totalpost,
            'users':user_json,
        })