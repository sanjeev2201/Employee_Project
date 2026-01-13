from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and 'Super Admin' in [role.name for role in request.user.roles.all()]

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and 'Admin' in [role.name for role in request.user.roles.all()]

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and 'Manager' in [role.name for role in request.user.roles.all()]

class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and 'Member' in [role.name for role in request.user.roles.all()]

#organization
class CanRetrieveOrListOrganizations(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class CanUpdateOrganization(BasePermission):
    def has_object_permission(self, request, view, obj):
        if 'Super Admin' in [role.name for role in request.user.roles.all()]:
            return True
        if 'Admin' in [role.name for role in request.user.roles.all()] and obj == request.user.organization:
            return True
        return False

class CanDeleteOrganization(BasePermission):
    def has_object_permission(self, request, view, obj):
        if 'Super Admin' in [role.name for role in request.user.roles.all()]:
            return True
        if 'Admin' in [role.name for role in request.user.roles.all()] and obj == request.user.organization:
            return True
        return False

#role
class CanRetrieveOrListRoles(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class CanCreateRole(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            # Super Admin can create roles in any organization
            if 'Super Admin' in [role.name for role in request.user.roles.all()]:
                return True
            # Admin can create roles in their own organization
            if 'Admin' in [role.name for role in request.user.roles.all()]:
                # Extract organization ID from request data
                organization_id = request.data.get('organization', None)
                return organization_id and int(organization_id) == request.user.organization.id
        return False

class CanUpdateRole(BasePermission):
    def has_object_permission(self, request, view, obj):
        if 'Super Admin' in [role.name for role in request.user.roles.all()]:
            return True
        if 'Admin' in [role.name for role in request.user.roles.all()] and obj.organization == request.user.organization:
            return True
        return False

class CanDeleteRole(BasePermission):
    def has_object_permission(self, request, view, obj):
        if 'Super Admin' in [role.name for role in request.user.roles.all()]:
            return True
        if 'Admin' in [role.name for role in request.user.roles.all()] and obj.organization == request.user.organization:
            return True
        return False
    
    
#user

class CanCreateUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if 'Super Admin' in [role.name for role in request.user.roles.all()]:
                return True
            if 'Admin' in [role.name for role in request.user.roles.all()]:
                organization_id = request.data.get('organization', None)
                return organization_id and int(organization_id) == request.user.organization.id
        return False

class CanRetrieveUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if 'Super Admin' in [role.name for role in request.user.roles.all()]:
            return True
        if 'Admin' in [role.name for role in request.user.roles.all()] and obj.organization == request.user.organization:
            return True
        if 'Manager' in [role.name for role in request.user.roles.all()] and obj.organization == request.user.organization:
            return True
        if 'Member' in [role.name for role in request.user.roles.all()] and obj == request.user:
            return True
        return False

class CanUpdateUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if 'Super Admin' in [role.name for role in request.user.roles.all()]:
            return True
        if 'Admin' in [role.name for role in request.user.roles.all()] and obj.organization == request.user.organization:
            return True
        if 'Manager' in [role.name for role in request.user.roles.all()] and obj.organization == request.user.organization:
            return True
        if 'Member' in [role.name for role in request.user.roles.all()] and obj == request.user:
            return True
        return False

class CanDeleteUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if 'Super Admin' in [role.name for role in request.user.roles.all()]:
            return True
        if 'Admin' in [role.name for role in request.user.roles.all()] and obj.organization == request.user.organization:
            return True
        if 'Manager' in [role.name for role in request.user.roles.all()] and obj.organization == request.user.organization:
            return True
        return False

class CanListUsers(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            if 'Super Admin' in [role.name for role in request.user.roles.all()]:
                return True
            if 'Admin' in [role.name for role in request.user.roles.all()]:
                return True
            if 'Manager' in [role.name for role in request.user.roles.all()]:
                return True
        return False