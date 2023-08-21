import math
import random

OTP_LOWER_LIMIT = 100000
OTP_UPPER_LIMIT = 999999

def generate_otp():
    return random.randint(OTP_LOWER_LIMIT, OTP_UPPER_LIMIT)
