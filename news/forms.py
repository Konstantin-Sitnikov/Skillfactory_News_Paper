from django import forms
from .models import Post



class Publication(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["category", "title_news", "text_news"]

