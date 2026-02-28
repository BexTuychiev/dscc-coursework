import pytest
from django.test import Client
from django.contrib.auth.models import User
from workouts.models import Exercise, Workout, WorkoutExercise
from datetime import date


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass123')


@pytest.fixture
def client_logged_in(user):
    client = Client()
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def exercise(user):
    return Exercise.objects.create(
        name='Bench Press',
        muscle_group='chest',
        created_by=user,
    )


@pytest.fixture
def workout(user):
    return Workout.objects.create(
        title='Monday Push',
        date=date(2026, 2, 10),
        duration_minutes=60,
        user=user,
    )


@pytest.mark.django_db
def test_create_exercise(user):
    ex = Exercise.objects.create(
        name='Squat', muscle_group='legs', created_by=user
    )
    assert ex.name == 'Squat'
    assert ex.created_by == user


@pytest.mark.django_db
def test_create_workout(user):
    w = Workout.objects.create(
        title='Leg Day', date=date(2026, 2, 12),
        duration_minutes=45, user=user,
    )
    assert w.user == user
    assert w.duration_minutes == 45


@pytest.mark.django_db
def test_add_exercise_to_workout(workout, exercise):
    we = WorkoutExercise.objects.create(
        workout=workout, exercise=exercise,
        sets=4, reps=8, weight=80.0,
    )
    assert workout.exercises.count() == 1
    assert we.sets == 4


@pytest.mark.django_db
def test_home_page(client):
    resp = client.get('/')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_workout_list_requires_login(client):
    resp = client.get('/workouts/')
    assert resp.status_code == 302
    assert '/accounts/login/' in resp.url


@pytest.mark.django_db
def test_workout_list_logged_in(client_logged_in):
    resp = client_logged_in.get('/workouts/')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_create_workout_view(client_logged_in):
    resp = client_logged_in.post('/workouts/new/', {
        'title': 'Test Workout',
        'date': '2026-02-15',
        'duration_minutes': '30',
        'notes': '',
        'workout_exercises-TOTAL_FORMS': '0',
        'workout_exercises-INITIAL_FORMS': '0',
        'workout_exercises-MIN_NUM_FORMS': '0',
        'workout_exercises-MAX_NUM_FORMS': '1000',
    })
    assert resp.status_code == 302
    assert Workout.objects.filter(title='Test Workout').exists()


@pytest.mark.django_db
def test_register_user(client):
    resp = client.post('/accounts/register/', {
        'username': 'newuser',
        'password1': 'complexpass123!',
        'password2': 'complexpass123!',
    })
    assert resp.status_code == 302
    assert User.objects.filter(username='newuser').exists()
