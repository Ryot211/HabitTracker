from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import HabitForm
from django.shortcuts import render, redirect

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
@login_required
def home(request):
    return render(request, 'habits/home.html')

@login_required
def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit =form.save(commit=False)
            habit.user=request.user
            habit.save()
            return redirect('habit_list')
    else:
        form =HabitForm
    return render(request, 'habits/create_habit.html',{'form':form})

