from django.urls import include, path,re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('convert',views.Conversion)
urlpatterns = [
    path('', include(router.urls)),
    path('gettext/',views.getText, name="getText")
]