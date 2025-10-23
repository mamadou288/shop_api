from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(ModelSerializer):
    """
    Serializer for User model - Display user data.
    """
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'phone',
            'is_admin',
            'newsletter_consent',
            'marketing_consent',
            'date_of_birth',
            'language',
            'currency',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

