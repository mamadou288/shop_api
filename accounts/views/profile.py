from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from ..serializers import UserSerializer


class ProfileView(RetrieveUpdateAPIView):
    """
    GET /api/auth/profile/ - Get authenticated user's profile
    PATCH /api/auth/profile/ - Update authenticated user's profile
    
    Requires Bearer token in Authorization header.
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        """Return the authenticated user."""
        return self.request.user

