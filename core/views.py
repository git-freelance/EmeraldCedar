from django.shortcuts import redirect


def redirect_login(request):
    if request.user.is_admin():
        return redirect('/admin')
    else:
        return redirect('/dash')
