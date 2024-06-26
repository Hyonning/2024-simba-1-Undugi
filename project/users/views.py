from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserProfileForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib import messages
# Create your views here.
def mypage(request):
    user = request.user
    profileImage = user.profile.profileImage.url if user.profile.profileImage else '/project/static/images/defaultProfile.jpg'
    consumedCalorie = request.user.profile.consumedCalorie
    goal = request.user.profile.goal
    
    if goal is None:
        goal=0.0
    if consumedCalorie is None:
        consumedCalorie=0.0    
    
    remainCalorie = goal  - consumedCalorie
    context = {
        'profileImage': profileImage,
        'remainCalorie' : remainCalorie
    }
    return render(request, 'users/mypage.html', context)


def modify(request):
    return render(request, 'users/modify.html')

def pw_checking(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            request.session['password_checked'] = True
            return redirect('users:modifyv2')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
    return render(request, 'users/pw_checking.html')

def modifyv2(request):
    if not request.session.get('password_checked'):
        return redirect('users:pw_checking')
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if profile_form.is_valid():
            profile_form.save()
            update_session_auth_hash(request, request.user)  
            return redirect('users:mypage')
        else:
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        profile_form = UserProfileForm(instance=request.user.profile)
    
    context = {
        'profile_form': profile_form,
    }
    return render(request, 'users/modifyv2.html', context)