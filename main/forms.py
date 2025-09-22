from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content' : forms.Textarea(attrs={
                'placeholder': "What do you want to talk about?",
                'rows': 3,
                'class': 'form-control'
            })
        }