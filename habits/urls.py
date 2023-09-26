from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitListAPIView, HabitCreateAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDeleteAPIView, PleasantHabitListAPIView, PleasantHabitCreateAPIView, PleasantHabitRetrieveAPIView, \
    PleasantHabitUpdateAPIView, PleasantHabitDeleteAPIView

app_name = HabitsConfig.name

urlpatterns = [
    # Привычки для формирования — Habit model.
    path('', HabitListAPIView.as_view(), name='habit_list'),
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_detail'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('delete/<int:pk>/', HabitDeleteAPIView.as_view(), name='habit_delete'),

    # Приятные привычки — PleasantHabit model.
    path('pleasant/', PleasantHabitListAPIView.as_view(), name='pleasant_habit_list'),
    path('pleasant/create/', PleasantHabitCreateAPIView.as_view(), name='pleasant_habit_create'),
    path('pleasant/<int:pk>/', PleasantHabitRetrieveAPIView.as_view(), name='pleasant_habit_detail'),
    path('pleasant/update/<int:pk>/', PleasantHabitUpdateAPIView.as_view(), name='pleasant_habit_update'),
    path('pleasant/delete/<int:pk>/', PleasantHabitDeleteAPIView.as_view(), name='pleasant_habit_delete'),
]
