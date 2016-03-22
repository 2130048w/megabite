import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'megabite.settings')

import django
django.setup()

from django.contrib.auth.models import User
from game.models import Player, Badge 

def populate():
    
    add_badge('killer bronze','10 kills', 10, 0, 0, 'images/badges/bkill.png')
    add_badge('killer silver','25 kills', 25, 0, 1, 'images/badges/skill.png')
    add_badge('killer gold','50 kills', 50, 0, 2, 'images/badges/gkill.png')
    add_badge('survivor bronze','10 days', 10, 1, 0, 'images/badges/bday.png')
    add_badge('survivor silver','25 days', 25, 1, 1, 'images/badges/sday.png')
    add_badge('survivor gold','30 days', 30, 1, 2, 'images/badges/gday.png')
    add_badge('stamina bronze','5 games', 5, 2, 0, 'images/badges/bgame.png')
    add_badge('stamina silver','10 games', 10, 2, 1, 'images/badges/sgame.png')
    add_badge('stamina gold','20 games', 20, 2, 2, 'images/badges/ggame.png')
    
    jill_user = add_user("jill", email="jill@jill.co.uk", password="jill")
    bob_user = add_user("bob", email="bob@bob.co.uk", password="bob")
    jen_user = add_user("jen", email="jen@jen.co.uk", password="jen")
    
    jill_player = add_player(jill_user[0], 6, 37, 169, 6)
    
   
    bob_player = add_player(bob_user[0], 10, 12, 47, 22)
    
    
    jen_player = add_player(jen_user[0], 18, 28, 69, 17)
    

    
def add_player(u, games_played, most_days_survived, most_kills, most_people):
    p = Player.objects.get_or_create(user=u,games_played=games_played,most_days_survived=most_days_survived,
    most_kills=most_kills,most_people=most_people)
    return p
    
def add_user(username, email, password):
    u = User.objects.get_or_create(username=username, email=email, password=password)
    return u
    
def add_badge(name, description, criteria, badge_type, level, icon):
    b = Badge.objects.get_or_create(name=name,description=description,criteria=criteria,badge_type=badge_type,level=level,icon=icon)
    return b


if __name__ == '__main__':
    print "Starting Megabite population script..."
    populate()
