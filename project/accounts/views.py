from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Profile

# Create your views here.
def login(request):
    if request.method == 'POST':
        id = request.POST['id']
        password = request.POST['password']

        user = auth.authenticate(request, username=id, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('main:mainpage') # alert(?)
        else:
            return render(request, 'accounts/login.html')
        
    elif request.method == 'GET':
        return render(request, 'accounts/login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('main:mainpage')

def signup1(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm']:
            request.session['id'] = request.POST['id']
            request.session['password'] = request.POST['password']
            return redirect('accounts:signup2')
    return render(request, 'accounts/signup.html')

def signup2(request):
    if request.method == 'POST':
        request.session['nickName'] = request.POST['nickName']
        request.session['major'] = request.POST['major']
        request.session['weight'] = request.POST['weight']
        request.session['gender'] = request.POST['gender']
        request.session['agegroup'] = request.POST['agegroup']
        return redirect('accounts:signup3')
    return render(request, 'accounts/signup2.html')

def signup3(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.session['id'],
            password=request.session['password']
        )
        user.profile.nickName = request.session['nickName']
        user.profile.major = request.session['major']
        user.profile.weight = request.session['weight']
        user.profile.gender = int(request.session['gender'])
        user.profile.agegroup = request.session['agegroup']

        user.profile.goal = request.POST['goal']

        user.profile.save()

        auth.login(request, user)
        return redirect('/')
    return render(request, 'accounts/signup3.html')

def idpasswordfind(request):
    return render(request, 'accounts/idpasswordfind.html')

def idfindv1(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickName', '')
        password = request.POST.get('password', '')
        major = request.POST.get('major', '')

        try:
            user_profile = Profile.objects.get(nickName=nickname, major=major)
            user = user_profile.user
            if check_password(password, user.password):
                return render(request, 'accounts/idfindv2.html', {'username': user.username})
            else:
                messages.warning(request, "비밀번호가 일치하지 않습니다.")      # 추후 경고창 디자인 완료시 수정
                return render(request, 'accounts/idfindv2.html', {'error':'비밀번호가 일치하지 않습니다.'})
        except Profile.DoesNotExist:
            messages.warning(request, "일치하는 사용자를 찾을 수 없습니다.")    # 추후 경고창 디자인 완료시 수정
            return render(request, 'accounts/idfindv2.html', {'error':'일치하는 사용자를 찾을 수 없습니다.'})
    return render(request, 'accounts/idfindv1.html')

def idfindv2(request):
    return render(request, 'accounts/idfindv2.html')

def passwordfindv1(request):
    return render(request, 'accounts/passwordfindv1.html')

def passwordfindv2(request):
    return render(request, 'accounts/passwordfindv2.html')