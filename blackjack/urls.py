"""
URL configuration for blackjack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from game.views import home_view, blackjack_view, place_bet_view, hit_view, stand_view, newround_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('blackjack/', home_view, name='home'),
    path('blackjack/playgame/', blackjack_view, name='start_blackjack'),
    path('blackjack/playgame/place_bet/<int:game_id>/', place_bet_view, name='place_bet'),
    path('blackjack/playgame/hit/<int:game_id>/', hit_view, name='hit'),
    path('blackjack/playgame/stand/<int:game_id>/', stand_view, name='stand'),
    path('blackjack/playgame/giround/<int:game_id>/', newround_view, name='round'),
]
