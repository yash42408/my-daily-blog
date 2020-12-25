"""demo1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import (
    PostView,GenerateTokenView,PostDetailView,CommentView,MyPostView,MyPublishPostView,
    MyUnpublishPostView,MyArchivePostView,LikeView,MakePublishView,MakeUnpublishView,
    RecentLoadPage,LikeLoadPage,ViewLoadPage,MyLoadPage,BloggerRequest,MakeArchivePost

)
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login',GenerateTokenView.as_view(),name='login'),
    path('post',PostView.as_view(),name='post'),
    path('post/<int:pk>',PostView.as_view(),name='updatepost'),
    path('detailpost/<int:pk>',PostDetailView.as_view(),name='detailpost'),
    path('post/comment',CommentView.as_view(),name='comment'),
    path('post/comment/<int:pk>',CommentView.as_view()),
    path('post/mypost',MyPostView.as_view(),name='mypost'),
    path('post/my-publish-post',MyPublishPostView.as_view(),name='my-publish-post'),
    path('post/my-unpublish-post',MyUnpublishPostView.as_view(),name='my-unpublish-post'),
    path('post/my-archive-post',MyArchivePostView.as_view(),name='my-archive-post'),
    path('post/like-post/<int:pk>',LikeView.as_view(),name='like-post'),
    path('post/publish-post',MakePublishView.as_view(),name='publish-post'),
    path('post/unpublish-post',MakeUnpublishView.as_view(),name='unpublish-post'),
    path('post/most-recent-post',RecentLoadPage.as_view(),name='recent-load-page'),
    path('post/most-like-post',LikeLoadPage.as_view(),name='like-load-page'),
    path('post/most-view-post',ViewLoadPage.as_view(),name='view-load-page'),
    path('post/my-load-post',MyLoadPage.as_view(),name='my-load-page'),
    path('user/request-for-blogger',BloggerRequest.as_view(),name='request-for-blogger'),
    path('post/archive-post/<int:pk>',MakeArchivePost.as_view(),name='archive-post'),


]


