# Generated by Django 3.2.8 on 2021-10-27 20:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Pastor', 'Pastor'), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Mr', 'Mr'), ('Chief', 'Chief')], default=('Pastor', 'Pastor'), help_text='Choose a title from the options above', max_length=20)),
                ('course_of_study', models.CharField(max_length=100)),
                ('country_of_residence', models.CharField(max_length=50)),
                ('state_or_city_1', models.CharField(max_length=100)),
                ('residential_address', models.CharField(max_length=1000)),
                ('country_of_origin', models.CharField(max_length=50)),
                ('state_or_city_2', models.CharField(max_length=100)),
                ('permanent_address', models.CharField(max_length=1000)),
                ('phone_number', models.CharField(max_length=20)),
                ('place_of_birth', models.CharField(max_length=20)),
                ('marital_status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('In A Relationship', 'In A Relationship'), ('Widow', 'Widow'), ('Separated', 'Separated'), ('Divorced', 'Divorced'), ('Remarried', 'Remarried')], default=('Single', 'Single'), help_text='What is your marital status?', max_length=50)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default=('Male', 'Male'), help_text='Choose your gender', max_length=10)),
                ('name_of_spouse', models.CharField(blank=True, max_length=30, null=True)),
                ('number_of_children', models.CharField(max_length=30)),
                ('children_age_bracket', models.CharField(choices=[('0', '0'), ('1 - 5', '1 - 5'), ('6 - 10', '6 - 10'), ('11 - 20', '11 - 20'), ('Above 20', 'Above 20')], default=('0', '0'), help_text='What is the age bracket of your children?', max_length=20)),
                ('years_born_again', models.CharField(max_length=10)),
                ('salvation_experience', models.TextField()),
                ('spirit_baptism', models.BooleanField(default=False, help_text='Have you receive the baptism of Holy Spirit according to Acts 2:4?')),
                ('spiritual_gifts', models.CharField(max_length=100)),
                ('spiritual_fruit', models.CharField(max_length=100)),
                ('disability', models.BooleanField(default=False, help_text='Did you have any physical or emotional problem that might impair your studies in this institute?')),
                ('ministry_gift', models.CharField(max_length=20)),
                ('discplined', models.TextField(help_text='Have you ever been disciplined by your church for any act of immorality?  Give reasons if yes.')),
                ('ministry_experience', models.TextField(help_text='Share your ministerial experience/any post held')),
                ('spiritual_mentor', models.CharField(max_length=100)),
                ('obedience', models.BooleanField(default=False, help_text='Are you ready to abide by the rules and regulation of S.B.I?')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
