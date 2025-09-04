from rest_framework.routers import DefaultRouter
from .views import HabitViewSet

router = DefaultRouter()
router.register('', HabitViewSet, basename='habit')

urlpatterns = router.urls