from urllib import request

from django.core import paginator
from rest_framework.viewsets import ModelViewSet
from django.core.paginator import Paginator

from habit.models import Habit
from habit.serializer import HabitSerializer
from habit.validators import validate_time_limit, validate_frequency


class HabitViewSet(ModelViewSet):

    queryset = Habit.objects.all()
    validators = [validate_time_limit, validate_frequency]
    serializer_class = HabitSerializer
    paginator = Paginator(queryset, 5)  # Создаем объект пагинатора, указывая количество объектов на странице
    page_number = request.GET.get('page')  # Получаем номер страницы из GET параметров
    page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

    #    permission_classes = [~IsModer, AllowAny,] # IsAuthenticated

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return CourseDetailSerializer
    #     return CourseSerializer
    #
    # def perform_create(self, serializer):
    #     lesson = serializer.save()
    #     lesson.owner = self.request.user
    #     lesson.save()
    #
    # def get_permissions(self):
    #     if self.action == 'create':
    #         self.permission_classes = (~IsModer,)
    #     elif self.action in ['update', 'retrieve']:
    #         self.permission_classes = (IsModer | IsOwner,)
    #     elif self.action == 'destroy':
    #         self.permission_classes = (IsOwner | ~IsModer,)
    #     return super().get_permissions()
