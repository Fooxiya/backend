from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authapp.views import UserViewSet
from todomanager.views import ProjectViewSet, TodoViewSet, get_view, post_view


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('projects', ProjectViewSet)
router.register('todo', TodoViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api_get/', get_view),
    path('api_post/', post_view)
]

