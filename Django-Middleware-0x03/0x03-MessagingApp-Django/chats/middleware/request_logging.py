import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Use the logger defined in settings.py
        self.logger = logging.getLogger("middleware_logger")

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_entry)  # Logs to requests.log file

        response = self.get_response(request)
        return response

