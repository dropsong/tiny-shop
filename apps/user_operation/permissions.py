from rest_framework import permissions
import re

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # print('*'*30)
        if request.method in permissions.SAFE_METHODS:
            return True

        cookie_header = request.headers.get('Cookie', '')
        match = re.search(r'name=([^;]+)', cookie_header)
        uname = ''
        if match:
            name_value = match.group(1)
            uname = name_value
        else:
            return False
        
        return str(obj) == str(uname)
