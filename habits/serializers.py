from rest_framework import serializers

from habits.models import PleasantHabit
from users.models import User


class PleasantHabitSerializer(serializers.ModelSerializer):
    habit_user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    def validate_execution_time(self, data):
        errors = {}
        if not 0 < data.total_seconds() <= 120:
            errors['invalid_time'] = 'Максимальное время выполнения — 120 сек.'
        if errors:
            raise serializers.ValidationError(errors)
        return data

    class Meta:
        model = PleasantHabit
        fields = ('id', 'habit_user', 'place', 'date_time', 'action', 'interval', 'execution_time', 'is_published',)
