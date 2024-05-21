from django import forms
from .models import Group, GroupArticle, Announcement, Event
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'logo']



class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),           
            'end_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),        
              }


class GroupArticleForm(forms.ModelForm):
    class Meta:
        model = GroupArticle
        fields = ['title', 'content',  'type', 'invitation_note', 'authors']
        widgets = {
            'authors': forms.CheckboxSelectMultiple(),
            'type': forms.Select(choices=GroupArticle.TYPE_CHOICES)  # Use the choices from the model

        }

class GroupArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = GroupArticle
        fields = ['title', 'content', 'invitation_note', 'authors']
        widgets = {
            'authors': forms.CheckboxSelectMultiple(),
        }