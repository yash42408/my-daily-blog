from django import forms
from .models import Post,Comment
from ckeditor.widgets import CKEditorWidget


class PostForms(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title','title_tag','blogger','body','status')

        widgets = {

            'title':forms.TextInput(attrs={'class':'form-control'}),
            'title_tag':forms.TextInput(attrs={'class':'form-control'}),
            'blogger':forms.TextInput(attrs={'class':'form-control','value':'','id':'blogger','type':'hidden'}),
            'body':forms.Textarea(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),

            

        }

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('comment_content','user')

#         widgets ={
#             'comment_content':forms.TextInput(attrs={'class':'form-control'}),
#             'user':forms.TextInput(attrs={'class':'form-control','value':'','id':'user','type':'hidden'}),


#         }
