from django.urls import path, include
from rest_framework.routers import SimpleRouter

from habit.apps import HabitConfig
from habit.views import HabitViewSet


app_name = HabitConfig.name

router = SimpleRouter()
router.register('', HabitViewSet)

urlpatterns = [
    # path('tracker/', HabitViewSet.as_view(), namespace='tracker'),
]



urlpatterns += router.urls