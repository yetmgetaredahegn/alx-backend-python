from rest_framework import permissions 

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PATCH',"PUT","DELETE"]:
            return True
        return bool(request.user.is_authenticated)