from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(ModelSerializer):
    """
    Serializer for user registration.
    """
    
    password = CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    
    password2 = CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label="Confirm Password"
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'password2',
            'first_name',
            'last_name',
            'phone',
            'newsletter_consent',
            'marketing_consent',
            'language',
            'currency'
        ]
    
    def validate(self, attrs):
        """Check if password and password2 match."""
        if attrs['password'] != attrs['password2']:
            raise ValidationError({
                "password": "Les mots de passe ne correspondent pas."
            })
        return attrs
    
    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

