from django.urls import path
from . import views

urlpatterns = [

    path('diaristas-cidade', views.DiarstasCidadeList.as_view(), name='diaristas-cidade-list' ),

]