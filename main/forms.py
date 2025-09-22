from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video', 'url']
        widgets = {
            'content' : forms.Textarea(attrs={
                'placeholder': "What do you want to talk about?",
                'rows': 3,
                'class': 'form-control'
            })
        }