from django.contrib import admin

from habits.models import PleasantHabit


# Register your models here.
@admin.register(PleasantHabit)
class PleasantHabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'date_time', 'action', 'interval', 'execution_time', 'is_published', 'habit_user')
    list_display_links = ('id', )
    search_fields = ('date_time', 'habit_user')
    list_filter = ('date_time', 'habit_user')
