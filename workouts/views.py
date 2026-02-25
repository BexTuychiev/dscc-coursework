from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exercise, Workout
from .forms import WorkoutForm, ExerciseForm, WorkoutExerciseFormSet


def home(request):
    return render(request, 'workouts/home.html')


@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'workouts/workout_list.html', {'workouts': workouts})


@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    return render(request, 'workouts/workout_detail.html', {'workout': workout})


@login_required
def workout_create(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        formset = WorkoutExerciseFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            formset.instance = workout
            formset.save()
            messages.success(request, 'Workout created successfully!')
            return redirect('workout_detail', pk=workout.pk)
    else:
        form = WorkoutForm()
        formset = WorkoutExerciseFormSet()
    return render(request, 'workouts/workout_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Log New Workout',
    })


@login_required
def workout_edit(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        formset = WorkoutExerciseFormSet(request.POST, instance=workout)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Workout updated successfully!')
            return redirect('workout_detail', pk=workout.pk)
    else:
        form = WorkoutForm(instance=workout)
        formset = WorkoutExerciseFormSet(instance=workout)
    return render(request, 'workouts/workout_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Edit Workout',
    })


@login_required
def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    if request.method == 'POST':
        workout.delete()
        messages.success(request, 'Workout deleted.')
        return redirect('workout_list')
    return render(request, 'workouts/workout_confirm_delete.html', {
        'workout': workout,
    })


@login_required
def exercise_list(request):
    exercises = Exercise.objects.filter(created_by=request.user)
    return render(request, 'workouts/exercise_list.html', {
        'exercises': exercises,
    })


@login_required
def exercise_create(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.created_by = request.user
            exercise.save()
            messages.success(request, 'Exercise added!')
            return redirect('exercise_list')
    else:
        form = ExerciseForm()
    return render(request, 'workouts/exercise_form.html', {
        'form': form,
    })
