from django.shortcuts import render
from game import forms, models, zgame
from game.models import Player
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import pickle

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html', {})

@ensure_csrf_cookie    
def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and PlayerForm.
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.PlayerForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the Player instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'profile_picture' in request.FILES:
                profile.picture = request.FILES['profile_picture']

            # Now we save the UserProfile model instance.
            
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

			# Invalid form or forms - mistakes or something else?
			# Print problems to the terminal.
			# They'll also be shown to the user.
	return render(request, 'register.html', {'reg' : registered})
    else:
	return render(request, 'index.html', {})

@ensure_csrf_cookie
def myLogin(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
            if user:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    # If the account is valid and active, we can log the user in.
                    # We'll send the user back to the homepage.
                    login(request, user)
                else:
                    # An inactive account was used - no logging in!
                    return alert("Your account is disabled.")
            else:
                # Bad pw was provided. So we can't log the user in.
                print "Incorrect password: {0}, {1}".format(username, password)
                #TODO: Sleek error message
        else:
                # Bad un was provided. So we can't log the user in.
                print "Incorrect username: {0}, {1}".format(username, password)
                #TODO: Sleek error message
        return index(request)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'index.html', {})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('game/index')

def leaderboards(request):
    kill_rankings = Player.objects.order_by('-most_kills')[:20]
    survival_rankings = Player.objects.order_by('-most_days_survived')[:20]
    contextDict = {'kranks' : kill_rankings, 'sranks': survival_rankings}
    return render(request, 'leaderboards.html', contextDict)
	
def safehouse(request):
    try:
        u = request.user.player
    except exceptions.ObjectDoesNotExist:
        return HttpResponseRedirect('/accounts/register/')
    
    kill_stat = u.most_kills
    days_stat = u.most_days_survived
    games_stat = u.games_played
    name = u.user.username
    contextDict = {'kstat' : kill_stat, 'dstat' : days_stat, 'gstat' : games_stat, 'username': name}
    return render(request, 'safehouse.html', contextDict)

def edit_profile(request):
    u = request.user.player
    if request.method == 'POST':
		un = request.POST.get('username', False)
		if un != False:
			u.user.username = un
		up = request.POST.get('password', False)
		if up != False:
			u.password = up
		pp = request.POST.get('profile_picture', False)
		if pp != False:
			u.profile_picture = pp
    u.save()	
    return render( request, 'edit_profile.html', '' )	
    
def intro(request):
	return render(request, 'intro.html')

def game(request):
	contextDict = {}
	try:
		u = request.user.player
	except exceptions.ObjectDoesNotExist:
		return HttpResponseRedirect('/accounts/register')
	g = zgame.Game() #Make a new game
	cstatus = ''
	if u.current_game != "":
            myg = pickle.loads(u.current_game) #Otherwise load their game
            g.player_state = myg['state']
            g.update_state = myg['upstate']
            g.game_state = myg['gstate']
            g.update_time_left(zgame.LENGTH_OF_DAY - myg['tleft'])
            g.street = myg['street']
        else:
            g.start_new_day()
        if not g.is_game_over():
            if not g.is_day_over():
                if g.game_state == 'STREET':
                    contextDict['street'] = range(len(g.street.house_list)) #Once again more useful
                    contextDict['currentHouse'] = g.street.get_current_house()
                    contextDict['currentStreet'] = g.street
                if g.game_state == 'HOUSE':
                    contextDict['currentHouse'] = g.street.get_current_house()
                    contextDict['rooms'] = range(len(g.street.get_current_house().room_list)) #Length is more useful for us than the actual list
                    contextDict['currentRoom'] = g.street.get_current_house().get_current_room()
                if g.game_state == 'ZOMBIE':
                    contextDict['zombies'] = g.street.get_current_house().get_current_room().zombies
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
                        g.take_turn('SEARCH', g.street.get_current_house().get_current_room())
                    if g.game_state == 'STREET':
                        for i in range(len(g.street.house_list)):
                            if str(i) in request.POST:
                                cstatus += "Outside house "+str(i)
                                g.take_turn('MOVE', i)
                                break
                    if g.game_state == 'HOUSE':
                        for i in range(len(g.street.get_current_house().room_list)):
                            if str(i) in request.POST:
                                cstatus += "Searched room "+str(i)
                                g.take_turn('SEARCH', i)
                                break
            else:
                # end the day
                g.end_day()
                g.start_new_day()
        else:
            u.games_played += 1
            g = zgame.Game() #Make a new game for that user
            g.start_new_day()

        cstatus = ''
        
        if g.update_state.party<0:
            cstatus += "You lost: {0} people </br>".format(abs(g.update_state.party))

        if g.update_state.party>0:
            cstatus += "{0} more people have joined your party </br>".format(g.update_state.party)

        if g.update_state.ammo > 0:
            cstatus += "You found: {0} units of ammo</br>".format(g.update_state.ammo)

        if g.update_state.ammo < 0:
            cstatus += "You used: {0} units of ammo</br>".format(abs(g.update_state.ammo))

        if g.update_state.food > 0:
            cstatus += "You found: {0} units of food</br>".format(g.update_state.food)

        if g.update_state.food < 0:
            cstatus += "You used: {0} units of food</br>".format(abs(g.update_state.food))

        if g.update_state.kills > 0:
            cstatus += "You killed: {0} zombies</br>".format(g.update_state.kills)

        if g.update_state.days > 0:
            cstatus += "New Day: You survived another day!"

        contextDict['status'] = cstatus           
        contextDict['options'] = g.turn_options   
	contextDict['state'] = g.player_state
	contextDict['gstate'] = g.game_state
	contextDict['tleft'] = g.time_left

	myg = {}
	
        myg['street'] = g.street
        myg['state'] = g.player_state
        myg['upstate'] = g.update_state
        myg['gstate'] = g.game_state
        myg['tleft'] = g.time_left
        u.current_game = pickle.dumps(myg)
        if g.player_state.kills > u.most_kills:
            u.most_kills = g.player_state.kills
            viable_badges = models.Badge.objects.filter(criteria__lte = g.player_state.kills, badge_type=0)
            for i in viable_badges:
                newAchieve = achievementHandler(u, i)
                newAchieve.save()
        if g.player_state.days > u.most_days_survived:
            u.most_days_survived = g.player_state.days
            viable_badges = models.Badge.objects.filter(criteria__lte = g.player_state.days, badge_type=1)
            for i in viable_badges:
                newAchieve = achievementHandler(u, i)
                newAchieve.save()
        if g.player_state.party > u.most_people:
            u.most_people = g.player_state.party
            viable_badges = models.Badge.objects.filter(criteria__lte = g.player_state.party, badge_type=2)
            for i in viable_badges:
                newAchieve = achievementHandler(u, i)
                newAchieve.save()
        
        u.save()
	return render(request, 'game.html', contextDict)
