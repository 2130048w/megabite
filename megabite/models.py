from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Player(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True)
    games_played = models.IntegerField(default=0, blank=False)
    most_days_survived = models.IntegerField(default=0, blank=False)
    most_kills = models.IntegerField(default=0, blank=False)
    most_people = models.IntegerField(default=1, blank=False)
    current_game = models.StringField(default="", blank=True)
    
    def __unicode__(self):
        return self.user.username

class Badge(models.Model):
     name = models.StringField(default="Badge 1", blank=False)
     description = models.StringField(default="Badge 1", blank=False)
     criteria = models.IntegerField(default=25, blank=False)
     badge_type = models.IntegerField(default=0, blank=False)
     level = models.IntegerField(default=1, blank=False)
     icon = models.ImageField(upload_to='icon_images', blank=True)
     #Need acheivement handler to sort this out.
