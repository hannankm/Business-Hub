# forms.py
from django import forms
from .models import Article, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         fields = ['title', 'file']

# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ['title', 'image']

# class VideoForm(forms.ModelForm):
#     class Meta:
#         model = Video
#         fields = ['title', 'video']

# class LinkForm(forms.ModelForm):
#     class Meta:
#         model = Link
#         fields = ['title', 'url']
