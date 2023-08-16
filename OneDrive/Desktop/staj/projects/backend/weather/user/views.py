from rest_framework.viewsets import ModelViewSet
# from .base_view import BaseViewSet
from rest_framework.permissions import AllowAny

from .serializer import UserProfileSerializer
from .models import User

from django.shortcuts import get_object_or_404

from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from .serializer import UserSerializer
from rest_framework import status


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        print('0')
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')

        if not username_or_email or not password:
            return Response({'error': 'Please provide both username/email and password.'}, status=400)

        if '@' in username_or_email:
            user = authenticate( email=username_or_email, password=password)
            print(user, '1')
        else:
            user = authenticate( username=username_or_email, password=password)
            return Response({'user':user}, status=200)
            print(user, '2')
        print('3')
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'message': 'Login successful.'}, status=200)
        else:
            return Response({'error': 'Invalid credentialsss.'}, status=401)

#
# class LoginView(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         return Response({'message':'ok'},status=status.HTTP_200_OK)
#
#         if user:
#             login(request, user)
#             print("User authenticated and logged in:", user)
#             return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#         else:
#             print("Authentication failed for user:", username)
#             return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class UserProfileViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    @classmethod
    def use_for(cls, method):
        return cls.as_view({'post': method})

    def get_object(self):
        queryset = self.get_queryset()
        data = self.request.data
        _id = data.get("id")
        if _id is None:
            raise APIException("You should pass id value for retrieve object.")

        obj = get_object_or_404(queryset, user__id=_id)
        return obj

    def bulk_update(self, request, *args, **kwargs):
        data = request.data
        ids = []
        queryset = self.get_queryset()
        for datum in data:
            _id = datum.get('id')
            if _id is not None:
                ids.append(_id)
                obj = get_object_or_404(queryset, user__id=_id)
                serializer = self.get_serializer(obj, data=datum)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
        instances = queryset.filter(id__in=ids)
        serializer = self.get_serializer(instances, many=True)
        return Response(serializer.data)
