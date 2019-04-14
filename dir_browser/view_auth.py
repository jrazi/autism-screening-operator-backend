from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from dir_browser.forms import UserCreationForm,UserLoginForm
from dir_browser.models import CustomUser
from django.contrib.auth import login,logout
from AILab.settings import LOGIN_REDIRECT_URL

# Create your views here.

from django.template.loader import get_template
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        uf = UserCreationForm(request.POST, prefix='user')
        try:
            if uf.is_valid():
                uf.save()
                return HttpResponseRedirect("/")
        except:
            pass
        return HttpResponseRedirect("/auth/register")
    else:
        template = get_template('registration/register.html')
        uf = UserCreationForm(prefix='user')
        return HttpResponse(template.render(dict(userform=uf),request))

def login_req(request):
    if request.method == 'POST':
        uf = UserLoginForm(request.POST)
        username = uf.data.get('username')
        password = uf.data.get('password')
        try:
            user = CustomUser.objects.get(username=username)
            print(user)
            if user.check_password(password) :
                print("hi")
                login(request,user)
                return HttpResponseRedirect("/")
        except:
            pass
        return HttpResponseRedirect("/auth/login")
    else:
        template = get_template('registration/login.html')
        uf = UserLoginForm()
        return HttpResponse(template.render(dict(form=uf), request))


# you can eather use UserCreationForm in default auth forms or you can create custome form like in forms.UserForm but
# remember that you should get_clean_data("password") and setPassword for user because of hash