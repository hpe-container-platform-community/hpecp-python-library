class ContainerPlatformClientException(Exception):
    def __init__(self, message, *args):
        self.message = message
        super( ContainerPlatformClientException, self).__init__(message, *args) 

class APIException(Exception):
    def __init__(self, message, request_method, request_url, request_data=None, *args):
        self.message = message
        self.request_method = request_method
        self.request_url = request_url
        self.request_data = request_data
        super( APIException, self).__init__(message, request_method, request_url, request_data, *args) 

class APIItemNotFoundException(APIException):
    def __init__(self, message, request_method, request_url, request_data=None, *args):
        self.message = message
        self.request_method = request_method
        self.request_url = request_url
        self.request_data = request_data
        super( APIItemNotFoundException, self).__init__(message, request_method, request_url, request_data, *args) 
