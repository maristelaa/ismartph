from django.shortcuts import redirect
from django.contrib import auth
import firebase_admin
from firebase_admin import auth as firebase_auth

class FirebaseAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/dashboard' and not request.user.is_authenticated:
            # Redirect users who are not authenticated and trying to access 'postSign' to the index page
            return redirect('index')  # Replace 'index' with the actual URL name for your index page

        response = self.get_response(request)
        return response

        
class LogoutCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == '/signOut':
            # Store the current path in the session
            request.session['current_path'] = request.path

            # Redirect to a page (e.g., index) without performing logout
            return redirect(request, 'ismartproj/welcome.html')  # Replace 'index' with the actual URL name for your welcome page

        response = self.get_response(request)
        return response