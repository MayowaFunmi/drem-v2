from django import forms
from .models import Questions

class QuizForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = "__all__"
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type Question Here...'}),
            'option1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Option 1 Here...'}),
            'option2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Option 2 Here...'}),
            'option3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Option 3 Here...'}),
            'option4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Option 4 Here...'}),
            'answer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Correct Answer Here...'}),
        }
