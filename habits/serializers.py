from rest_framework import serializers

from habits.models import PleasantHabit, Habit
from habits.validators import ExecutionTimeValidation, RewardOrPleasantHabitValidation, CountHabitPerDayValidation, \
    PleasantHabitOwnerValidation, CountPleasantHabitPerDayValidation
from users.models import User


class HabitSerializer(serializers.ModelSerializer):
    habit_user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    execution_time = serializers.DurationField(validators=[ExecutionTimeValidation(field='execution_time')])

    class Meta:
        model = Habit
        fields = ('id', 'habit_user', 'place', 'date_time', 'action', 'interval',
                  'execution_time', 'is_published', 'pleasant_habit', 'reward')
        validators = [RewardOrPleasantHabitValidation(field_1='reward', field_2='pleasant_habit'),
                      CountHabitPerDayValidation(field='date_time'),
                      PleasantHabitOwnerValidation(field='pleasant_habit')]


class PleasantHabitSerializer(serializers.ModelSerializer):
    habit_user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    execution_time = serializers.DurationField(validators=[ExecutionTimeValidation(field='execution_time')])

    class Meta:
        model = PleasantHabit
        fields = ('id', 'place', 'date_time', 'action', 'execution_time', 'is_published', 'habit_user')
        validators = [CountPleasantHabitPerDayValidation(field='date_time')]
