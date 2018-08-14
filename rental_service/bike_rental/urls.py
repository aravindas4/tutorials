from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from bike_rental import views

router = DefaultRouter()
router.register(r'stations', views.StationViewSet)
router.register(r'rents', views.RentViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls))
]
