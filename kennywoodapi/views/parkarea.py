"""Park Areas for Kennywood Amusement Park"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import ParkArea

# Python to JSON
class ParkAreaSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = ParkArea
        # Uses model preestablished park area and gives it a url 
        # Url is fulfilling default route constraints
        url = serializers.HyperlinkedIdentityField(
            view_name='parkarea',
            lookup_field='id'
        )
        # Indicating which fields you want to return for each item when serialization finishes
        fields = ('id', 'url', 'name', 'theme')


class ParkAreas(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ParkArea instance
        """
        newarea = ParkArea()
        newarea.name = request.data["name"]
        newarea.theme = request.data["theme"]
        newarea.save()

        serializer = ParkAreaSerializer(newarea, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        # If the pk doesn't exist in the database, it will throw an exception error
        try:
            # Returns a single park area given the primary key
            area = ParkArea.objects.get(pk=pk)
            serializer = ParkAreaSerializer(area, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
        area = ParkArea.objects.get(pk=pk)
        area.name = request.data["name"]
        area.theme = request.data["theme"]
        area.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park area

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            area = ParkArea.objects.get(pk=pk)
            area.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ParkArea.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        # Data to serialize
        areas = ParkArea.objects.all()
        # Sends the query set of park area objects to serializer
        serializer = ParkAreaSerializer(
            # Many=true is specifying if theres more than one item
            areas, many=True, context={'request': request})
        # Passed to HTTP Response
        return Response(serializer.data)