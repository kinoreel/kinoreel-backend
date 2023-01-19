from rest_framework.routers import DefaultRouter

from movies import views

router = DefaultRouter()
router.register(r'', views.RoleViewSet, basename='roles')
router.register(r'movies', views.MoviesViewSet, basename='movies')
router.register(r'rating', views.KinoRatingViewSet, basename='rating')
urlpatterns = router.urls