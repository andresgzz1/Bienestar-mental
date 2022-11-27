#from django.contrib.auth.models import User
from rest_framework import serializers, validators
from .models import User, userStandard


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name',
<<<<<<< HEAD
                  'is_client', 'is_admin', 'matricula', 'sexo', 'phone')
=======
                  'is_client', 'is_admin', 'sexo', 'phone')
>>>>>>> origin

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "Ya hay un usuario con el email ingresado"
                    )
                ]
            }

        }

    def create(self, validated_data):
        # matricula = validated_data.get('matricula') #añadi matricula para test
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        user = User.objects.create(
            # matricula=matricula, #matricula añadida
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_client=False,
            is_admin=True
        )

        return user
