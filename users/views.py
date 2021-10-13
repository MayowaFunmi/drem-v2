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


'''
class UserSignUpView(View):
    form_class = CustomUserCreationForm
    template_name = 'users/user_signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)

            photo = request.FILES['photo']
            fs = FileSystemStorage()
            photo_filename = fs.save(photo.name, photo)

            context = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'middle_name': form.cleaned_data['middle_name'],
                'born_again': form.cleaned_data['born_again'],
                'church_name': form.cleaned_data['church_name'],
                'marital_status': form.cleaned_data['marital_status'],
                'address': form.cleaned_data['address'],
                'phone_number': form.cleaned_data['phone_number'],
                'date_of_birth': form.cleaned_data['date_of_birth'],
                'favourite_bible_verse': form.cleaned_data['favourite_bible_verse'],
                'about_me': form.cleaned_data['about_me'],
                'photo': fs.url(photo_filename),
            }
            return render(request, 'users/signup_success.html', context)

        else:
            print(form.errors)
        return render(request, self.template_name, {'form': form})

'''


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


'''
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'users/base.html')
            else:
                messages.error(request, 'Incorrect Username or Password')
                return render(request, 'users/login.html', {'form': form})

    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})
'''

# user Profile


@login_required
def user_profile(request):
    if User.objects.filter(username=request.user.username).exists():
        user = User.objects.get(username=request.user.username)
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


'''
def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)

        try:
            if form.is_valid():
                form.save(commit=True)

                return render(request, 'users/contact_us_success.html')
        except:
            return render(request, 'users/errors.html')

    else:
        form = ContactUsForm()

    return render(request, 'users/contact_us.html', {'form': form})

'''


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


'''
@login_required
def testimony(request):
    user = request.user
    if request.method == 'POST':
        form = TestimonyForm(request.POST)

        try:
            if form.is_valid():
                myform = form.save(commit=False)
                myform.user = request.user
                myform.save()

                context = {
                    'user': request.user.username,
                    'testimony': form.cleaned_data['testimony']
                }

                return render(request, 'users/testimony_detail.html', context)
        except:
            return render(request, 'users/errors.html')

    else:
        form = TestimonyForm()
    return render(request, 'users/testimony_form.html', {'form': form, 'user': user})

'''


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

'''
@login_required
def prayer_request(request):
    user = request.user
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST)

        try:
            if form.is_valid():
                myform = form.save(commit=False)
                myform.user = request.user
                myform.save()

                context = {
                    'user': request.user,
                    'prayer_points': form.cleaned_data['prayer_points']
                }

                return render(request, 'users/prayer_request_detail.html', context)
        except:
            return render(request, 'users/errors.html')

    else:
        form = TestimonyForm()
    return render(request, 'users/prayer_request_form.html', {'form': form, 'user': user})

'''


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
        reg_date = request.POST['date']
        photo = None
        date_of_birth = None
        try:
            date_of_birth = request.POST['date_of_birth']
            photo = request.FILES['photo']
        except:
            pass
        #picture = request.FILES['picture']
        favourite_bible_verse = request.POST['favourite_bible_verse']
        about_me = request.POST['about_me']

        user.first_name = first_name
        user.last_name = last_name
        user.middle_name = middle_name
        user.born_again = born_again
        user.church_name = church_name
        user.gender = gender
        user.marital_status = marital_status
        user.address = address
        user.phone_number = phone_number
        if date_of_birth:
            user.date_of_birth = user.date_of_birth
        else:
            user.date_of_birth = date_of_birth

        if photo:
            user.photo = user.photo
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

'''
@login_required
def update_user(request):
    obj = get_object_or_404(User, id=request.user.id)
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=obj)

    try:
        if form.is_valid():
            form.save(commit=True)
            user = User.objects.get(username=request.user.username)
            return render(request, 'users/user_profile.html', {'user': user})

    except:
        return render(request, 'users/errors.html')

    return render(request, 'users/update_user_profile.html', {'form': form})

'''


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