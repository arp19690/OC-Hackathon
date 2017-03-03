from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
import httplib2
from oauth2client import client
import os


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
                    return redirect(reverse("google-auth"))
                else:
                    redirect_url = "/app/data-info"
                    return redirect(redirect_url)


def google_auth(request):
    client_secrets_file_path = settings.BASE_DIR + "/helpers/client_secrets.json"
    flow = client.flow_from_clientsecrets(client_secrets_file_path,
                                          scope='https://www.googleapis.com/auth/analytics.readonly',
                                          redirect_uri=os.environ.get(
                                              "SITE_URL") + request.path)
    flow.params['access_type'] = 'offline'  # offline access
    # flow.params['include_granted_scopes'] = True  # incremental auth

    if 'code' not in request.GET:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.GET.get('code')
        credentials = flow.step2_exchange(auth_code)
        http_auth = credentials.authorize(httplib2.Http())
        request.session['credentials'] = credentials.to_json()
        # request.session['http_auth'] = http_auth
        return redirect("/")


@login_required(login_url=settings.LOGIN_URL)
def logout(request):
    auth_logout(request)
    request.session.flush()
    return redirect(reverse('login'))


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
