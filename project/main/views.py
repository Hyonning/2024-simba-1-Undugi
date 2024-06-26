from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Building, Visit
from ranking.models import Ranking
from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def update_rankings():
    profiles = Profile.objects.all().order_by('-consumedCalorie')
    for index, profile in enumerate(profiles, start=1):
        ranking, created = Ranking.objects.get_or_create(profile=profile)
        ranking.total_calories_burned = profile.consumedCalorie
        ranking.rank = index
        ranking.save()
    
    
    # 랭킹 업데이트 로직
    #rankings = Ranking.objects.order_by('-total_calories_burned')
    #for index, ranking in enumerate(rankings, start=1):
    #    ranking.rank = index
    #    ranking.save()

def mainpage(request):
    return render(request, 'main/mainpage.html')

def map_select(request):
    if request.method == 'POST':    # 메인페이지에서 출발/도착 지점 저장
        start_building = request.POST['start_building']
        end_building = request.POST['end_building']
        # 출발지 or 도착지 미입력시 경고 문구
        if not start_building or not end_building:
            messages.warning(request, '출발지와 도착지를 입력해 주세요!')
            return render(request, 'main/mainpage.html')

        # 출발지와 도착지 저장
        if not start_building == end_building:
            new_path = Visit()
            new_path.start_building = start_building
            new_path.end_building = end_building
            new_path.user = request.user

            new_path.save()
            return redirect('main:map_page', id=new_path.id)
        else:
            messages.error(request, '출발지와 도착지를 다르게 입력해주세요!')
            return render(request, 'main/mainpage.html')
    elif request.method == 'GET':       # 지도페이지에서 출발/도착 지점 불러올 때
        return render(request, 'main/mainpage.html')
    return render(request, 'main/mainpage.html')

def map_page(request, id):
    new_path = Visit.objects.get(pk=id)
    return render(request, 'main/map.html', {'path':new_path})

def arrive(request):
    if request.method == 'POST':
        calorie = float(request.POST.get('calorie'))
        profile = request.user.profile
        request.user.profile.daily_consumedCalorie += calorie
        request.user.profile.consumedCalorie += calorie
        profile.save()

        update_rankings()

        user_ranking = None
        try:
            user_ranking = Ranking.objects.get(profile=profile)
        except Ranking.DoesNotExist:
            user_ranking = None


        return render(request, 'main/arrive.html', {
            'calorie': calorie,
            'daily_consumedCalorie': profile.daily_consumedCalorie,
            'remained_calorie': float(request.user.profile.goal) - float(request.user.profile.daily_consumedCalorie),
            'user_ranking':user_ranking
        })
    return render(request, 'main/arrive.html')