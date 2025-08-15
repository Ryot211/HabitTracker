from django.urls import path
from .import views
urlpatterns= [
    path('',views.landing_page, name='landing'),
    path('inicio/', views.home, name='home'),
    path('register/',views.register, name='register'),
    path('crear-habito/',views.create_habit, name='create_habit'),
    path('completar/<int:habit_id>',views.completar_habito, name='completar_habito'),
    path('editar/<int:habit_id>',views.editar_habit, name='editar_habit'),
    path('eliminar/<int:habit_id>', views.eliminar_habit, name='eliminar_habit'),
    path('toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),

]