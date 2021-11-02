from django import forms
from .models import Awards


class AwardForm(forms.ModelForm):
    class Meta:
        model = Awards
        fields = ['title', 'name', 'award_title', 'award_image_1', 'award_image_2', 'brief_profile']
