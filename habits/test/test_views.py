from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from habits.models import Habit
from datetime import time
from rest_framework import status


class HabitAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user2 = User.objects.create_user(username='otheruser', password='password')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_habit(self):
        data = {
            "place": "Home",
            "time": "08:00:00",
            "action": "Morning jog",
            "is_pleasant": False,
            "periodicity": 1,
            "duration_seconds": 60,
            "is_public": True,
            "reward": "Eat fruit"
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['action'], "Morning jog")

    def test_list_own_habits(self):
        Habit.objects.create(
            user=self.user,
            place="Home",
            time=time(8, 0),
            action="Jog",
            is_pleasant=False,
            periodicity=1,
            duration_seconds=60,
            is_public=True
        )
        Habit.objects.create(
            user=self.user2,
            place="Office",
            time=time(9, 0),
            action="Meditate",
            is_pleasant=False,
            periodicity=1,
            duration_seconds=60,
            is_public=True
        )
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_public_habits(self):
        Habit.objects.create(
            user=self.user2,
            place="Park",
            time=time(7, 0),
            action="Stretch",
            is_pleasant=False,
            periodicity=1,
            duration_seconds=60,
            is_public=True
        )
        response = self.client.get('/api/habits/public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)

    def test_delete_habit_owner(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Home",
            time=time(8, 0),
            action="Jog",
            is_pleasant=False,
            periodicity=1,
            duration_seconds=60,
            is_public=True
        )
        response = self.client.delete(f'/api/habits/{habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
