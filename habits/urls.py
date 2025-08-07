from django.urls import path
from .import views
urlpatterns= [
    path('register/',views.register, name='register'),
    path('crear-habito/',views.create_habit, name='create_habit'),
]