from django.contrib.auth.models import User
from django.db import models

class Habit(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    frequency = models.CharField(
        max_length=10,
        choices=[('daily','Diario'),('weekly','Semanal')],
        default='daily'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HabitEntry(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('habit','date')
    def __str__(self):
        return f"{self.habit.name} - {self.date}"

