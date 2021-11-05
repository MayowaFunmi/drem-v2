from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from .decorators import unauthorised_user
from .forms import CustomUserCreationForm, ContactUsForm, LoginForm, TestimonyForm, PrayerRequestForm, UserUpdateForm
from .models import ContactUs, Testimony, PrayerRequest

User = get_user_model()


def base(request):
    return render(request, 'users/base.html')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        middle_name = request.POST['middle_name']
        born_again = request.POST['born_again']
        church_name = request.POST['church_name']
        gender = request.POST['gender']
        marital_status = request.POST['marital_status']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        date_of_birth = request.POST['date_of_birth']
        photo = request.FILES['photo']
        favourite_bible_verse = request.POST['favourite_bible_verse']
        about_me = request.POST['about_me']
        password = request.POST['password']
        password2 = request.POST['password2']

        # validate username
        check_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root', 'email',
                       'user', 'join', 'sql', 'static', 'python', 'delete', 'sex', 'sexy']

        if username in check_users:
            messages.error(request, 'Your Username, ' + username + ', Is Not Acceptable. Please Use Another Username')
            return render(request, 'users/user_signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Your Username, ' + username + ', Already Exists. Please Try Another Username')
            return render(request, 'users/user_signup.html')

        # validate email
        email = email.strip().lower()
        if ("@" not in email) or (email[-4:] not in ".com.org.edu.gov.net"):
            messages.error(request, 'Your Email, ' + email + ', Is Invalid!!!')
            return render(request, 'users/user_signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Your Email, ' + email + ', Already Exists. Please Try Another Email')
            return render(request, 'users/user_signup.html')

        # validate password
        if password != password2:
            messages.error(request, "Your Passwords Don't match")
            return render(request, 'users/user_signup.html')

        User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name,
                                 middle_name=middle_name, born_again=born_again, church_name=church_name,
                                 marital_status=marital_status, address=address, phone_number=phone_number,
                                 date_of_birth=date_of_birth, photo=photo, favourite_bible_verse=favourite_bible_verse,
                                 about_me=about_me, gender=gender)
        user = User.objects.get(username=username)
        context = {
            'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'middle_name': middle_name,
            'born_again': born_again, 'church_name': church_name, 'marital_status': marital_status, 'address': address,
            'phone_number': phone_number, 'date_of_birth': date_of_birth, 'photo': user.photo, 'favourite_bible_verse': favourite_bible_verse,
            'about_me': about_me, 'gender': gender
        }
        return render(request, 'users/signup_success.html', context)
    return render(request, 'users/user_signup.html')


# login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'This Username, ' + username + ', Does Not Exist...')
            return render(request, 'users/login.html')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('base')
    return render(request, 'users/login.html')


# user Profile
def user_profile(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'users/user_profile.html', {'user': user})


# logout view
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# view for contact form
def contact_us(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        message = request.POST['message']

        ContactUs.objects.create(
            full_name=full_name,
            email=email,
            address=address,
            phone_number=phone_number,
            message=message
        )
        return render(request, 'users/contact_us_success.html')
    return render(request, 'users/contact_us.html')


# testimony form
@login_required
def testimony(request):
    user = request.user
    if request.method == 'POST':
        my_testimony = request.POST['my_testimony']

        Testimony.objects.create(user=request.user, testimony=my_testimony)
        context = {
            'my_testimony': my_testimony
        }
        return render(request, 'users/testimony_detail.html', context)
    return render(request, 'users/testimony_form.html', {'user': user})


# prayer request form
@login_required
def prayer_request(request):
    user = request.user
    if request.method == 'POST':
        prayer = request.POST['prayer']

        PrayerRequest.objects.create(user=request.user, prayer_points=prayer)
        context = {
            'prayer': prayer
        }
        return render(request, 'users/prayer_request_detail.html', context)
    return render(request, 'users/prayer_request_form.html', {'user': user})


# update user profile
@login_required
def update_user(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        middle_name = request.POST['middle_name']
        born_again = request.POST['born_again']
        church_name = request.POST['church_name']
        gender = request.POST['gender']
        marital_status = request.POST['marital_status']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        reg_date = request.POST['date_of_birth']
        updated_date = request.POST['dob']
        favourite_bible_verse = request.POST['favourite_bible_verse']
        about_me = request.POST['about_me']
        y = user.photo
        photo = None

        try:
            if request.FILES['photo']:
                photo = request.FILES['photo']
        except:
            photo = None

        # change date format to yyyy-mm-dd
        x = user.date_of_birth
        reg = x.strftime('%Y-%m-%d')

        user.first_name = first_name
        user.last_name = last_name
        user.middle_name = middle_name
        user.born_again = born_again
        user.church_name = church_name
        user.gender = gender
        user.marital_status = marital_status
        user.address = address
        user.phone_number = phone_number

        if not updated_date:
            user.date_of_birth = reg
        elif reg_date == updated_date:
            user.date_of_birth = reg
        else:
            user.date_of_birth = updated_date

        if photo is None:
            user.photo = y
        else:
            user.photo = photo

        user.favourite_bible_verse = favourite_bible_verse
        user.about_me = about_me
        user.save()
        return redirect('users:user_profile')
    context = {
        'user': user
    }
    return render(request, 'users/update_user_profile.html', context)


def about_us(request):
    return render(request, 'users/about_us.html')


def convener(request):
    return render(request, 'users/convener.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your Password Has Been Changed Successfully')
            return redirect('users:logout')
        else:
            messages.error(request, 'Error while changing your password. Please try again')
            return redirect('users:change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})