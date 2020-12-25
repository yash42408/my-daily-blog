from blog.models import User,Post
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'create rendom post'
    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        user = User.objects.create_user(username="admin",is_superuser=True,is_staff=True,is_request=True,is_blogger=True, email='admin@gmail.com', password='12345678')
        for i in range(total):
            Post.objects.create(title=get_random_string(),blogger=user,body=get_random_string())

