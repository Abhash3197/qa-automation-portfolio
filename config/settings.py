import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium")
TIMEOUT = int(os.getenv("TIMEOUT", 30000))

# Test users
VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"

LOCKED_USER = "locked_out_user"
PERFORMANCE_USER = "performance_glitch_user"
PROBLEM_USER = "problem_user"
