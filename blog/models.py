from django.db import models
from django.urls import reverse
from django.conf import settings
import datetime
# Create your models here.
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

STATUS_CHOICE = (
    ('Publish', 'Publish'),
    ('Unpublish', 'Unpublish'),
)

# model for user customize
class User(AbstractUser):
    is_blogger = models.BooleanField(default=False)
    is_request = models.BooleanField(default=False)
    
#model for post 
class Post(models.Model):
    title = models.CharField(max_length = 255)
    title_tag = models.CharField(max_length = 255 , default="Greeting of the day!")
    blogger = models.ForeignKey(User,on_delete=models.CASCADE)
    body = RichTextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='Publish')
    post_view = models.IntegerField(default=0)
    
    post_date = models.DateField(auto_now_add=True)
    is_archive = models.BooleanField(default=False)
    
    likes = models.ManyToManyField(User,related_name='blog_posts',null=True)
    # count the total likes
    def total_likes(self):
        return self.likes.count()

    def __str__(self):

        return self.title 
    def get_absolute_url(self):
        
        return reverse("articledetail", kwargs={"pk": self.pk})

# model for comment
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=200)
    comment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment_content
        
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)