from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import AbstractUser

class CustomUserManager(BaseUserManager):

    """
    Custom manager for the Employee model.

    This manager provides methods for creating regular users and superusers.
    It extends the BaseUserManager class.

    Methods:
    - create_user(username, email, password=None, **extra_fields): Creates a regular user.
    - create_superuser(username, email, password=None, **extra_fields): Creates a superuser.

    Args:
    - BaseUserManager: The base manager class for user models in Django.
    """

    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given username, email, and password.

        Args:
        - username (str): The username for the new user.
        - email (str): The email address for the new user.
        - password (str): The password for the new user. Default is None.
        - **extra_fields: Additional fields for the new user.

        Returns:
        - User: The newly created regular user.
        """
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given username, email, and password.

        Args:
        - username (str): The username for the new superuser.
        - email (str): The email address for the new superuser.
        - password (str): The password for the new superuser. Default is None.
        - **extra_fields: Additional fields for the new superuser.

        Returns:
        - User: The newly created superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class Employee(AbstractUser):
    """
    Custom user model for representing employees with the help of AbstractUser so we can use this employee for authentication
    and admin inteface.

    Attributes:
    - name (str): The name of the employee. //no need, there is already first and last name
    - salary (float): The salary of the employee.
    - position (str): The position or job title of the employee.
    - address (str): The address of the employee.

    Inherits from:
    - AbstractUser: The base user model provided by Django.
    """
    name = models.CharField(max_length=100)
    salary = models.FloatField()
    position = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email','salary', 'position', 'address']

    def __str__(self):
        """
        Return the username as the string representation of the employee.

        Returns:
        - str: The username of the employee.
        """
        return self.username

class PhoneNumber(models.Model):
    """
    Model for representing phone numbers associated with employees.

    Attributes:
    - empID (Employee): The employee associated with the phone number.
    - PhoneNumber (int): The phone number.

    """
    empID = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='phone',blank=True)
    PhoneNumber = models.IntegerField()

    def __str__(self) -> str:
        """
        Return the string representation of the phone number.

        Returns:
        - str: The phone number as a string.
        """
        return str(self.PhoneNumber)
    


# Create your models here.
# class Employee(models.Model):
#     name = models.CharField(max_length=100)
#     salary = models.FloatField()
#     position = models.CharField(max_length=100)
#     address = models.CharField(max_length=100)
#     manager = models.BooleanField(default=False)

#     def __str__(self) -> str:
#         return self.name
    
# class Employee(AbstractUser):
#     name = models.CharField(max_length=100,unique=True)
#     position = models.CharField(max_length=100)
#     address = models.CharField(max_length=100)
#     salary = models.FloatField()
    
#     USERNAME_FIELD = 'name'
#     REQUIRED_FIELDS = ['position', 'address', 'salary']

#     def __str__(self) -> str:
#         return self.name
    
#     def save(self, *args, **kwargs):
#         if self.manager:
#             self.is_superuser = True
#             self.is_staff = True
#         super(Employee, self).save(*args, **kwargs)

# class CustomUserManager(BaseUserManager):
#     def create_user(self, name, password=None, **extra_fields):
#         if not name:
#             raise ValueError('The name field must be set')
#         user = self.model(name=name, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, name, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(name, password, **extra_fields)

# class Employee(AbstractBaseUser, PermissionsMixin):
#     name = models.CharField(max_length=100,unique=True)
#     salary = models.FloatField()
#     position = models.CharField(max_length=100)
#     address = models.CharField(max_length=100)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'name'
#     REQUIRED_FIELDS = ['salary', 'position', 'address']

#     def __str__(self):
#         return self.name

# from rest_framework.authtoken.models import Token
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def TokenCreate(sender, instance, created, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
    
#general idea of token creation immediatly after user is created 
    
#this is for normal token not a jwt token:
#That's the point of JWTs, they do not need server-side storage. All the information is baked into the token itself, 
#which is signed with a secret only the server has (is supposed to have, if you do it properly without security vulnerability). 
#The server reads the information in the JWT and confirms that it has been signed with the secret, 
#something only it itself should have. If that succeeds, it trusts the information contained in the JWT. 
#Hence it doesn't need to look up anything in any database.