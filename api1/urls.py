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
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import (PostViewSet,GenerateTokenView,CommentViewSet,MyPostViewSet,
   MyPublishPostViewSet,MyUnpublishPostViewSet,MyArchivePostViewSet,LikeViewSet,
   MakePublishViewSet,MakeUnpublishViewSet,MakeArchiveViewSet,RecentPageViewSet,
   LikePageViewSet,ViewPageViewSet,BloggerRequestViewSet
)
router=DefaultRouter()
router.register('post',PostViewSet,basename='post')
router.register('comment',CommentViewSet,basename='comment')
router.register('mypost',MyPostViewSet,basename='mypost')
router.register('my-publish-post',MyPublishPostViewSet,basename='my-publish-post')
router.register('my-unpublish-post',MyUnpublishPostViewSet,basename='my-unpublish-post')
router.register('my-archive-post',MyArchivePostViewSet,basename='my-archive-post')
router.register('like',LikeViewSet,basename='like')
router.register('publish-post',MakePublishViewSet,basename='publish-post')
router.register('unpublish-post',MakeUnpublishViewSet,basename='unpublish-post')
router.register('archive-post',MakeArchiveViewSet,basename='archive-post')
router.register('recent-load-page',RecentPageViewSet,basename='recent-load-page')
router.register('like-load-page',LikePageViewSet,basename='like-load-page')
router.register('view-load-page',ViewPageViewSet,basename='view-load-page')
router.register('blogger-request',BloggerRequestViewSet,basename='blogger-request')


urlpatterns = [
    path('login',GenerateTokenView.as_view(),name='login'),
    path('',include(router.urls))
]
