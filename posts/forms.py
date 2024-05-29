from django import forms
from .models import Post, PostComment

class postform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','text_content', 'file_content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']
