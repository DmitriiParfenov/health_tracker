from django.contrib import admin

from habits.models import Habit, HabitLog, PleasantHabit


# Register your models here.
@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'date_time', 'action', 'interval', 'execution_time',
                    'is_published', 'habit_user', 'pleasant_habit', 'reward')
    list_display_links = ('id',)
    search_fields = ('date_time', 'habit_user')
    list_filter = ('date_time', 'habit_user')


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'habit', 'user', 'status', 'last_try',)
    list_display_links = ('id',)
    search_fields = ('user', 'status')
    list_filter = ('user', 'status')


@admin.register(PleasantHabit)
class PleasantHabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'date_time', 'action', 'execution_time', 'is_published', 'habit_user',)
    list_display_links = ('id',)
    search_fields = ('date_time', 'habit_user')
    list_filter = ('date_time', 'habit_user')
