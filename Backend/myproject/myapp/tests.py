from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Organization, Role, User
# import pdb

class UserManagementTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create Organizations
        self.org1 = Organization.objects.create(name='Org1', description='Test Organization 1')
        self.org2 = Organization.objects.create(name='Org2', description='Test Organization 2')
        # pdb.set_trace()
        # breakpoint()
        # Create Roles
        self.super_admin_role = Role.objects.create(name='Super Admin', description='Super Admin Role', organization=self.org1)
        self.admin_role = Role.objects.create(name='Admin', description='Admin Role', organization=self.org1)
        self.manager_role = Role.objects.create(name='Manager', description='Manager Role', organization=self.org1)
        self.member_role = Role.objects.create(name='Member', description='Member Role', organization=self.org1)

        # Create Users
        self.super_admin = User.objects.create(username='superadmin',email='superadmin@gmail.com',password='superadmin123',organization=self.org1)
        self.super_admin.roles.add(self.super_admin_role)
        
        self.admin = User.objects.create(username='admin', email='admin@example.com',password='admin123', organization=self.org1)
        self.admin.roles.add(self.admin_role)
        
        self.manager = User.objects.create(username='manager', email='manager@example.com', organization=self.org1)
        self.manager.roles.add(self.manager_role)
        
        self.member = User.objects.create(username='member', email='member@example.com', organization=self.org1)
        self.member.roles.add(self.member_role)
        
        self.user2 = User.objects.create(username='user2', email='user2@example.com', organization=self.org2)
        self.user2.roles.add(self.member_role)

    def test_create_user_as_super_admin(self):
        self.client.force_authenticate(user=self.super_admin)
        data = {
                "username": "new_user",
                "email": "new_user@example.com",
                "password":"test123",
                "organization": self.org1.id,
                "roles": [self.member_role.id]
                }
        response = self.client.post(reverse('user-list'), data)
        # print('line number 47 :' ,response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_as_admin_in_own_organization(self):
        self.client.force_authenticate(user=self.admin)
        data = {
                    "username": "new_user",
                    "email": "new_user@example.com",
                    "password":"test123",
                    "organization": self.org1.id,
                    "roles": [self.member_role.id]
                }
        response = self.client.post(reverse('user-list'), data)
        # print('line number 60 :' ,response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_as_admin_in_other_organization(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "username": "new_user",
            "email": "new_user@example.com",
            "organization": self.org2.id,
            "roles": [self.member_role.id]
        }
        response = self.client.post(reverse('user-list'), data)
        # print('line number 72 :' ,response.status_code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_as_manager(self):
        self.client.force_authenticate(user=self.manager)
        data = {
            "username": "new_user",
            "email": "new_user@example.com",
            "organization": self.org1.id,
            "roles": [self.member_role.id]
        }
        response = self.client.post(reverse('user-list'), data)
        # print('line number 84 :' ,response.status_code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_as_super_admin(self):
        self.client.force_authenticate(user=self.super_admin)
        response = self.client.get(reverse('user-detail', args=[self.admin.id]))
        # print('line number 90 :' ,response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_as_admin_in_own_organization(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('user-detail', args=[self.member.id]))
        # print('line number 96 :' ,response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_as_admin_in_other_organization(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('user-detail', args=[self.user2.id]))
        # print('line number 102 :' ,response.status_code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_as_manager_in_own_organization(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(reverse('user-detail', args=[self.member.id]))
        # print('line number 108 :' ,response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_as_manager_in_other_organization(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(reverse('user-detail', args=[self.user2.id]))
        # print('line number 114 :' ,response.status_code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_own_user_as_member(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.get(reverse('user-detail', args=[self.member.id]))
        # print('line number 120 :' ,response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_other_user_as_member(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.get(reverse('user-detail', args=[self.admin.id]))
        # print('line number 120 :' ,response.status_code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
