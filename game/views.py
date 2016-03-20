from django.shortcuts import render
from game.models import Player

def index(request):
    return render(request, 'index.html', {})
    
def register(request):
    return render(request, 'register.html', {})
	
def leaderboards(request):
    kill_rankings = Player.objects.order_by('-most_kills')[:20]
    survival_rankings = Player.objects.order_by('-most_days_survived')[:20]
    contextDict = {'kranks' : kill_rankings, 'sranks': survival_rankings}
    return render(request, 'leaderboards.html', contextDict)
    
def intro(request):
	return render(request, 'intro.html')