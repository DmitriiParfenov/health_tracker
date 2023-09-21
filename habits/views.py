from rest_framework import generics

from habits.models import PleasantHabit
from habits.permissions import IsAuthenticatedAndIsOwner
from habits.serializers import PleasantHabitSerializer
from django.db.models import Q


# Create your views here.
class PleasantHabitCreateAPIView(generics.CreateAPIView):
    queryset = PleasantHabit.objects.all()
    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = PleasantHabitSerializer

    def perform_create(self, serializer):
        new_hab = serializer.save()
        new_hab.habit_user = self.request.user
        new_hab.save()


class PleasantHabitListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = PleasantHabitSerializer

    def get_queryset(self):
        q = Q(is_published=True) | Q(habit_user=self.request.user)
        return PleasantHabit.objects.filter(q)


class PleasantHabitRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()


class PleasantHabitUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()


class PleasantHabitDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticatedAndIsOwner,)
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()
