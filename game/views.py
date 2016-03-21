from django.shortcuts import render
from game.models import Player
from django.http import HttpResponseRedirect, HttpResponse
from django.core import exceptions
import zgame

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

def game(request):
	contextDict = {}
	try:
		u = request.user
	except exceptions.ObjectDoesNotExist:
		return HttpResponseRedirect('/accounts/register')
	g = zgame.Game()
	g.start_new_day()
	if not g.is_game_over():
        #kick off the day
		g.start_new_day()
        if not g.is_day_over() and not g.is_game_over():
			contextDict['options'] = g.turn_options
			contextDict['state'] = str(zgame.PlayerState())
			contextDict['gstate'] = g.game_state
			if request.method == 'POST':
				if 'MOVE' in request.POST:
					g.take_turn('MOVE')
				if 'ENTER' in request.POST:
					g.take_turn('ENTER')
				if 'WAIT' in request.POST:
					g.take_turn('WAIT')	
				if 'FIGHT' in request.POST:
					g.take_turn('FIGHT')
				if 'RUN' in request.POST:
					g.take_turn('RUN')
				if 'EXIT' in request.POST:
					g.take_turn('EXIT')	
				if 'SEARCH' in request.POST:
					g.take_turn('SEARCH')	
        # end the day
        g.end_day()
        #u.game = pickle(g)
	return render(request, 'game.html', contextDict)