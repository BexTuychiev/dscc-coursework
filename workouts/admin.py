from django.contrib import admin
from .models import Exercise, Workout, WorkoutExercise


class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'muscle_group', 'created_by']
    list_filter = ['muscle_group']
    search_fields = ['name', 'description']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'date', 'duration_minutes']
    list_filter = ['date', 'user']
    search_fields = ['title', 'notes']
    inlines = [WorkoutExerciseInline]


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ['workout', 'exercise', 'sets', 'reps', 'weight']
    list_filter = ['exercise__muscle_group']
