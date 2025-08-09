from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import HabitForm
from datetime import date, timedelta
from django.http import HttpResponseRedirect
from .models import Habit, HabitEntry
from django.shortcuts import render, redirect, get_object_or_404


def register(request):
    if request.method == 'POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'habits/register.html', {'form':form})
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'habits/landing.html')

def editar_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/editar_habit.html',{'form':form})

def eliminar_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        habit.delete()
        return redirect('home')
    return render(request, 'habits/eliminar_habit.html',{'habit':habit})



@login_required
def home(request):
   
    hoy = date.today()
    dias = [hoy - timedelta(days=i) for i in range(6,-1,-1) ]
    habits = Habit.objects.filter(user=request.user).order_by('-created_at')

    completados_hoy =HabitEntry.objects.filter(
        habit__in= habits,
        date=hoy,
        completed=True
    ).values_list('habit_id', flat=True)

    historial = {}
    porcentajes = {}
    
    for habit in habits:
        entradas = HabitEntry.objects.filter(
            habit=habit,
            date__in=dias
        ).values_list('date','completed')

        completados_dict = {fecha: completo for fecha, completo in entradas }

        completados = [completados_dict.get(d,False)for d in dias]
        historial[habit.id]=completados

        total= len(completados)
        porcentaje = int((sum(completados)/total)*100) if total> 0 else 0
        porcentajes[habit.id]=porcentaje
     
    return render(request, 'habits/home.html',{'habits':habits,'completados_hoy':completados_hoy,'dias':dias,'historial':historial,"porcentajes":porcentajes})

@login_required
def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit =form.save(commit=False)
            habit.user=request.user
            habit.save()
            return redirect('/inicio')
    else:
        form =HabitForm
    return render(request, 'habits/create_habit.html',{'form':form})

@login_required
def completar_habito(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)
    today = date.today()

    entry, created = HabitEntry.objects.get_or_create(
        habit=habit,
        date=today,
        defaults={'completed':True}
    )
    if not created and not entry.completed:
        entry.completed = True
        entry.save()
    return redirect('/inicio')


# últimos 7 días (del más antiguo al más reciente)

