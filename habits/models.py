from datetime import timedelta

from django.db import models

from users.models import NULLABLE


# Create your models here.
class Habit(models.Model):
    class Kinds(models.TextChoices):
        DAILY = ('Ежедневно', 'Ежедневно')
        TWICE = ('Один раз в 2 дня', 'Один раз в 2 дня')
        THREE = ('Один раз в 3 дня', 'Один раз в 3 дня')
        FOUR = ('Один раз в 4 дня', 'Один раз в 4 дня')
        FIVE = ('Один раз в 5 дней', 'Один раз в 5 дней')
        SIX = ('Один раз в 6 дней', 'Один раз в 6 дней')
        SEVEN = ('Один раз в 7 дней', 'Один раз в 7 дней')

    habit_user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец привычки')
    place = models.CharField(max_length=150, verbose_name='место')
    date_time = models.DateTimeField(verbose_name='время привычки')
    action = models.CharField(max_length=150, verbose_name='действие')
    interval = models.CharField(max_length=17, choices=Kinds.choices, default=Kinds.DAILY, verbose_name='периодичность')
    execution_time = models.DurationField(verbose_name='время выполнения', default=timedelta(minutes=2),
                                          help_text='Введите время в секундах. Максимальное время — 120 сек.')
    reward = models.CharField(max_length=150, verbose_name='вознаграждение', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='статус')
    pleasant_habit = models.ForeignKey('habits.PleasantHabit', on_delete=models.SET_NULL,
                                       verbose_name='полезная привычка', **NULLABLE)

    def __str__(self):
        return f'я буду {self.action} в {self.date_time} в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ('habit_user',)


class HabitLog(models.Model):
    habit = models.ForeignKey('habits.Habit', on_delete=models.CASCADE, verbose_name='привычка')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец')
    status = models.BooleanField(default=False, verbose_name='статус')
    last_try = models.DateTimeField(auto_now_add=True, verbose_name='попытка')

    class Meta:
        verbose_name = 'Информация'
        verbose_name_plural = 'Информации'


class PleasantHabit(models.Model):
    habit_user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец привычки')
    place = models.CharField(max_length=150, verbose_name='место')
    date_time = models.DateTimeField(verbose_name='время привычки')
    action = models.CharField(max_length=150, verbose_name='действие')
    execution_time = models.DurationField(verbose_name='время выполнения', default=timedelta(minutes=2),
                                          help_text='Введите время в секундах. Максимальное время — 120 сек.')
    is_published = models.BooleanField(default=False, verbose_name='статус')

    def __str__(self):
        return f'я буду {self.action} в {self.date_time} в {self.place}'

    class Meta:
        verbose_name = 'приятная привычка'
        verbose_name_plural = 'приятные привычки'
        ordering = ('habit_user',)
