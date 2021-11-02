from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Application(models.Model):
    # bio data
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
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
        ('Evangelist', 'Evangelist'),
        ('Deacon', 'Deacon'),
        ('Deaconess', 'Deaconess'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Mr', 'Mr'),
        ('Chief', 'Chief'),
    ]

    AGE_BRACKET = [
        ('0', '0'),
        ('1 - 5', '1 - 5'),
        ('6 - 10', '6 - 10'),
        ('11 - 20', '11 - 20'),
        ('Above 20', 'Above 20'),
    ]

    title = models.CharField(choices=TITLE, default=TITLE[0], help_text='Choose a title from the options above', max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_of_study = models.CharField(max_length=100)
    country_of_residence = models.CharField(max_length=50)
    state_or_city_1 = models.CharField(max_length=100)
    residential_address = models.CharField(max_length=1000)
    country_of_origin = models.CharField(max_length=50)
    state_or_city_2 = models.CharField(max_length=100)
    permanent_address = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=20)
    place_of_birth = models.CharField(max_length=20)
    marital_status = models.CharField(choices=STATUS, default=STATUS[0], help_text='What is your marital status?', max_length=50)
    gender = models.CharField(choices=GENDER, default=GENDER[0], help_text='Choose your gender', max_length=10)
    name_of_spouse = models.CharField(max_length=30, null=True, blank=True)
    number_of_children = models.CharField(max_length=30)
    children_age_bracket = models.CharField(choices=AGE_BRACKET, default=AGE_BRACKET[0], help_text='What is the age bracket of your children?', max_length=20)

    # spiritual matters

    years_born_again = models.CharField(max_length=10)
    salvation_experience = models.TextField()
    spirit_baptism = models.BooleanField(default=False, help_text='Have you receive the baptism of Holy Spirit according to Acts 2:4?')
    spiritual_gifts = models.CharField(max_length=100)
    spiritual_fruit = models.CharField(max_length=100)
    disability = models.BooleanField(default=False, help_text='Did you have any physical or emotional problem that might impair your studies in this institute?')
    ministry_gift = models.CharField(max_length=20)
    discplined = models.TextField(help_text='Have you ever been disciplined by your church for any act of immorality?  Give reasons if yes.')
    ministry_experience = models.TextField(help_text="Share your ministerial experience/any post held")
    spiritual_mentor = models.CharField(max_length=100)
    obedience = models.BooleanField(default=False, help_text='Are you ready to abide by the rules and regulation of S.B.I?')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'