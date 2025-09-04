from celery import shared_task
from django.utils.timezone import now
from .models import Habit
import requests
from django.conf import settings

@shared_task
def send_telegram_reminders():
    current_time = now().time().replace(second=0, microsecond=0)

    habits = Habit.objects.filter(time=current_time)
    bot_token = settings.TELEGRAM_BOT_TOKEN

    for habit in habits:
        user = habit.user
        chat_id = getattr(user, 'telegram_chat_id', None)
        if not chat_id:
            continue

        message = f"Напоминание: пора выполнить привычку:\n{habit.action} в {habit.place} в {habit.time.strftime('%H:%M')}"

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {
            'chat_id': chat_id,
            'text': message,
        }
        try:
            requests.get(url, params=params)
        except Exception as e:

            print(f"Ошибка отправки Telegram уведомления: {e}")