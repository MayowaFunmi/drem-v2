from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import ApplicationForm, ApplicationCode
from .models import Application


@login_required
def application_form(request):
    return render(request, 'bible_school/application_form.html')


@login_required
def apply_form(request):
    if request.method == 'POST':
        title = request.POST['title']
        course_of_study = request.POST['course_of_study']
        country_of_residence = request.POST['country_of_residence']
        state_or_city_1 = request.POST['state_or_city_1']
        residential_address = request.POST['residential_address']
        country_of_origin = request.POST['country_of_origin']
        state_or_city_2 = request.POST['state_or_city_2']
        permanent_address = request.POST['permanent_address']
        phone_number = request.POST['phone_number']
        place_of_birth = request.POST['place_of_birth']
        marital_status = request.POST['marital_status']
        gender = request.POST['gender']
        name_of_spouse = request.POST['name_of_spouse']
        number_of_children = request.POST['number_of_children']
        children_age_bracket = request.POST['children_age_bracket']

        
        years_born_again = request.POST['years_born_again']
        salvation_experience = request.POST['salvation_experience']
        spirit_baptism = request.POST['spirit_baptism']
        spiritual_gifts = request.POST['spiritual_gifts']
        ministry_gift = request.POST['ministry_gift']
        spiritual_fruit = request.POST['spiritual_fruit']
        disability = request.POST['disability']
        discplined = request.POST['discplined']
        obedience = request.POST['obedience']
        ministry_experience = request.POST['ministry_experience']
        spiritual_mentor = request.POST['spiritual_mentor']

        if obedience == "False":
            messages.error(request, "You must agree to adhere strictly to the rules and regulations of S.B.I. Choose "
                                    "Yes option and submit your application successfully.")
            return render(request, 'bible_school/apply_form.html')
        else:
            Application.objects.create(
                title=title, user=request.user, course_of_study=course_of_study,
                country_of_residence=country_of_residence, state_or_city_1=state_or_city_1,
                residential_address=residential_address, country_of_origin=country_of_origin,
                state_or_city_2=state_or_city_2, permanent_address=permanent_address, phone_number=phone_number,
                place_of_birth=place_of_birth, marital_status=marital_status, gender=gender,
                name_of_spouse=name_of_spouse, number_of_children=number_of_children,
                children_age_bracket=children_age_bracket, years_born_again=years_born_again,
                salvation_experience=salvation_experience, spirit_baptism=spirit_baptism, spiritual_gifts=spiritual_gifts,
                spiritual_fruit=spiritual_fruit, disability=disability, ministry_gift=ministry_gift,
                discplined=discplined, ministry_experience=ministry_experience, spiritual_mentor=spiritual_mentor,
                obedience=obedience
            )

            context = {
                'user': request.user,
                'title': title,
                'course_of_study': course_of_study,
                'country_of_residence': country_of_residence,
                'state_or_city_1': state_or_city_1,
                'residential_address': residential_address,
                'country_of_origin': country_of_origin,
                'state_or_city_2': state_or_city_2,
                'permanent_address': permanent_address,
                'phone_number': phone_number,
                'place_of_birth': place_of_birth,
                'marital_status': marital_status,
                'gender': gender,
                'name_of_spouse': name_of_spouse,
                'number_of_children': number_of_children,
                'children_age_bracket': children_age_bracket,
                'years_born_again': years_born_again,
                'salvation_experience': salvation_experience,
                'spirit_baptism': spirit_baptism,
                'spiritual_gifts': spiritual_gifts,
                'spiritual_fruit': spiritual_fruit,
                'ministry_gift': ministry_gift,
                'discplined': discplined,
                'ministry_experience': ministry_experience,
                'spiritual_mentor': spiritual_mentor,
                'obedience': obedience,
            }
            return render(request, 'bible_school/application_success.html', context)

    return render(request, 'bible_school/apply_form.html')


# bible school home page
def bible_school_home(request):
    return render(request, 'bible_school/sbi_home.html')


@login_required
def code_login(request):
    if request.method == 'POST':
        code = request.POST['login_code']
        if code == request.user.code_number:
            return redirect('school:instructions')
        else:
            messages.error(request, "Incorrect Login Code")
    return redirect('school:sbi_home')


def instructions(request):
    return render(request, 'bible_school/instructions.html')


@login_required
def application_form_save(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)

        if form.is_valid():
            myform = form.save(commit=False)
            myform.user = request.user

            if myform.obedience == False:
                messages.error(request, "You must agree to adhere strictly to the rules and regulations of S.B.I. Please check the box next to 'obedience' in the application form.")
                return render(request, 'bible_school/apply_form.html', {'form': form})
            else:
                myform.save()
            context = {
                'user': request.user,
                'title': form.cleaned_data['title'],
                'course_of_study': form.cleaned_data['course_of_study'],
                'country_of_residence': form.cleaned_data['country_of_residence'],
                'state_or_city_1': form.cleaned_data['state_or_city_1'],
                'residential_address': form.cleaned_data['residential_address'],
                'country_of_origin': form.cleaned_data['country_of_origin'],
                'state_or_city_2': form.cleaned_data['state_or_city_2'],
                'permanent_address': form.cleaned_data['permanent_address'],
                'phone_number': form.cleaned_data['phone_number'],
                'place_of_birth': form.cleaned_data['place_of_birth'],
                'marital_status': form.cleaned_data['marital_status'],
                'gender': form.cleaned_data['gender'],
                'name_of_spouse': form.cleaned_data['name_of_spouse'],
                'number_of_children': form.cleaned_data['number_of_children'],
                'children_age_bracket': form.cleaned_data['children_age_bracket'],
                'years_born_again': form.cleaned_data['years_born_again'],
                'salvation_experience': form.cleaned_data['salvation_experience'],
                'spirit_baptism': form.cleaned_data['spirit_baptism'],
                'spiritual_gifts': form.cleaned_data['spiritual_gifts'],
                'spiritual_fruit': form.cleaned_data['spiritual_fruit'],
                'ministry_gift': form.cleaned_data['ministry_gift'],
                'discplined': form.cleaned_data['discplined'],
                'ministry_experience': form.cleaned_data['ministry_experience'],
                'spiritual_mentor': form.cleaned_data['spiritual_mentor'],
                'obedience': form.cleaned_data['obedience'],
                #'created_date': form.cleaned_data['created_date'],
            }
            return render(request, 'bible_school/application_success.html', context)
    else:
        form = ApplicationForm()
    return render(request, 'bible_school/application_form.html', {'form': form})