from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from workouts.models import Exercise, Workout, WorkoutExercise
from datetime import date


class Command(BaseCommand):
    help = 'Seed the database with sample exercises and workouts'

    def handle(self, *args, **options):
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('No users found. Create a superuser first.'))
            return

        if Exercise.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists, skipping.'))
            return

        exercises = Exercise.objects.bulk_create([
            Exercise(name='Bench Press', muscle_group='chest', created_by=user),
            Exercise(name='Squat', muscle_group='legs', created_by=user),
            Exercise(name='Deadlift', muscle_group='back', created_by=user),
            Exercise(name='Overhead Press', muscle_group='shoulders', created_by=user),
            Exercise(name='Barbell Row', muscle_group='back', created_by=user),
            Exercise(name='Pull-ups', muscle_group='back',
                     description='Bodyweight pull-ups', created_by=user),
            Exercise(name='Plank', muscle_group='core',
                     description='Hold for time', created_by=user),
        ])

        w1 = Workout.objects.create(
            title='Push Day', date=date(2026, 2, 24),
            duration_minutes=55, notes='Felt strong today', user=user,
        )
        WorkoutExercise.objects.create(
            workout=w1, exercise=exercises[0], sets=4, reps=8, weight=80)
        WorkoutExercise.objects.create(
            workout=w1, exercise=exercises[3], sets=3, reps=10, weight=45)

        w2 = Workout.objects.create(
            title='Pull Day', date=date(2026, 2, 26),
            duration_minutes=50, notes='Good back pump', user=user,
        )
        WorkoutExercise.objects.create(
            workout=w2, exercise=exercises[2], sets=3, reps=5, weight=120)
        WorkoutExercise.objects.create(
            workout=w2, exercise=exercises[4], sets=4, reps=8, weight=60)
        WorkoutExercise.objects.create(
            workout=w2, exercise=exercises[5], sets=3, reps=10)

        w3 = Workout.objects.create(
            title='Leg Day', date=date(2026, 3, 1),
            duration_minutes=60, user=user,
        )
        WorkoutExercise.objects.create(
            workout=w3, exercise=exercises[1], sets=5, reps=5, weight=100)

        self.stdout.write(self.style.SUCCESS(
            'Seeded 7 exercises and 3 workouts.'))
