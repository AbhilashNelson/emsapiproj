from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Employee, Department
from datetime import date
from .serializers import EmployeeSerializer

class EmployeeViewSetTest(APITestCase):
    
    def setUp(self):
        # Set up department and employee instances for testing
        self.department = Department.objects.create(DepartmentName="HR")
        self.employee = Employee.objects.create(
            EmployeeName="John Doe",
            Designation="Manager",
            DateOfJoining=date(2020, 1, 15),
            DepartmentId=self.department,
            Contact="1234567890",
            IsActive=True
        )
        self.client = APIClient()
    def test_employee_list(self):
        # Test the list endpoint for fetching all employees
        url = reverse('employee-list')
        response = self.client.get(url)
        
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_employee_detail(self):
        # Test the retrieve endpoint for fetching a single employee
        url = reverse('employee-detail', args=[self.employee.EmployeeId])
        response = self.client.get(url)
        
        serializer = EmployeeSerializer(self.employee)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_employee_create(self):
        # Test the create endpoint for adding a new employee
        url = reverse('employee-list')
        data = {
            "EmployeeName": "Jane Doe",
            "Designation": "Assistant",
            "DateOfJoining": "2021-05-20",
            "Contact": "0987654321",
            "IsActive": True,
            "DepartmentId": self.department.DepartmentId
        }
        response = self.client.post(url, data, format='json')
        
        # Check response and that employee is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.assertEqual(Employee.objects.get(EmployeeName="Jane Doe").Designation, "Assistant")

    def test_employee_update(self):
        # Test the update endpoint to modify an existing employee
        url = reverse('employee-detail', args=[self.employee.EmployeeId])
        data = {
            "EmployeeName": "John Doe",
            "Designation": "Senior Manager",  # Updated designation
            "DateOfJoining": "2020-01-15",
            "Contact": "1234567890",
            "IsActive": True,
            "DepartmentId": self.department.DepartmentId
        }
        response = self.client.put(url, data, format='json')
        
        # Check response and that employee is updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.Designation, "Senior Manager")

    def test_employee_delete(self):
        # Test the delete endpoint for removing an employee
        url = reverse('employee-detail', args=[self.employee.EmployeeId])
        response = self.client.delete(url)
        
        # Check response and that employee is deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

    def test_employee_search(self):
        # Test the search functionality using the search filter
        url = reverse('employee-list') + '?search=Manager'
        response = self.client.get(url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        for employee in response.data:
            self.assertIn("Manager", employee["Designation"])