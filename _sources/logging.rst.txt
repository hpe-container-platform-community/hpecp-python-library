Logging
=======

Log level is controlled with the environment variable LOG_LEVEL.

You may set it programmatically in your code::

   import os
   os.environ["LOG_LEVEL"] = "DEBUG"

Typical valid values are ERROR, WARNING, INFO, DEBUG. For a full list of values, see here

- INFO = Significant Events
- DEBUG = API Request Parameters