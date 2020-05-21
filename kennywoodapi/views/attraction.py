from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction
from kennywoodapi.models import ParkArea

# Python to JSON
class AttractionSerializer(serializers.HyperlinkedModelSerializer):
   
    class Meta:
        model = Attraction
        # Uses model preestablished attraction and gives it a url 
        # Url is fulfilling default route constraints
        url = serializers.HyperlinkedIdentityField(
            view_name='Attraction',
            lookup_field='id'
        )
        # Indicating which fields you want to return for each item when serialization finishes
        fields = ('id', 'url', 'name', 'area',)
        # Depth determines how deep it will be displayed ?? 
        depth = 2


class Attractions(ViewSet):

    def create(self, request):
        
        new_attraction = Attraction()
        new_attraction.name = request.data["name"]
        # Area refers to ParkAreas, so requesting the data requires getting the specific park area
        area = ParkArea.objects.get(pk=request.data["area_id"])
        new_attraction.area = area
        new_attraction.save()

        serializer = AttractionSerializer(new_attraction, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        # If the pk doesn't exist in the database, it will throw an exception error
        try:
            # Returns a single park attraction given the primary key
            attraction = Attraction.objects.get(pk=pk)
            serializer = AttractionSerializer(attraction, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        # Defining the specific attraction to update
        attraction = Attraction.objects.get(pk=pk)
        # Defining the specific attraction area to update 
        # Gets the new area that has been updated
        area = ParkArea.objects.get(pk=request.data["area_id"])
        # Request data gets the information from the request
        attraction.name = request.data["name"]
        # Setting area of attraction equal to the area_id instance in park area
        attraction.area = area
        attraction.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        
        try:
            attraction = Attraction.objects.get(pk=pk)
            attraction.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Attraction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def list(self, request):
        # Set attractions to all instances 
        attractions = Attraction.objects.all()
        # Get the area depending on what is queried 
        area = self.request.query_params.get('area', None)
        # If there is an area selected it'll filter to only include that specific area 
        if area is not None:
            attractions = attractions.filter(area__id=area)

        serializer = AttractionSerializer(
            attractions, many=True, context={'request': request})

        return Response(serializer.data)