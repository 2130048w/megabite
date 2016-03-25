from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Player(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(upload_to='images/profile_pictures', blank=True)
    games_played = models.IntegerField(default=0, blank=False)
    most_days_survived = models.IntegerField(default=0, blank=False)
    most_kills = models.IntegerField(default=0, blank=False)
    most_people = models.IntegerField(default=1, blank=False)
    current_game = models.SlugField(default="", blank=True)

    
    def __unicode__(self):
        return self.user.username

class Badge(models.Model):
     name = models.CharField(default="Badge 1", blank=False, max_length=128)
     description = models.CharField(default="Badge 1", blank=False, max_length=128)
     criteria = models.IntegerField(default=25, blank=False)
     badge_type = models.IntegerField(default=0, blank=False)
     level = models.IntegerField(default=1, blank=False)
     icon = models.ImageField(upload_to='images/badges', blank=True)

class achievementHandler(models.Model):
    user = models.ForeignKey(User)
    achievement = models.ForeignKey(Badge, related_name="userbadges")
    earned_at = models.DateTimeField(auto_now_add=True)
