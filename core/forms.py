from django import forms
from .models import MediaContent

class MediaContentForm(forms.ModelForm):
    class Meta:
        model = MediaContent
        fields = ['title', 'media_type', 'file', 'description']
