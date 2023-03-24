from django.utils.deprecation import MiddlewareMixin


class DisableBrowserBackButtonMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check if the user has just logged out
        if request.user.is_authenticated is False:
            # Set the Cache-Control header to no-cache, no-store
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
        return response
