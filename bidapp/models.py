from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    user_image = models.ImageField(upload_to='user_images')
    player_position = models.CharField(max_length=255, default='NA')
    owner = models.BooleanField(default=False)
    coowner = models.BooleanField(default=False)
    player_value = models.IntegerField(default=1)
    marquee = models.BooleanField(default=False)
    captain = models.BooleanField(default=False)
    vicecaptain = models.BooleanField(default=False)
    department = models.CharField(max_length=255)
    host = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    team = models.ForeignKey('team', related_name='team_players', null=True, blank=True, on_delete=models.SET_NULL)


    REQUIRED_FIELDS = ['firstname', 'lastname','email',
                       'year','user_image','department']


class team(models.Model):
    team_name = models.CharField(max_length=255, unique=True)
    captain = models.OneToOneField('User', related_name='captain_team', null=True, blank=True,on_delete=models.SET_NULL)
    owner = models.OneToOneField('User', related_name='owner_team', null=True, blank=True, on_delete=models.SET_NULL)
    coowner = models.OneToOneField('User', related_name='coowner_team', null=True, blank=True, on_delete=models.SET_NULL)
    vicecaptain = models.OneToOneField('User', related_name='vicecaptain_team', null=True, blank=True,on_delete=models.SET_NULL)
    marquee = models.OneToOneField('User', related_name='marquee_team', null=True, on_delete=models.SET_NULL)
    players = models.ManyToManyField('User', related_name='teams', blank=True)
    pot = models.IntegerField(default=100)
