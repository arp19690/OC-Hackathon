from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

from oauth2client import client


@login_required(login_url=settings.LOGIN_URL)
def index(request):
    if request.user.is_authenticated:
        return redirect("/app/data-info")
    else:
        return redirect(reverse("login"))


def login(request):
    if request.user.is_authenticated:
        redirect_url = "/app/data-info"
        return redirect(redirect_url)
    else:
        if request.method != "POST":
            return render(request, 'marketingmanager/login.html')
        else:
            username = request.POST.get('username', False)
            password = request.POST.get('password', False)
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request,
                               'Oops, Incorrect username and/or password')
                return render(request, 'marketingmanager/login.html')
            if user.is_active:
                auth_login(request, user)

                # google auth here
                if "credentials" not in request.session:
                    google_auth(request)

                redirect_url = "/app/data-info"
                return redirect(redirect_url)


@login_required(login_url=settings.LOGIN_URL)
def logout(request):
    auth_logout(request)
    request.session.flush()
    return redirect(reverse('login'))


def google_auth(request):
    flow = client.flow_from_clientsecrets('client_secrets.json',
                                          scope='https://www.googleapis.com/auth/drive.metadata.readonly',
                                          redirect_uri=request.path,
                                          include_granted_scopes=True)
    if 'code' not in request.GET:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.GET.get('code')
        credentials = flow.step2_exchange(auth_code)
        request.session['credentials'] = credentials.to_json()
        return redirect("/")


# Error handlers mentioned below
def error503(request):
    data = {'error_code': 'Maintenance Mode ON',
            'error_message': "We are currently under maintenance. We will be back up soon."}
    return render(request, 'marketingmanager/503.html', data)


def error500(request):
    data = {'error_code': '500! Error',
            'error_message': "Unexpected error occurred. Our technology team is looking into it."}
    return render(request, 'marketingmanager/error.html', data)


def error404(request):
    data = {'error_code': '404! Error',
            'error_message': "Looks like you landed on the wrong planet."}
    return render(request, 'marketingmanager/error.html', data)


def error403(request):
    data = {'error_code': '403! Error',
            'error_message': "Please refresh the page and try again."}
    return render(request, 'marketingmanager/error.html', data)
