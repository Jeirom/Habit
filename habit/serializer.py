from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from habit.models import Habit



class HabitSerializer(ModelSerializer):
    """ Сериалайзер для Habit. Включает все поля"""
    class Meta:
        model = Habit
        fields = '__all__'

