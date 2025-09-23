from django import forms
from .models import Post, Experience


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video', 'url']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': "What do you want to talk about?",
                'rows': 3,
                'class': 'form-control'
            })
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "employment_type",
            "company",
            "start_date",
            "end_date",
            "location",
            "location_type",
            "description",
            "profile_headline",
            "where_found",
            "skills",
            "media",
        ]

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
            "skills": forms.TextInput(attrs={"placeholder": "Comma-separated skills"}),
        }