from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action', 'is_pleasant',
            'related_habit', 'periodicity', 'reward', 'duration_seconds',
            'is_public', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        reward = data.get('reward')
        related_habit = data.get('related_habit')
        is_pleasant = data.get('is_pleasant')
        duration_seconds = data.get('duration_seconds')
        periodicity = data.get('periodicity')

        if reward and related_habit:
            raise serializers.ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")

        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

        if duration_seconds and duration_seconds > 120:
            raise serializers.ValidationError("Время выполнения не должно превышать 120 секунд.")

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной.")

        if periodicity and not (1 <= periodicity <= 7):
            raise serializers.ValidationError("Периодичность должна быть от 1 до 7 дней.")

        return data