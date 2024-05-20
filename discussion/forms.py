from django import forms
from .models import Question, Response

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
       
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']