import time
from django.core.cache import cache
from django.http import JsonResponse
from django.conf import settings

# Throttling Configuration
THROTTLE_RULES = {
    '/api/login/': {'limit': 5, 'period': 60},  # 5 requests per 60 seconds
    '/careers/apply/': {'limit': 3, 'period': 3600}, 
    '/api/data/': {'limit': 10, 'period': 300},  
    # Add more API endpoints and rules here

    #applicant
    '/api/v1/applicant/': {'limit': 10, 'period': 300},
    '/api/v1/applicant/assignment/submission/': {'limit': 5, 'period': 300},
    '/api/v1/applicant/submit/signed/offer/letter/': {'limit': 1, 'period': 300},

    # auth
    '/api/v1/auth/token/refresh/': {'limit': 5, 'period': 300},
    '/api/v1/auth/user/': {'limit': 5, 'period': 300},
    '/api/v1/auth/user/token/verify/': {'limit': 5, 'period': 300},
    '/api/v1/auth/user/password/reset/request/': {'limit': 5, 'period': 300},
    '/api/v1/auth/user/password/reset/confirm/': {'limit': 5, 'period': 300},
    '/api/v1/auth/user/password/reset/verify/': {'limit': 5, 'period': 300},
    '/api/v1/auth/user/password/change/': {'limit': 5, 'period': 300},
    '/api/v1/auth/user/register/': {'limit': 2, 'period': 300},
    '/api/v1/auth/user/list/': {'limit': 5, 'period': 300},
    '/api/v1/auth/user/login/': {'limit': 2, 'period': 300},
    '/api/v1/auth/user/logout/': {'limit': 5, 'period': 300},

    #company
    '/api/v1/company/api/company': {'limit': 5, 'period': 300},


    #job
    '/api/v1/job/': {'limit': 5, 'period': 300},
    'api/v1/job/applicant/template/': {'limit': 5, 'period': 300},
    'api/v1/job/applicant/template/<uuid:pk>/': {'limit': 5, 'period': 300},
    'api/v1/job/assignment/template/': {'limit': 5, 'period': 300},
    'api/v1/job/create/': {'limit': 5, 'period': 300},
    'api/v1/job/list/': {'limit': 5, 'period': 300},
    'api/v1/job/offer/letter': {'limit': 5, 'period': 300},


    #mail
    'api/v1/mail/': {'limit': 5, 'period': 300},



}

class DynamicThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path is in the throttling rules
        for path, rule in THROTTLE_RULES.items():
            if request.path.startswith(path):
                limit = rule['limit']
                period = rule['period']

                # Throttle based on user email if authenticated, otherwise by IP
                if request.user.is_authenticated:
                    throttle_key = f"{path}:user:{request.user.email}"
                else:
                    client_ip = self.get_client_ip(request)
                    throttle_key = f"{path}:ip:{client_ip}"

                if not self.is_throttled(throttle_key, limit, period):
                    return JsonResponse({"detail": "Too many requests. Please try again later."}, status=429)

        # Process the request
        response = self.get_response(request)
        return response

    def is_throttled(self, throttle_key, limit, period):
        """
        Check if the request is throttled based on the key, limit, and period.
        """
        current_time = time.time()
        throttle_data = cache.get(throttle_key, [])

        
        throttle_data = [timestamp for timestamp in throttle_data if timestamp > current_time - period]
        cache.set(throttle_key, throttle_data, timeout=period)

        if len(throttle_data) >= limit:
            return False  # User has exceeded the request limit

        # Update the cache with the new timestamp
        throttle_data.append(current_time)
        cache.set(throttle_key, throttle_data, timeout=period)
        return True

    def get_client_ip(self, request):
        """
        Get the client's IP address from the request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
