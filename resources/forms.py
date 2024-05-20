# forms.py
from django import forms
from .models import Article, Comment, Media, Document
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

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'media_type', 'file']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']