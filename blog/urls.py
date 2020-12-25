from django.contrib import admin
from django.urls import path,include
from .views import HomeView,ArticleDetailsView,MyLoadPage,ViewLoadPage,LikeLoadPage,RecentLoadPage,PublishPost,ArchivePost,SearchByTitle,MyArchivePost,MyUnpublishPostView,MyPublishPostView,ApproveRequest,UserProfile,UnpublishPost,RemoveComment,AddPostView,UpdatePostView,AddCommentView,LikeView,MyPostView,DeletePostView
urlpatterns = [
    path('home/',HomeView.as_view(),name='home'),
    path('post/<int:pk>',ArticleDetailsView.as_view(),name = 'articledetail'),
    path('addpost/',AddPostView.as_view(),name='addpost'),
    path('updatepost/edit/<int:pk>',UpdatePostView.as_view(),name='update_post'),
    path('mypost/<int:id>',MyPostView.as_view(),name='mypost'),
    path('deletepost/delete',DeletePostView.as_view(),name='delete_post'),
    path('like_post/',LikeView.as_view(),name='like_post'),
    path('post/comment/addcomment',AddCommentView.as_view(),name='addcomment'),
    path('post/comment/remove/',RemoveComment.as_view(),name='removecomment'),
    path('post/mypost/publish',PublishPost.as_view(),name='publishpost'),
    path('post/mypost/unpublish',UnpublishPost.as_view(),name='unpublish-post'),
    path('user/userprofile',UserProfile.as_view(),name='userprofile'),
    path('user/userprfile/request-for-blogger/<int:id>',ApproveRequest.as_view(),name='approve-request'),
    path('post/mypost/mypublishpost',MyPublishPostView.as_view(),name='my-publish-post'),
    path('post/mypost/myunpublishpost',MyUnpublishPostView.as_view(),name='my-unpublish-post'),
    path('post/mypost/archivepost/<int:id>',ArchivePost.as_view(),name='archive-post'),
    path('post/mypost/myarchivepost',MyArchivePost.as_view(),name='my-archive-post'),
    path('home/post/search_by_title',SearchByTitle.as_view(),name='search-by-title'),
    path('home/recentloadpost',RecentLoadPage.as_view(),name='recentloadpage'),
    path('home/likeloadpost',LikeLoadPage.as_view(),name='likeloadpage'),
    path('home/viewloadpost',ViewLoadPage.as_view(),name='viewloadpage'),    
    path('home/myloadpost',MyLoadPage.as_view(),name='my-load-page'),    

]
