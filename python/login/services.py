import json
import logging

from start import *


logger = logging.getLogger(__name__)
# Configure logger to include timestamp, log level and source filename:lineno
# Add a StreamHandler with a formatter only if no handlers are configured to avoid
# duplicate handlers when this module is imported multiple times.
if not logging.getLogger().handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)



print (__name__)
class UserAuthService:

    def __init__(self):
        with open("data.json", "r") as file:
            user_data = file.read()
            self.data = json.loads(user_data)

    def authenticate(self, username: str, password: str):
        logger.info("Authentication service is called")
        try:
            if self.data[username]:
                if password == self.data[username]["password"]:
                    return {"status": "Login is successful"}
                else:
                    return {"status": "Login is not successful"}
        except Exception as error:
            # Use logger.exception to include traceback along with our formatted message
            logger.exception("Error while authenticating user %s", error)
            return {"status": "either username or password is incorrect"}

class passwordAuthService:
    def __init__(self):
        with open("data.json", "r") as file: