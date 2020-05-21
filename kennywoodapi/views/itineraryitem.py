from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction, ParkArea, Itinerary, Customer


class ItineraryItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        fields = ('id', 'url', 'starttime', 'attraction',)
        # Allows us to expand 
        depth = 2

class ItineraryItems(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            itinerary_item = Itinerary.objects.get(pk=pk)
            serializer = ItineraryItemSerializer(
                itinerary_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        # Set customer equal to the associated user
        # Customer is the user of the following application
        customer = Customer.objects.get(user=request.auth.user)
        # Filters itineraries associated with customer // user 
        itineraries = Itinerary.objects.filter(customer=customer)

        serializer = ItineraryItemSerializer(
            itineraries, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        # Sets attraction equal to the specific attraction depending on ride Id given
        attraction = Attraction.objects.get(pk=request.data["ride_id"])
        customer = Customer.objects.get(user=request.auth.user)

        new_itinerary_item = Itinerary()
        new_itinerary_item.starttime = request.data["starttime"]
        new_itinerary_item.customer = customer
        new_itinerary_item.attraction = attraction

        new_itinerary_item.save()

        serializer = ItineraryItemSerializer(
            new_itinerary_item, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        itinerary = Itinerary.objects.get(pk=pk)
        itinerary.starttime = request.data["starttime"]
        attraction = Attraction.objects.get(pk=request.data["attraction_id"])
        itinerary.attraction = attraction
        itinerary.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            # Get the specific Itinerary object and given the Id, delete it
            itinerary = Itinerary.objects.get(pk=pk)
            itinerary.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)