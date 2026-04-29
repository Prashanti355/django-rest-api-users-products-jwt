import logging
import time
import uuid

logger = logging.getLogger("django")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        request.request_id = request_id

        response = self.get_response(request)

        duration = int((time.time() - start_time) * 1000)

        user = getattr(request, "user", None)
        user_email = user.email if user and user.is_authenticated else "anonymous"

        logger.info(
            f"request_id={request_id} "
            f"method={request.method} "
            f"path={request.path} "
            f"status={response.status_code} "
            f"duration_ms={duration} "
            f"user={user_email}"
        )

        return response
