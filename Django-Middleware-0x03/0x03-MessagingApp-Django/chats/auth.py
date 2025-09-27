from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Extend JWTAuthentication if needed later (for logging, etc.)
    """
    pass
