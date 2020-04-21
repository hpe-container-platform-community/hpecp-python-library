from unittest import TestCase
from mock import Mock, patch

import sys
import tempfile
import os
import json
import requests
from requests.exceptions import RequestException
from hpecp import ContainerPlatformClient, ContainerPlatformClientException


class TestClient(TestCase):
    
    def test_invalid_api_key_file(self):
        pass
