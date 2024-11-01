from rest_framework import viewsets, permissions, filters
from .models import Employee, Department, UserDetails
from .serializers import EmployeeSerializer, DepartmentSerializer
from .serializers import UserDetailsSerializer, SignupSerializer
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

class LoginAPIView(APIView):
    """This api will handle login and return token for authenticate user."""
    permission_classes = [AllowAny]  # Allow unauthenticated access
    def post(self,request):
            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid():
                    username = serializer.validated_data["username"]
                    password = serializer.validated_data["password"]
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        """We are reterving the token for authenticated user."""
                        token = Token.objects.get(user=user)
                        response = {
                               "status": status.HTTP_200_OK,
                               "message": "success",
                               "username": user.username,
                               "role": user.groups.all()[0].id if user.groups.exists() else None, 
                               "data": {
                                       "Token" : token.key
                                       }
                               }
                        return Response(response, status = status.HTTP_200_OK)
                    else :
                        response = {
                               "status": status.HTTP_401_UNAUTHORIZED,
                               "message": "Invalid Email or Password",
                               }
                        return Response(response, status = status.HTTP_401_UNAUTHORIZED)
            response = {
                 "status": status.HTTP_400_BAD_REQUEST,
                 "message": "bad request",
                 "data": serializer.errors
                 }
            return Response(response, status = status.HTTP_400_BAD_REQUEST)

class SignupAPIView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access
    
    """This api will handle signup"""
    def post(self,request):
            serializer = SignupSerializer(data = request.data)
            if serializer.is_valid():
                    """If the validation success, it will created a new user."""
                    user = serializer.save()
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        "user_id": user.id,
                        "username": user.username,
                        "token": token.key,
                        "role": user.groups.all()[0].id if user.groups.exists() else None
                    }, status=status.HTTP_201_CREATED)

            else:
                res = { 'status' : status.HTTP_400_BAD_REQUEST, 'data' : serializer.errors }
                return Response(res, status = status.HTTP_400_BAD_REQUEST)

# Create your views here.
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    #permission_classes = [IsAuthenticated]  #uncomment to allow only logged in users

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['EmployeeName','Designation']
    permission_classes = []
    #permission_classes = [permissions.IsAuthenticated] #uncomment to allow only logged in users

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = []
    #permission_classes = [permissions.IsAuthenticated] #uncomment to allow only logged in users

class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = []
    #permission_classes = [permissions.IsAuthenticated] #uncomment to allow only logged in users
