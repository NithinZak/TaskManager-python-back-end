from rest_framework import generics
from . import serializers 
from . import models
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated





# User authentication --------------------------------------------------

class RegistrationView(generics.CreateAPIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'email': user.email,
          
        })
    
class UserLoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
# -----------------------------------------------------------------------------------------

# API for creating listing and searching of the Task

class TaskList(generics.ListCreateAPIView):
    serializer_class = serializers.TaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user 
        return models.MdlTask.objects.filter(user=user) 

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except APIException as e:
            return Response(
                {"error": "An error occurred while processing your request: " + str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred: " + str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, *args, **kwargs):
        try:
            request.data['user'] = request.user.id
            return super().post(request, *args, **kwargs)
        except APIException as e:
            return Response(
                {"error": "An error occurred while creating the task: " + str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred: " + str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# API for Detail view and Deletion of Task

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        user = self.request.user 
        return models.MdlTask.objects.filter(user=user) 

    def handle_exception(self, exc):
        if isinstance(exc, NotFound):
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return self.handle_exception(e)

    def put(self, request, *args, **kwargs):
        try:
            return super().put(request, *args, **kwargs)
        except Exception as e:
            return self.handle_exception(e)

    def patch(self, request, *args, **kwargs):
        try:
            return super().patch(request, *args, **kwargs)
        except Exception as e:
            return self.handle_exception(e)

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            return self.handle_exception(e)

#API for listing Tasks respect to its status
class TaskListByStatus(generics.ListAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        status_param = self.kwargs.get('status')
        queryset = models.MdlTask.objects.filter(user=self.request.user)

        if status_param.lower() in ['true', 'false']:
            status_bool = status_param.lower() == 'true'
            queryset = queryset.filter(status=status_bool)
        else:
          
            raise APIException("Invalid status parameter. Must be 'true' or 'false'.")
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except ValueError as e:
          
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:

            return Response({"error": "An unexpected error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    





    




