from rest_framework import permissions
import re

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
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
