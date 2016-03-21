from django.shortcuts import render
from game import forms, models, zgame
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

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
