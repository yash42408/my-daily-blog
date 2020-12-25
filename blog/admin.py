from django.contrib import admin
from .models import User,Post,Comment
# Register your models here.
def make_blogger(modelAdmin,request,queryset):
    queryset.update(is_blogger=True)
make_blogger.short_description="Mark Selected User as Blogger"
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','is_request','is_blogger']
    ordering=['username']
    actions = [make_blogger]

admin.site.register(User,UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
