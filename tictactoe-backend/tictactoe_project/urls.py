"""Tictactoe URL Configuration"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from tictactoe_app import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'api/v1/games', views.GameViewset, basename="game")
urlpatterns = [
    path('', include(router.urls)),
    path('api/admin/', admin.site.urls),
    path('api/v1/game_info/', views.info_by_game_id, name="info"),
    path('api/v1/test/', views.test, name="test"),
]
