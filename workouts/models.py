from django.db import models
from django.contrib.auth.models import User


class Exercise(models.Model):
    MUSCLE_GROUPS = [
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('shoulders', 'Shoulders'),
        ('arms', 'Arms'),
        ('legs', 'Legs'),
        ('core', 'Core'),
        ('cardio', 'Cardio'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    muscle_group = models.CharField(max_length=20, choices=MUSCLE_GROUPS)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='exercises'
    )

    def __str__(self):
        return f"{self.name} ({self.get_muscle_group_display()})"

    class Meta:
        ordering = ['name']


class Workout(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='workouts'
    )
    exercises = models.ManyToManyField(
        Exercise, through='WorkoutExercise', blank=True
    )

    def __str__(self):
        return f"{self.title} - {self.date}"

    class Meta:
        ordering = ['-date']


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name='workout_exercises'
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name='workout_exercises'
    )
    sets = models.PositiveIntegerField(default=3)
    reps = models.PositiveIntegerField(default=10)
    weight = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps}"

    class Meta:
        ordering = ['id']
