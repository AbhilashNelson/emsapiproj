from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'userdetails', views.UserDetailsViewSet)
router.register(r'users', views.UserViewSet)

#RegisterUser is an APIView, not a ViewSet. 
# Therefore, it should be added to the URL patterns directly using Django’s path()
urlpatterns = [
    path("signup/", views.SignupAPIView.as_view(), name="user-signup"),
    path("login/", views.LoginAPIView.as_view(), name="user-login"),
]

# Include router URLs as well
urlpatterns += router.urls

