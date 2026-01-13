from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,SAFE_METHODS
from .models import Organization, Role, User
from .serializer import OrganizationSerializer, RoleSerializer, UserListSerializer, UserSerializer
from .permissions import IsSuperAdmin, IsAdmin, IsManager, IsMember, CanRetrieveOrListOrganizations, CanUpdateOrganization, CanDeleteOrganization,CanRetrieveOrListRoles, CanCreateRole, CanUpdateRole, CanDeleteRole,CanCreateUser, CanRetrieveUser, CanUpdateUser, CanDeleteUser, CanListUsers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permission() for permission in [IsAuthenticated, CanRetrieveOrListOrganizations , IsSuperAdmin]]
        if self.action == 'update':
            return [permission() for permission in [IsAuthenticated, CanUpdateOrganization]]
        if self.action == 'destroy':
            return [permission() for permission in [IsAuthenticated, CanDeleteOrganization]]
        return super().get_permissions()

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permission() for permission in [IsAuthenticated, CanRetrieveOrListRoles]]
        if self.action == 'create':
            return [permission() for permission in [IsAuthenticated, CanCreateRole]]
        if self.action in ['update', 'partial_update']:
            return [permission() for permission in [IsAuthenticated, CanUpdateRole]]
        if self.action == 'destroy':
            return [permission() for permission in [IsAuthenticated, CanDeleteRole]]
        return super().get_permissions()
   
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action == 'create':
            return [permission() for permission in [IsAuthenticated, CanCreateUser]]
        if self.action in ['retrieve', 'list']:
            return [permission() for permission in [IsAuthenticated, CanRetrieveUser if self.action == 'retrieve' else CanListUsers]]
        if self.action in ['update', 'partial_update']:
            return [permission() for permission in [IsAuthenticated, CanUpdateUser]]
        if self.action == 'destroy':
            return [permission() for permission in [IsAuthenticated, CanDeleteUser]]
        return super().get_permissions()
    
class RegisterView(APIView):
    """
    List all users, or create a new users.
    """

    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        # print(serializer.data)
        return Response({'data' :serializer.data})

    def post(self, request, format=None):
        payload = request.data
        roleid = payload.get('roles')
        # print("Role ID:", roleid)
        try:
            for role in roleid:
                if role==1:
                    payload['is_superuser']=True
                    payload['is_staff']=True
                    serializer = UserSerializer(data=payload)
                    if serializer.is_valid():
                        print("Valid data")
                        serializer.save()
                        print(serializer.data)
                        # return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                if role==2:
                    payload['is_staff']=True
                    serializer = UserSerializer(data=payload)
                    if serializer.is_valid():
                        print("Valid data")
                        serializer.save()
                        print(serializer.data)
                if role==3:
                    payload['is_staff']=False
                    serializer = UserSerializer(data=payload)
                    if serializer.is_valid():
                        print("Valid data")
                        # serializer.save()
                        print(serializer.data)
                if role==4:
                    payload['is_staff']=False
                    serializer = UserSerializer(data=payload)
                    if serializer.is_valid():
                        print("Valid data")
                        serializer.save()
                        print(serializer.data)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error:", str(e))
            return Response({"Error:", str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RoleView(APIView):
    """
    List all roles, or create a new role.
    """

    def get(self, request, format=None):
        snippets = Role.objects.all()
        serializer = RoleSerializer(snippets, many=True)
        # print(serializer.data)
        return Response(serializer.data)

    def post(self, request, format=None):
        payload = request.data
        print(payload)
        serializer = RoleSerializer(data=payload)
        if serializer.is_valid():
            # print("Valid data")
            # serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class OrganizationView(APIView):
    """
    List all Organization, or create a new Organization.
    """

    def get(self, request, format=None):
        organization = Organization.objects.all()
        serializer = OrganizationSerializer(organization, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request, format=None):
        payload = request.data
        print(payload)
        serializer = OrganizationSerializer(data=payload)
        if serializer.is_valid():
            print("Valid data")
            # serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DashboardView(APIView):
    """
        Dashboard view to provide summary statistics.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        total_users = User.objects.count()
        total_organizations = Organization.objects.count()
        total_roles = Role.objects.count()
        users = User.objects.select_related('organization').prefetch_related('roles').all()
        print([role.name for role in request.user.roles.all()])
        userroleslist = [role.name for role in request.user.roles.all()]
        for permission in userroleslist:
            if permission=='Super Admin':
                users = users.filter(roles__name="Super Admin")
                serializer = UserListSerializer(users, many=True)
                data = {
                        'total_users': total_users,
                        'total_organizations': total_organizations,
                        'total_roles': total_roles,
                        'users': serializer.data
                        }
                return Response(data)
            if permission=='Admin':
                users = users.filter(roles__name="Admin")
                serializer = UserListSerializer(users, many=True)
                data = {
                        'total_users': total_users,
                        'total_organizations': total_organizations,
                        'total_roles': total_roles,
                        'users': serializer.data
                        }
                return Response(data)
            if permission=='Manager':
                users = users.filter(roles__name="Manager")
                serializer = UserListSerializer(users, many=True)
                data = {
                        'total_users': total_users,
                        'total_organizations': total_organizations,
                        'total_roles': total_roles,
                        'users': serializer.data
                        }
                return Response(data)
            if permission=='Member':
                users = users.filter(roles__name="Member")
                serializer = UserListSerializer(users, many=True)
                data = {
                        'total_users': total_users,
                        'total_organizations': total_organizations,
                        'total_roles': total_roles,
                        'users': serializer.data
                        }
                return Response(data)
        serializer = UserListSerializer(users, many=True)
        # return Response(serializer.data)


        data = {
                'total_users': total_users,
                'total_organizations': total_organizations,
                'total_roles': total_roles,
                'users': serializer.data
                }
        return Response(data)
    
class ResetPasswordAPIView(APIView):
    # permission_classes = [IsAdmin]
    def post(self, request):
        new_password = request.data.get("password")
        email = request.data.get("email")
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        print("Password reset successfully")
        return Response({"message": "Password reset successfully"})
