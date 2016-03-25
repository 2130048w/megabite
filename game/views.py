from django.shortcuts import render
from game import forms, models, zgame
from game.models import Player
from game.forms import UserForm, PlayerForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
import pickle, json, random

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html', {})
    
def register(request):
    registered = False

    if request.is_ajax() and request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and PlayerForm.
        user_form = forms.UserForm(data=request.POST)
        player_form = forms.PlayerForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and player_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the Player instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            player = player_form.save(commit=False)
            player.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'profile_picture' in request.FILES:
                player.profile_picture = request.FILES['profile_picture']

            # Now we save the UserProfile model instance.
            
            player.save()

            # Update our variable to tell the template registration was successful.
            registered = True

			# Invalid form or forms - mistakes or something else?
			# Print problems to the terminal.
			# They'll also be shown to the user.
        return HttpResponse(json.dumps({'reg' : registered, 'errors' : user_form.errors}), content_type="application/json")
    else:
	return render(request, '/game/index/', {})

def myLogin(request):
    if request.is_ajax() and request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form, passed through AJAX post.
        username = request.POST.get('username')
        password = request.POST.get('password')

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
                    return HttpResponse(json.dumps({ 'error' : "Your account is disabled." }), content_type="application/json")
            else:
                # Bad pw was provided. So we can't log the user in.
                return HttpResponse(json.dumps({ 'password_error' : "Incorrect password" }), content_type="application/json")
        else:
            # Bad un was provided. So we can't log the user in.
            return HttpResponse(json.dumps({ 'username_error' : "Incorrect username" }), content_type="application/json")
        
        return HttpResponse(json.dumps({}), content_type="application/json")

    #Not a POST request so we need to redirect
    else:
        return render(request, '/game/', {})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/game/')

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
    partysize = u.most_people
    photo = u.profile_picture
    badges = models.achievementHandler.objects.filter(user=u.user)
    contextDict = {'kstat' : kill_stat, 'dstat' : days_stat, 'gstat' : games_stat, 'username': name, 'pstat':partysize, 'badges':badges, 'photo':photo}
    return render(request, 'safehouse.html', contextDict)

@login_required
def edit_profile(request):
    u = request.user
    edit = False
    if request.is_ajax() and request.method == 'POST':
        old_password = request.POST.get('old_password')
        user = authenticate(username=u.username, password=old_password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            user_form = UserForm(data=request.POST, instance=u)
            if user_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.player = u.player
                update_session_auth_hash(request, user)
                if 'profile_picture' in request.FILES:
                    user.player.profile_picture = request.FILES['profile_picture']
                user.save()
                edit = True
            return HttpResponse(json.dumps({'edit' : edit, 'errors' : user_form.errors }), content_type="application/json")
        else:
            return HttpResponse(json.dumps({ 'password_error' : "Incorrect password" }), content_type="application/json")
    else:
        return render(request, '/game/', {})
    
    
def intro(request):
	return render(request, 'intro.html')
    
@login_required
def game(request):
	contextDict = {'newday' : False, 'gameover' : False} #Assigned false by default
	roomData = {} # Need to assign this so I can check it later
	g = zgame.Game() #Make a new game
	cstatus = ''
	trn = ''
        u = request.user.player
        if request.is_ajax() and request.method == 'POST':
            trn = request.POST.get('the_post')
	if u.current_game != "":
            myg = pickle.loads(u.current_game) #Otherwise load their game
            g.player_state = myg['state']
            g.update_state = myg['upstate']
            g.game_state = myg['gstate']
            g.update_time_left(zgame.LENGTH_OF_DAY - myg['tleft'])
            g.street = myg['street']
        else:
            u.games_played += 1 #Remove if you only want to increment the counter on them finishing a game
            g.start_new_day()
        if g.is_game_over():
            if trn == 'Play Again':
                u.games_played += 1
                viable_badges = models.Badge.objects.filter(badge_type=2, criteria__lte = u.games_played)
                for i in viable_badges:
                    newAchieve = models.achievementHandler.objects.get_or_create(user=u.user, achievement=i)
                    if newAchieve[1] == True:
                        my_dict = {'achieve' : True, 'badge' : i.name, 'desc' : i.description, 'icon' : i.icon.url}
                g = zgame.Game() #Make a new game for that user
                g.start_new_day()
            else:
                #Game over man... game over.
                contextDict['gameover'] = True
        else:
            if g.is_day_over():
                if trn == 'Continue':
                    # end the day
                    g.end_day()
                    g.start_new_day()
                    #if we wanted to let the player carry on from where they were - some sort of street progression system:
                    #g.game_state = myg['gstate']
                    cstatus +='You wake up on an unfamiliar street, groaning can be heard in the distance</br>'
                else:
                    contextDict['newday'] = True
        if contextDict['gameover'] == False and contextDict['newday'] == False:
            if trn == 'MOVE':
                g.take_turn('MOVE')
            elif trn == 'ENTER':
                g.take_turn('ENTER')
                cstatus += 'You enter the house'
            elif trn == 'WAIT':
                g.take_turn('WAIT')
                cstatus += 'You wait for a bit..'
            elif trn =='FIGHT':
                g.take_turn('FIGHT')
                cstatus += 'You attack the zombies'
            elif trn == 'RUN':
                g.take_turn('RUN')
                cstatus += 'You run out to the street!'
            elif trn == 'EXIT':
                g.take_turn('EXIT')
                cstatus += 'You exit the house'
            elif trn == 'SEARCH':
                g.take_turn('SEARCH', g.street.get_current_house().get_current_room())
                
            if g.game_state == 'STREET':
                for i in range(len(g.street.house_list)): 
                    if str(i) == trn:
                        cstatus += "You moved outside house: "+str(i)+"</br>"
                        g.take_turn('MOVE', i)
                houseList = {}
                for i in range(len(g.street.house_list)): #This for loop puts the houses in a dictionary assigned images according to their size, so it's consistent on page reloads
                    if len(g.street.house_list[i].room_list) >= 12:
                        houseList[str(i)] = '2'
                    elif len(g.street.house_list[i].room_list) >= 9:
                        houseList[str(i)] = '1'
                    else:
                        houseList[str(i)] = '0' #Amazingly strings are more useful for us. Saves ugly js type conversion
                contextDict['streetData'] = houseList
                contextDict['currentStreet'] = str(g.street)
                
            if g.game_state == 'HOUSE': 
                for i in range(len(g.street.get_current_house().room_list)):
                    if str(i) == trn:
                        cstatus += "You searched room: "+str(i)+"</br>"
                        g.take_turn('SEARCH', i)
                contextDict['currentHouse'] = str(g.street.get_current_house())
                if myg['mappedHouse'] == True: #If we're in the same house we don't need to generate a new mapping of images!
                    roomData = myg['roomData'] #We can load the old mapping from the database
                else:
                    for i in range(len(g.street.get_current_house().room_list)): #This for loop puts the rooms assigned with a random image into the database - All these complex datatypes just for consistent images!
                        roomData[str(i)] = str(random.randint(0, 12)) #better as strings again
                contextDict['roomData'] = roomData #Pass to the contextDict
                
            if g.game_state == 'ZOMBIE':
                contextDict['zombies'] = g.street.get_current_house().get_current_room().zombies
                roomData = myg['roomData'] #We can load the old mapping from the database since zombies MUST be in a house
            contextDict['options'] = zgame.ACTIONS[g.game_state]
            contextDict['state'] = str(g.player_state)
            contextDict['gstate'] = g.game_state
            contextDict['tleft'] = g.time_left
            
        #Recheck the state after moving
        if g.is_game_over():
            contextDict = {'gameover' : True}
        elif g.is_day_over():
            contextDict = {'newday' : True}
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

	myg = {}
	if roomData != {}:
            myg['roomData'] = roomData #Save it to the database
        if g.game_state == 'HOUSE' or g.game_state == 'ZOMBIE': #We only want to map new houses
            myg['mappedHouse'] = True #We mapped this house
        else:
            myg['mappedHouse'] = False #Cowboy fix - Won't remember a house after you exit / run.
        myg['street'] = g.street
        myg['state'] = g.player_state
        myg['upstate'] = g.update_state
        myg['gstate'] = g.game_state
        myg['tleft'] = g.time_left
        my_dict = {'achieve' : False} 
        u.current_game = pickle.dumps(myg)
        if g.player_state.kills > u.most_kills:
            u.most_kills = g.player_state.kills
            viable_badges = models.Badge.objects.filter(badge_type=0, criteria__lte = g.player_state.kills)
            for i in viable_badges:
                newAchieve = models.achievementHandler.objects.get_or_create(user=u.user, achievement=i)
                if newAchieve[1] == True:
                    my_dict = {'achieve' : True, 'badge' : i.name, 'desc' : i.description, 'icon' : i.icon.url}
        if g.player_state.days > u.most_days_survived:
            u.most_days_survived = g.player_state.days
            viable_badges = models.Badge.objects.filter(badge_type=1, criteria__lte = g.player_state.days)
            for i in viable_badges:
                newAchieve = models.achievementHandler.objects.get_or_create(user=u.user, achievement=i)
                if newAchieve[1] == True:
                    my_dict = {'achieve' : True, 'badge' : i.name, 'desc' : i.description, 'icon' : i.icon.url}
        if g.player_state.party > u.most_people:
            u.most_people = g.player_state.party
        
        u.save()
        contextDict['adata'] = my_dict
        if request.is_ajax() and request.method == 'POST':
            return HttpResponse(json.dumps(contextDict), content_type="application/json")
	return render(request, 'game.html', contextDict) #To handle html requests
