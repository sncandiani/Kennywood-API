from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from kennywoodapi.models import *
from kennywoodapi.views import *
from kennywoodapi.views import register_user, login_user
# Setting up the routing for the viewset rather than individual routes for each view method
router = routers.DefaultRouter(trailing_slash=False)
# Registering all the paths for a single resource using default router
router.register(r'parkareas', ParkAreas, 'parkarea')
router.register(r'attractions', Attractions, 'attraction')
# router.register(r'url_path', function, 'model verbose names')
router.register(r'itineraries', ItineraryItems, 'itinerary')



urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user),
    path('login/', login_user),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]