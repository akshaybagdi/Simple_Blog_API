from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def validate_payload(required_keys):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            data = request.data
            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                return Response({"error": f"Missing keys: {', '.join(missing_keys)}"}, status=status.HTTP_400_BAD_REQUEST)
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator

#
# # Custom method decorator for validating payloads with required fields
# def validate_post_payload(required_fields):  # Decorator definition
#     """
#     Validates if the required fields are present in the payload.
#     :param required_fields: List of fields to check in the payload.
#     """
#
#     def decorator(view_func):  # Inner function to wrap the view
#         @wraps(view_func)  # Preserves the original function's metadata
#         def wrapped(self, request, *args, **kwargs):
#             print("Decorator: Payload received:", request.data)  # Debug statements
#             payload = request.data  # Get the payload from the request
#             missing_fields = [field for field in required_fields if field not in payload]  # Find missing fields
#             if missing_fields:  # If any fields are missing, return an error response
#                 return Response(
#                     {"Error": f"Missing required fields: {', '.join(missing_fields)}"},
#                     status=status.HTTP_400_BAD_REQUEST)
#             return view_func(self, request, *args, **kwargs)  # Call the original view function if valid
#
#         return wrapped
#
#     return decorator
