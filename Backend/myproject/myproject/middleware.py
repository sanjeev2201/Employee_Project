import time

class ApiExecutionTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()

        execution_time = end_time - start_time
        print('Api execution time : - ',execution_time)
        response["X-Execution-Time"] = f"{execution_time:.4f}s"

        return response
