from datetime import timedelta

from django.db import models


# Create your models here.
class PleasantHabit(models.Model):
    class Kinds(models.TextChoices):
        DAILY = ('Ежедневно', 'Ежедневно')
        ONE = ('Один раз в неделю', 'Один раз в неделю')
        TWICE = ('Два раз в неделю', 'Два раз в неделю')
        THREE = ('Три раз в неделю', 'Три раз в неделю')
        FOUR = ('Четыре раз в неделю', 'Четыре раз в неделю')
        FIVE = ('Пять раз в неделю', 'Пять раз в неделю')
        SIX = ('Шесть раз в неделю', 'Шесть раз в неделю')

    habit_user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец привычки')
    place = models.CharField(max_length=150, verbose_name='место')
    date_time = models.DateTimeField(verbose_name='время привычки')
    action = models.CharField(max_length=150, verbose_name='действие')
    interval = models.CharField(max_length=19, choices=Kinds.choices, default=Kinds.DAILY, verbose_name='периодичность')
    execution_time = models.DurationField(verbose_name='время выполнения', default=timedelta(minutes=2),
                                          help_text='Введите время в секундах. Максимальное время — 120 сек.')
    is_published = models.BooleanField(default=False, verbose_name='статус')

    def __str__(self):
        return f'я буду {self.action} в {self.date_time} в {self.place}'

    class Meta:
        verbose_name = 'полезная привычка'
        verbose_name_plural = 'полезные привычки'
        ordering = ('habit_user',)


class HabitLog(models.Model):
    habit = models.ForeignKey('habits.PleasantHabit', on_delete=models.CASCADE, verbose_name='привычка')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец')
    status = models.BooleanField(default=False, verbose_name='статус')
    last_try = models.DateTimeField(auto_now_add=True, verbose_name='попытка')

    class Meta:
        verbose_name = 'Информация'
        verbose_name_plural = 'Информации'
