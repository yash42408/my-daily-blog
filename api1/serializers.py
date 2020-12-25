from rest_framework import serializers
from blog.models import User,Post,Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','post','comment_content']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

class PostSerializer(serializers.ModelSerializer):
    # comments = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='comment_content'
    #  )

    comments = CommentSerializer(many=True, read_only=True)
    blogger = UserSerializer()
    class Meta:
        model = Post
        fields = ['id','title','title_tag','body','is_archive','status','post_date','blogger','likes','post_view','comments']


