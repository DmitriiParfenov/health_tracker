import time
from datetime import datetime, timedelta

import requests
from celery import shared_task
from config import settings
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from habits.models import Habit, HabitLog

TELEGRAM_API_KEY = settings.TELEGRAM_API_KEY
URL = 'https://api.telegram.org/bot'


def send_telegram_message(habit):
    """Функция отправляет пользователям в телеграм напоминания об исполнении привычек. Когда поступило напоминание,
    пользователь в течение двух минут должен отправить <да> в чат об успешном исполнении привычки. Если он это сделает,
    то ему придет сообщение с вознаграждением в зависимости от объекта привычки, в ином случае — напутствующее
    сообщение."""

    # Объявление переменных.
    chat_id = habit.habit_user.telegram_chat_id
    action = habit.action
    time_start = habit.date_time.strftime('%H:%M')
    place = habit.place
    time_duration = habit.execution_time.seconds
    reward = habit.reward
    pleasant_habit = habit.pleasant_habit

    # Формирование сообщения для отправки.
    message = f"Привет! Вам пора поработать: \nПривычка — я буду {action} в {time_start} в {place}.\n" \
              f"Время на выполнение — {time_duration} секунд.\n" \
              f"Максимальное время на выполнение — 120 секунд.\n" \
              f"Если вы выполнили действие, то введите в чате — да."

    # Отправка сообщения.
    message_to_bot = requests.get(f"{URL}{TELEGRAM_API_KEY}/sendMessage?chat_id={chat_id}&text={message}").json()

    # Получение даты отправки сообщения.
    date_start_habit = message_to_bot['result']['date']

    # Формирование дедлайна на получение сообщения от пользователя об успешности исполнения проверки.
    time.sleep(120)
    date_end_habit = datetime.fromtimestamp(date_start_habit) + timedelta(seconds=120)

    # Получение всех сообщений от пользователя с момента отправки уведомления до окончания дедлайна.
    message_from_bot = requests.get(f'{URL}{TELEGRAM_API_KEY}/getUpdates?offset=0').json()['result']
    list_messages = [x['message']['text'].lower() for x in message_from_bot if
                     date_end_habit.timestamp() > x['message']['date'] > date_start_habit]

    # Если в списке полученных сообщений есть <да>, то отправляем пользователю вознаграждение с формированием
    # лога с информацией об исполнении текущей привычки. Если <да> нет в списке, то отправляем напутствующее
    # сообщение с формированием лога.
    if 'да' in list_messages:
        success = 'Вы молодец!'
        if reward:
            success = f'Вы молодец!\nДля закрепления привычки воспользуйтесь вознаграждением — {reward}.\n' \
                      f'Продолжайте в том же духе!'
        elif pleasant_habit:
            success = f'Вы молодец!\nДля закрепления привычки выполните действие: \n' \
                      f'Я буду {pleasant_habit.action} в {pleasant_habit.date_time.strftime("%H:%M")} в ' \
                      f'{pleasant_habit.place}.\nПродолжайте в том же духе!'
        requests.get(f"{URL}{TELEGRAM_API_KEY}/sendMessage?chat_id={chat_id}&text={success}").json()

        HabitLog.objects.create(
            habit=habit,
            user=habit.habit_user,
            status=True
        )
    else:
        failure = 'Вы лентяй!'
        requests.get(f"{URL}{TELEGRAM_API_KEY}/sendMessage?chat_id={chat_id}&text={failure}").json()

        HabitLog.objects.create(
            habit=habit,
            user=habit.habit_user,
            status=False
        )


@shared_task
def telegram_schedule():
    """Функция работает при помощи celery-beat. В зависимости от расписания и периодичности она отправляет пользователям
    сообщения при помощи функции send_telegram_message(habit). Логика отправки: для каждой привычки проверяется
    информация по модели HabitLog. Если у привычки такой информации нет, то будет создан объект модели HabitLog с
    текущей датой и далее в зависимости от периодичности и даты создания информации будут отправляться сообщения."""

    # Получение текущей даты.
    now = datetime.now()

    for habit in Habit.objects.all():

        # Для каждой привычки и пользователя проверяем информацию, которая содержит дату отправки сообщения в телеграм.
        user_log = HabitLog.objects.filter(user=habit.habit_user.pk, habit=habit.pk)

        # Если такой объект с информацией существует, то получаем самую последнюю дату отправки и в зависимости от
        # периодичности вызываем функцию send_telegram_message(habit). В ином случае — отправляет пользователю сообщение
        # и создаем объект HabitLog вручную.
        if user_log.exists():
            date_try = user_log.order_by('-last_try').first()
            if habit.interval == habit.Kinds.DAILY:
                if (now.day - date_try.last_try.day) == 1 and (
                        now.strftime('%H:%M') == habit.date_time.strftime('%H:%M')):
                    send_telegram_message(habit)
            elif habit.interval == habit.Kinds.TWICE:
                if (now.day - date_try.last_try.day) == 2 and (
                        now.strftime('%H:%M') == habit.date_time.strftime('%H:%M')):
                    send_telegram_message(habit)
            elif habit.interval == habit.Kinds.THREE:
                if (now.day - date_try.last_try.day) == 3 and (
                        now.strftime('%H:%M') == habit.date_time.strftime('%H:%M')):
                    send_telegram_message(habit)
            elif habit.interval == habit.Kinds.FOUR:
                if (now.day - date_try.last_try.day) == 4 and (
                        now.strftime('%H:%M') == habit.date_time.strftime('%H:%M')):
                    send_telegram_message(habit)
            elif habit.interval == habit.Kinds.FIVE:
                if (now.day - date_try.last_try.day) == 5 and (
                        now.strftime('%H:%M') == habit.date_time.strftime('%H:%M')):
                    send_telegram_message(habit)
            elif habit.interval == habit.Kinds.SIX:
                if (now.day - date_try.last_try.day) == 6 and (
                        now.strftime('%H:%M') == habit.date_time.strftime('%H:%M')):
                    send_telegram_message(habit)
            elif habit.interval == habit.Kinds.SEVEN:
                if (now.day - date_try.last_try.day) == 7 and (
                        now.strftime('%H:%M') == habit.date_time.strftime('%H:%M')):
                    send_telegram_message(habit)
        else:
            if now.time().hour >= habit.date_time.hour:
                message = f'Начинаем вырабатывать привычку:\n' \
                          f'<я буду {habit.action} в {habit.date_time.strftime("%H:%M")} в {habit.place}> ' \
                          f'с периодичностью: {habit.interval}.\n' \
                          f'Постарайтесь не пропускать выполнять действия!'
                user_chat_id = habit.habit_user.telegram_chat_id
                requests.get(f"{URL}{TELEGRAM_API_KEY}/sendMessage?chat_id={user_chat_id}&text={message}").json()

                HabitLog.objects.create(
                    habit=habit,
                    user=habit.habit_user,
                    status=False
                )


# Создание Crontab-расписания.
schedule, _ = CrontabSchedule.objects.get_or_create(
    minute='*',
    hour='*',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)
# Создание периодической задачи.
PeriodicTask.objects.get_or_create(
    crontab=schedule,
    name='Send telegram message',
    task='habits.tasks.telegram_schedule',
)


@shared_task
def register_habit(action, time_duration, time_start, place, chat_id, period=None):
    """Функция работает при помощи celery. При создании объектов модели Habit и PleasantHabit пользователь получает
    уведомление об этом."""

    if period is None:
        message = f"Вы зарегистрировали приятную привычку: я буду {action} в {time_start} в {place}.\n\n" \
                  f"Время исполнения — {time_duration} секунд.\n"
    else:
        message = f"Вы зарегистрировали привычку: я буду {action} в {time_start} в {place}.\n\n" \
                  f"Время исполнения — {time_duration} секунд.\n" \
                  f"Периодичность — {period}.\n" \
                  f"Максимальное время исполнения — 120 сек.\n"

    requests.get(f"{URL}{TELEGRAM_API_KEY}/sendMessage?chat_id={chat_id}&text={message}").json()
