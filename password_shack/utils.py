from random import randint

def otp_generator():
    """
        Randomly generates an OTP of size 6
    """
    return randint(100000, 999999)