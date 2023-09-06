from django import forms
from .models import POST, Comment

class PostForm(forms.ModelForm):
    
    class Meta:
        model = POST
        fields = ('title', 'text',)
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)