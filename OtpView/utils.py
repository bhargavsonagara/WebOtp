from django.http import JsonResponse
def send_response_validation(request, code, message):

    response = JsonResponse(
        data={'responseCode': code, 'responseMessage': message})
    response.status_code = 200
    return response

def send_response(request, code, message, data):

    response = JsonResponse(
        data={'responseCode': code, 'responseMessage': message, 'responseData': data})
    response.status_code = 200
    return response

def success_200(request, code, message):

    response = JsonResponse(
        data={'responseCode': code, 'responseMessage': message})
    response.status_code = 200
    return response

def error_400(request, code, message):

    response = JsonResponse(
        data={'responseCode': code, 'responseMessage': message})
    response.status_code = 400
    return response