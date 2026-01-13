from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    organization = models.ForeignKey(
        Organization, related_name='roles', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, username, organization, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            organization=organization,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        organization, _ = Organization.objects.get_or_create(
            name="Default Org",
            defaults={"description": "Default organization"}
        )

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        user = self.create_user(
            email=email,
            username=username,
            organization=organization,
            password=password,
            **extra_fields
        )

        role, _ = Role.objects.get_or_create(
            name="Super Admin",
            organization=organization,
            defaults={"description": "Super admin role"}
        )

        user.roles.add(role)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    organization = models.ForeignKey(Organization, related_name='users', on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role, related_name='users', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email

