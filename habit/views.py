from rest_framework.viewsets import ModelViewSet

from habit.models import Habit
from habit.serializer import HabitSerializer


class HabitViewSet(ModelViewSet):

    queryset = Habit.objects.all()
#    permission_classes = [~IsModer, AllowAny,] # IsAuthenticated
#    validators = [validate_forbidden_words]

    serializer_class = HabitSerializer

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
