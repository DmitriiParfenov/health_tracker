from django.urls import path

from habits.apps import HabitsConfig
from habits.views import PleasantHabitListAPIView, PleasantHabitCreateAPIView, PleasantHabitRetrieveAPIView, \
    PleasantHabitUpdateAPIView, PleasantHabitDeleteAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('pleasant_habits/', PleasantHabitListAPIView.as_view(), name='pleasant_list'),
    path('pleasant_habits/create/', PleasantHabitCreateAPIView.as_view(), name='pleasant_create'),
    path('pleasant_habits/<int:pk>/', PleasantHabitRetrieveAPIView.as_view(), name='pleasant_detail'),
    path('pleasant_habits/update/<int:pk>/', PleasantHabitUpdateAPIView.as_view(), name='pleasant_update'),
    path('pleasant_habits/delete/<int:pk>/', PleasantHabitDeleteAPIView.as_view(), name='pleasant_delete'),
]
