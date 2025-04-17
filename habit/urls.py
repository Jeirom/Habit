from rest_framework.routers import SimpleRouter

from habit.apps import HabitConfig
from habit.views import HabitViewSet


app_name = HabitConfig.name

router = SimpleRouter()
router.register("", HabitViewSet)

urlpatterns = []


urlpatterns += router.urls
