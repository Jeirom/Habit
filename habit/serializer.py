from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from habit.models import Habit



class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

