from django.test import TestCase
from django.contrib.auth.models import User
from habits.models import Habit
from django.core.exceptions import ValidationError
from datetime import time

class HabitModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_habit_creation(self):
        habit = Habit(
            user=self.user,
            place='Home',
            time=time(8, 0),
            action='Morning exercise',
            is_pleasant=False,
            periodicity=1,
            duration_seconds=60,
            is_public=True,
            reward='Eat a treat'
        )
        habit.full_clean()  # Проверка валидации
        habit.save()
        self.assertEqual(Habit.objects.count(), 1)

    def test_validation_reward_and_related(self):
        pleasant = Habit.objects.create(
            user=self.user,
            place='Home',
            time=time(9, 0),
            action='Relaxing bath',
            is_pleasant=True,
            periodicity=1,
            duration_seconds=60,
            is_public=False
        )
        habit = Habit(
            user=self.user,
            place='Park',
            time=time(7, 0),
            action='Jogging',
            is_pleasant=False,
            periodicity=1,
            duration_seconds=60,
            is_public=True,
            reward='Eat a treat',
            related_habit=pleasant
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_duration_seconds_limit(self):
        habit = Habit(
            user=self.user,
            place='Office',
            time=time(10, 0),
            action='Quick meditation',
            is_pleasant=False,
            periodicity=1,
            duration_seconds=121,
            is_public=False
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_periodicity_limits(self):
        habit = Habit(
            user=self.user,
            place='Gym',
            time=time(18, 0),
            action='Workout',
            is_pleasant=False,
            periodicity=8,
            duration_seconds=60,
            is_public=False
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()