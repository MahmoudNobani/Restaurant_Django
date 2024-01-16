from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Employee, PhoneNumber

class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Employee model.

    Attributes:
        Meta:
            model (Employee): The model associated with the serializer.
            fields (list): The fields to be included in the serialized representation.
    """
    class Meta:
        model = Employee
        fields = '__all__'

class PhoneNumberSerializer1(serializers.ModelSerializer):
    """
    Serializer for the PhoneNumber model.
    Attributes:
    - empID as a nested serilizer
        Meta:
            model (PhoneNumber): The model associated with the serializer.
            fields (list): The fields to be included in the serialized representation.
    """
    empID = EmployeeSerializer(required=False)
    class Meta:
        model = PhoneNumber
        fields = '__all__'

class EmpSerWithPhone(serializers.ModelSerializer):
    """
    Serializer for the Employee model with associated PhoneNumbers.

    Includes methods for retrieving and updating associated PhoneNumber instances.
    Attributes:
    - phone_numbers as a nested serilizer
    - number as a custom field for numbers
    - password as a write only field
    - and all other necessicy field in meta
        
    Meta:
        model (Employee): The model associated with the serializer.
        fields (list): The fields to be included in the serialized representation ('pk','username','salary','position','number','email','password','address','phone_numbers').
        read_only_fields (list): Fields that are read-only in the serialized representation ('pk')
    """
    phone_numbers = PhoneNumberSerializer1(many=True, required=False)
    number = serializers.SerializerMethodField('get_phones')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['pk','username','salary','position','number','email','password','address','phone_numbers']
        read_only_fields = ['pk']

    def get_phones(self, obj) -> list:
        """
        Retrieve and return the list of phone numbers objects associated with the Employee.

        Args:
            obj (Employee): The Employee instance for which phone numbers are to be retrieved.

        Returns:
            list: A list of phone numbers objects associated with the Employee.
        """
        p = PhoneNumber.objects.values_list('PhoneNumber', flat=True).filter(empID=obj.pk)
        return p

    def create(self, validated_data):
        """
        Create and return a new Employee instance with associated PhoneNumbers.

        Args:
            validated_data (dict): input data for creating the Employee instance.

        Returns:
            Employee: The newly created Employee instance.
        """
        phone_numbers_data = validated_data.pop('phone_numbers', [])
        validated_data['password'] = make_password(validated_data.get('password'))
        employee = Employee.objects.create(**validated_data)
        self.create_phone_numbers(employee, phone_numbers_data)
        return employee

    def create_phone_numbers(self, employee, phone_numbers_data):
        """
        Create and associate PhoneNumbers with the given Employee instance.

        Args:
            employee (Employee): The Employee instance.
            phone_numbers_data (list): List of phone number data for creation.

        Returns:
            None
        """
        for phone_data in phone_numbers_data:
            x = PhoneNumber.objects.create(empID=employee, PhoneNumber=phone_data["PhoneNumber"])
            x.save()

    def update(self, instance, validated_data):
        """
        Update and return an existing Employee instance with associated PhoneNumbers.

        Args:
            instance (Employee): The existing Employee instance.
            validated_data (dict): input data for updating the Employee instance.

        Returns:
            Employee: The updated Employee instance.
        """
        validated_data.pop('password', None)
        phone_numbers_data = validated_data.pop('phone_numbers', [])
        x = PhoneNumber.objects.filter(empID=instance)
        print(phone_numbers_data)
        j = 0
        if len(phone_numbers_data) > 0 and len(phone_numbers_data) == len(x):
            for i in x:
                i.PhoneNumber = phone_numbers_data[j]["PhoneNumber"]
                i.save()
                j+=1
        
        instance = super().update(instance, validated_data)
        return instance

class PhoneNumberSerializer(serializers.ModelSerializer):
    """
    Serializer for the PhoneNumber model.

    Attributes:
        Meta:
            model (PhoneNumber): The model associated with the serializer.
            fields (list): The fields to be included in the serialized representation ('__all__' for all fields).
    """
    #empID = EmpSerWithPhone(read_only=True,required=False)
    class Meta:
        model = PhoneNumber
        fields = '__all__'

# class EmpSerWithPhone(serializers.ModelSerializer):
#     phone_numbers = PhoneNumberSerializer1(many=True, required=False)
#     pn = serializers.SerializerMethodField('get_phones')

#     class Meta:
#         model = Employee
#         fields = ['pk','name','salary','position','pn','manager','address','phone_numbers']

#     def get_phones(self, obj):
#         # Access obj.phone_numbers to retrieve the phone numbers data
#         p = PhoneNumber.objects.values_list('PhoneNumber', flat=True).filter(empID=obj.pk)
#         return p

#     def create(self, validated_data):
#         phone_numbers_data = validated_data.pop('phone_numbers', [])
#         employee = Employee.objects.create(**validated_data)
#         self.create_phone_numbers(employee, phone_numbers_data)
#         return employee

#     # def update(self, instance, validated_data):
#     #     phone_numbers_data = validated_data.pop('phone_numbers', [])
#     #     instance = super().update(instance, validated_data)
#     #     instance.phone_numbers.all().delete()  # Delete existing phone numbers
#     #     self.create_phone_numbers(instance, phone_numbers_data)
#     #     return instance

#     def create_phone_numbers(self, employee, phone_numbers_data):
#         for phone_data in phone_numbers_data:
#             x = PhoneNumber.objects.create(empID=employee, PhoneNumber=phone_data["PhoneNumber"])
#             x.save()
