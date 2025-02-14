from django import forms
from .models import Post


class Publication(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["autor_id", "category", "title_news", "text_news"]

