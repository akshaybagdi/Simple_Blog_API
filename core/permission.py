from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class UserPermission(permissions.BasePermission):
    message = "Editing post is restricted to the author only"
    def has_object_permission(self, request, view, obj):
        print(f"Request user: {request.user}, Post author: {obj.author}")
        if not request.user or not request.user.is_authenticated:
            return False

        # Log user and author details for debugging
        print(f"Request user: {request.user} (ID: {request.user.id})")
        print(f"Post author: {obj.author} (ID: {obj.author.id})")
        if request.method in SAFE_METHODS:
            return True
        return obj.author.id == request.user.id
