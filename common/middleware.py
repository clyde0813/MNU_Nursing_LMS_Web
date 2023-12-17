from django.http import HttpResponseForbidden
from models.models import *
from common.models import *


class PathAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the path from the request
        response = self.get_response(request)
        path = request.path_info

        if path == "/":
            return response

        # Extract the role ('p' or 's') and id from the path
        try:
            role, subject_id = path.split('/')[1:3]
        except ValueError:
            # Invalid path format, do something (e.g., raise an exception)
            return HttpResponseForbidden("Invalid path format")

        if role not in ['p', 's']:
            return response

        # Check the role and id against your authorization logic
        if role == 'p':
            # Check if the user has professor permissions for the specified id
            if not has_professor_permission(request.user):
                return HttpResponseForbidden("Permission denied")
        elif role == 's':
            # Check if the user has student permissions for the specified id
            if not has_student_permission(request.user):
                return HttpResponseForbidden("Permission denied")

        # Continue with the request
        return response


def has_professor_permission(user):
    if user.profile.group.name == "professor":
        return True


def has_student_permission(user):
    if user.profile.group.name == "student":
        return True
