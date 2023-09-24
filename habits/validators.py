from rest_framework import serializers

from habits.models import Habit


class ExecutionTimeValidation:
    """Класс для валидации поля <execution_time> для моделей Habit и PleasantHabit. Значение данного поля должно быть
    в диапазоне от 0 до 120 секунд включительно."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        errors = {}
        if not 0 < value.total_seconds() <= 120:
            errors['invalid_time'] = 'Максимальное время выполнения — 120 сек.'
        if errors:
            raise serializers.ValidationError(errors)


class RewardOrPleasantHabitValidation:
    """Класс для валидации полей <reward> и <pleasant_habit> модели Habit. При создании объекта необходимо указать
    ЛИБО <reward>, ЛИБО <pleasant_habit>."""

    def __init__(self, field_1, field_2):
        self.field_1 = field_1
        self.field_2 = field_2

    def __call__(self, value):
        errors = {}
        reward = value.get(self.field_1)
        pleasant_habit = value.get(self.field_2)
        if (not reward and not pleasant_habit) or (reward and pleasant_habit):
            errors['reward_or_pleasant_habit_fields'] = "Необходимо указать ЛИБО 'reward', ЛИБО 'pleasant_habit'."
        if errors:
            raise serializers.ValidationError(errors)


class CountHabitPerDayValidation:
    """Класс для валидации поля <date_time> модели Habit. Пользователь не может устанавливать привычку чаще 1 в час."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # Объявление переменных.
        errors = {}
        user = value.get('habit_user')
        hour = value.get(self.field).hour

        # Получение всех временных интервалов одного пользователя.
        hours_data = Habit.objects.select_related('habit_user').filter(
            habit_user__email=user
        ).values('date_time')
        hour_by_user = [x['date_time'].hour for x in hours_data]

        # Нельзя создавать 1 привычку чаще чем 1 раз в час.
        if hour in hour_by_user:
            errors['date_time'] = 'Для одного пользователя необходимо устанавливать привычку не чаще 1 в час.'
        if errors:
            raise serializers.ValidationError(errors)


class PleasantHabitOwnerValidation:
    """Класс для валидации поля <pleasant_habit> модели Habit. Пользователь может добавлять только свою приятную
    привычку или доступную для всех."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        errors = {}
        pleasant_habit = value.get(self.field)
        user = value.get('habit_user')
        if pleasant_habit.habit_user != user and not pleasant_habit.is_published:
            errors['pleasant_habit'] = 'Вы можете добавлять только свою приятную привычку или доступную для всех.'
        if errors:
            raise serializers.ValidationError(errors)
