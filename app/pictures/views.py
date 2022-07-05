from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Picture
from .serializers import PictureSerializer

class PictureListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        pictures = Picture.objects.filter(user = request.user.id)
        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'image': request.data.get('image'), 
            'user': request.user.id
        }
        serializer = PictureSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PictureDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, picture_id, user_id):
        '''
        Helper method to get the object with given picture_id, and user_id
        '''
        try:
            return Picture.objects.get(id=picture_id, user = user_id)
        except Picture.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, picture_id, *args, **kwargs):
        '''
        Retrieves the Picture with given picture_id
        '''
        picture_instance = self.get_object(picture_id, request.user.id)
        if not picture_instance:
            return Response(
                {"res": "Object with picture id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PictureSerializer(picture_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, picture_id, *args, **kwargs):
        '''
        Updates the Picture with given id if exists
        '''
        picture_instance = self.get_object(picture_id, request.user.id)
        if not picture_instance:
            return Response(
                {"res": "Picture with this id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'image': request.data.get('image'), 
            'user': request.user.id
        }
        serializer = PictureSerializer(instance=picture_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, picture_id, *args, **kwargs):
        '''
        Deletes the Picture item with given id if exists
        '''
        picture_instance = self.get_object(picture_id, request.user.id)
        if not picture_instance:
            return Response(
                {"res": "Picture with this id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        picture_instance.delete()
        return Response(
            {"res": "Picture deleted!"},
            status=status.HTTP_200_OK
        )

class PictureAdminApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        '''
        Delete all pictures in database
        '''
        if request.user.is_staff:
            pictures = Picture.objects.all()
            pics_len = pictures.count()
            for pic in pictures:
                pic.delete()
            return Response(
                {"res": f"{pics_len} pictures deleted!"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"res": "You dont have permissions to use this function!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )