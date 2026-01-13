from rest_framework import serializers
from .models import Organization, Role, User

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField( write_only=True,  required=True, style={'input_type': 'password'} )
    roles = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(),  many=True )
    class Meta:
        model = User
        fields = ['id', 'username','email','organization','roles','password','is_active', 'is_staff', 'is_superuser']
    def create(self, validated_data):
        roles = validated_data.pop('roles', [])  
        password = validated_data.pop('password')   
        user = User(**validated_data)
        user.set_password(password)  
        user.save()
        user.roles.set(roles)
        return user
class UserListSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'organization', 'roles']