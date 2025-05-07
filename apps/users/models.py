from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now


# Create your models here.
class FbUserManager(BaseUserManager):
    def create_user(
        self,
        email,
        password,
        first_name=None,
        last_name=None,
        date_of_birth=None,
        gender=None,
    ):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        email,
        password,
        first_name=None,
        last_name=None,
        date_of_birth=None,
        gender=None,
    ):
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class FbUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField(null=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="images/", default=None)
    cover_photo = models.ImageField(null=True, blank=True, upload_to="images/")
    gender = models.CharField(max_length=6, null=True)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254,unique=True)
    password = models.CharField(max_length=100)
    bio = models.CharField(max_length=250, null=True,blank=True)
    date_joined = models.DateTimeField(default=now)
    last_login = models.DateTimeField(default=now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = FbUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.first_name == None and self.last_name == None:
            super().save(*args, **kwargs)
        else:
            self.first_name = self.first_name.capitalize()
            self.last_name = self.last_name.capitalize()
            super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    
    class Meta:
        app_label = 'users'