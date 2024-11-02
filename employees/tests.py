import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Employee

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def employee_data():
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "department": "Engineering",
        "role": "Developer"
    }

@pytest.fixture
def create_employee(employee_data):
    employee = Employee.objects.create(**employee_data)
    return employee

@pytest.fixture
def auth_token(api_client, django_user_model):
    user = django_user_model.objects.create_user(username="testuser", password="testpass")
    response = api_client.post(reverse('token_obtain_pair'), {"username": "testuser", "password": "testpass"})
    return response.data['access']

@pytest.mark.django_db
def test_create_employee(api_client, employee_data, auth_token):
    # Test successful employee creation
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.post(reverse('employee-list-create'), data=employee_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == employee_data['name']

@pytest.mark.django_db
def test_create_employee_missing_field(api_client, auth_token):
    # Test creation with missing required field
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    invalid_data = {"email": "missing.name@example.com"}
    response = api_client.post(reverse('employee-list-create'), data=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data

@pytest.mark.django_db
def test_create_employee_duplicate_email(api_client, employee_data, auth_token, create_employee):
    # Test creating employee with duplicate email
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.post(reverse('employee-list-create'), data=employee_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data

@pytest.mark.django_db
def test_list_employees(api_client, create_employee, auth_token):
    # Test listing all employees
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.get(reverse('employee-list-create'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) >= 1

@pytest.mark.django_db
def test_filter_employees_by_department(api_client, create_employee, auth_token):
    # Test filtering employees by department
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.get(reverse('employee-list-create'), {'department': 'Engineering'})
    assert response.status_code == status.HTTP_200_OK
    assert all(emp['department'] == 'Engineering' for emp in response.data['results'])

@pytest.mark.django_db
def test_retrieve_employee(api_client, create_employee, auth_token):
    # Test retrieving a single employee by ID
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.get(reverse('employee-detail', args=[create_employee.id]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == create_employee.name

@pytest.mark.django_db
def test_retrieve_nonexistent_employee(api_client, auth_token):
    # Test retrieving an employee that doesn't exist
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.get(reverse('employee-detail', args=[999]))
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_update_employee(api_client, create_employee, auth_token):
    # Test updating an employee's data
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    updated_data = {"name": "Jane Doe"}
    response = api_client.put(reverse('employee-detail', args=[create_employee.id]), data=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == updated_data['name']

@pytest.mark.django_db
def test_partial_update_employee(api_client, create_employee, auth_token):
    # Test partially updating an employee's data
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    partial_data = {"role": "Senior Developer"}
    response = api_client.put(reverse('employee-detail', args=[create_employee.id]), data=partial_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['role'] == partial_data['role']

@pytest.mark.django_db
def test_delete_employee(api_client, create_employee, auth_token):
    # Test deleting an employee
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.delete(reverse('employee-detail', args=[create_employee.id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Employee.objects.filter(id=create_employee.id).exists()

@pytest.mark.django_db
def test_access_unauthenticated(api_client, employee_data):
    # Test accessing endpoints without authentication
    response = api_client.post(reverse('employee-list-create'), data=employee_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_list_employees_pagination(api_client, create_employee, auth_token):
    # Test pagination
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.get(reverse('employee-list-create'), {'page': 1})
    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data
