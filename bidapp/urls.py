from django.urls import path, include
from .views import (signupView,
                    getuserbyemailView , getallplayersView,
                    getteamView,getallteamView,getnextplayerView,TransferView,getPlayerByID,records)

urlpatterns = [
    path('signup',signupView.as_view()),
    path('getuserbyemail',getuserbyemailView.as_view()),
    path('getallplayers',getallplayersView.as_view()),
    path('getteam',getteamView.as_view()),
    path('getallteam',getallteamView.as_view()),
    path('getnextplayer',getnextplayerView.as_view()),
    path('transferplayer',TransferView.as_view()),
    path('getplayerbyid', getPlayerByID.as_view()),
    path('records',records.as_view())
]
