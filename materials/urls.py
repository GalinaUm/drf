from rest_framework.routers import SimpleRouter

from materials.views import LessonViewSet
from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register('', LessonViewSet)

urlpatterns = []

urlpatterns += router.urls