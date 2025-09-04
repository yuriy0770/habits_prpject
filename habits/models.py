from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                      limit_choices_to={'is_pleasant': True},
                                      related_name='pleasant_related')
    periodicity = models.PositiveSmallIntegerField(default=1)  
    reward = models.CharField(max_length=255, blank=True, null=True)
    duration_seconds = models.PositiveSmallIntegerField()
    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):

        if self.reward and self.related_habit:
            raise ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")


        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")


        if self.duration_seconds > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")


        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")


        if not (1 <= self.periodicity <= 7):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")

    def __str__(self):
        return f"{self.action} in {self.place} at {self.time} (User: {self.user.username})"