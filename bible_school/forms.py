from django import forms
from .models import Application

STATUS = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('In A Relationship', 'In A Relationship'),
        ('Widow', 'Widow'),
        ('Separated', 'Separated'),
        ('Divorced', 'Divorced'),
        ('Remarried', 'Remarried')
    ]

TITLE = [
        ('Pastor', 'Pastor'),
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Mr', 'Mr'),
        ('Chief', 'Chief'),
    ]

GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

AGE_BRACKET = [
        ('0', '0'),
        ('1 - 5', '1 - 5'),
        ('6 - 10', '6 - 10'),
        ('11 - 20', '11 - 20'),
        ('Above 20', 'Above 20'),
    ]


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ['user', ]
        widgets = {
            'title': forms.Select(choices=TITLE, attrs={'class': 'form-control'}),
            'course_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the course you are applying for.'}),
            'country_of_residence': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Your Country Of Residence'}),
            'state_or_city_1': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Your State of Residence'}),
            'residential_address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Your Residential Address'}),
            'country_of_origin': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Your Country Of Origin'}),
            'state_or_city_2': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Your State of Origin'}),
            'permanent_address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Your Permanent Address'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'place_of_birth': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Your Place Of Birth'}),
            'marital_status': forms.Select(choices=STATUS, attrs={'class': 'form-control'}),
            'gender': forms.Select(choices=GENDER, attrs={'class': 'form-control'}),

            'name_of_spouse': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Full Name Of Your Spouse'}),
            'number_of_children': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Number Of Children'}),
            'children_age_bracket': forms.Select(choices=AGE_BRACKET, attrs={'class': 'form-control', 'placeholder': 'Age Bracket of Children (if any)'}),
            'years_born_again': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'How long have you been a born-again Christian according to John 3:1-7?'}),
            'salvation_experience': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Share your salvation experience...'}),
            'spiritual_gifts': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Which spiritual gifts do you have according to 1 Corinthians 12 etc.?'}),
            'spiritual_fruit': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Fruits of the spirit manifesting in your life according to Galatians 5:22-23'}),
            'ministry_gift': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "State if you're currently a teacher/evangelist/prophet/pastor/any other one in your assembly"}),
            'discplined': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Have you ever been disciplined by your church for any act of immorality? Give reasons if yes."}),
            'ministry_experience': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Share your ministerial experience/any post held"}),
            'spiritual_mentor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Who is your spiritual mentor and Role Model?"}),
        }


# student application login code
class ApplicationCode(forms.Form):
    code = forms.CharField(widget=forms.PasswordInput, required=True)
