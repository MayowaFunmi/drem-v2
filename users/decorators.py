from django.shortcuts import render


def unauthorised_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'users/not_allowed.html')
    return wrapper_func

'''
from django.http import HttpResponse


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # print('working here')
            group = None
            if request.user.group.exists():
                group = request.user.groups.all()[0].name
                print(group)

                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse('You are not authorised')

        return wrapper_func
    return decorator
'''