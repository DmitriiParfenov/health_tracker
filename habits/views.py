from django.db.models import Q
from rest_framework import generics

from habits.models import Habit, PleasantHabit
from habits.paginator import Pagination
from habits.permissions import IsAuthenticatedAndIsOwner
from habits.serializers import HabitSerializer, PleasantHabitSerializer
from habits.tasks import register_habit


# Create your views here.
class HabitCreateAPIView(generics.CreateAPIView):
    """Для создания объектов модели Habit."""

    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        """Метод присваивает создаваемому объекту текущего пользователя и запускает отложенную задачу для отправки
        уведомления о создании объекта пользователю."""

        new_hab = serializer.save()
        new_hab.habit_user = self.request.user
        register_habit.delay(new_hab.action,
                             new_hab.execution_time.seconds,
                             new_hab.date_time.strftime('%H:%M'),
                             new_hab.place,
                             new_hab.habit_user.telegram_chat_id,
                             new_hab.interval)
        new_hab.save()


class HabitListAPIView(generics.ListAPIView):
    """Для просмотра всех объектов модели Habit."""

    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = HabitSerializer
    pagination_class = Pagination

    def get_queryset(self):
        """Возвращает публичные привычки и те привычки, пользователями которых являются текущие пользователи."""
        q = Q(is_published=True) | Q(habit_user=self.request.user)
        return Habit.objects.filter(q)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Для просмотра определенного объекта модели Habit."""

    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Для обновления информации об объекте модели Habit."""

    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitDeleteAPIView(generics.DestroyAPIView):
    """Для удаления объектов модели Habit."""

    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class PleasantHabitCreateAPIView(generics.CreateAPIView):
    """Для создания объектов модели PleasantHabit."""

    queryset = PleasantHabit.objects.all()
    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = PleasantHabitSerializer

    def perform_create(self, serializer):
        """Метод присваивает создаваемому объекту текущего пользователя и запускает отложенную задачу для отправки
        уведомления о создании объекта пользователю."""

        new_hab = serializer.save()
        new_hab.habit_user = self.request.user
        register_habit.delay(new_hab.action,
                             new_hab.execution_time.seconds,
                             new_hab.date_time.strftime('%H:%M'),
                             new_hab.place,
                             new_hab.habit_user.telegram_chat_id)
        new_hab.save()


class PleasantHabitListAPIView(generics.ListAPIView):
    """Для просмотра всех объектов модели PleasantHabit."""

    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = PleasantHabitSerializer
    pagination_class = Pagination

    def get_queryset(self):
        """Возвращает публичные привычки и те привычки, пользователями которых являются текущие пользователи."""
        q = Q(is_published=True) | Q(habit_user=self.request.user)
        return PleasantHabit.objects.filter(q)


class PleasantHabitRetrieveAPIView(generics.RetrieveAPIView):
    """Для просмотра определенного объекта модели PleasantHabit."""

    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()


class PleasantHabitUpdateAPIView(generics.UpdateAPIView):
    """Для обновления информации об объекте модели PleasantHabit."""

    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()


class PleasantHabitDeleteAPIView(generics.DestroyAPIView):
    """Для удаления объектов модели PleasantHabit."""

    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()
