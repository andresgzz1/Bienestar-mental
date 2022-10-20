#from django.contrib.auth.models import User
from rest_framework import serializers, validators
from .models import User, userStandard


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','email','first_name','last_name','is_client','is_admin','matricula','sexo','phone')

        extra_kwargs = {
            "password": {"write_only": True},
            "matricula" : {
                "required": True, 
                "validators": [
                    validators.UniqueValidator( User.objects.all(), "A user with that matricula already exists")
                ]
            },
            "email":{
                "required": True,
                "validators":[
                    validators.UniqueValidator(
                        User.objects.all(), "A user with that Email already exists"
                    )
                ]
            }

        }
    
    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        
        user = User.objects.create(
            username=username,
            password= password,
            email = email,
            first_name = first_name,
            last_name = last_name,
            is_client=False,
            is_admin=True
        )

        return user
