"""A python library for working with HPE Container Platform

.. moduleauthor:: Chris Snow <chsnow123@gmail.com>

"""

from __future__ import absolute_import


from .logger import Logger

from .client import ContainerPlatformClient, ContainerPlatformClientException, APIException
