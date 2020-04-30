from __future__ import absolute_import
from .logger import Logger

class TagController:

    def __init__(self, client):
        self.client = client
