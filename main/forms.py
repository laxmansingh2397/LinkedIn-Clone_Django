from django import forms
from .models import Post, Experience
from .models import Profile
from django.contrib.auth import get_user_model


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


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ['headline', 'bio', 'location', 'profile_picture', 'background_image']

    def save(self, commit=True):
        profile = super().save(commit=False)
        # update related User fields if provided
        user = getattr(profile, 'user', None)
        if user:
            first = self.cleaned_data.get('first_name')
            last = self.cleaned_data.get('last_name')
            if first is not None:
                user.first_name = first
            if last is not None:
                user.last_name = last
            if commit:
                user.save()
        if commit:
            profile.save()
        return profile


class EducationForm(forms.ModelForm):
    class Meta:
        model = __import__('main.models', fromlist=['Education']).Education
        fields = ['school', 'degree', 'field_of_study', 'start_year', 'end_year']

    def clean_start_year(self):
        val = self.cleaned_data.get('start_year')
        if val and val < 1900:
            raise forms.ValidationError('Start year seems invalid')
        return val
