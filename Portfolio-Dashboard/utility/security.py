from email.policy import strict

import bcrypt #libary with salting and stretching capabilities

def hash_password(password: str) -> str:
    """
    Hashing a password using bcrypt's salting capabilities
    :param password: user password to be hashed with a salt string
    :return: hashed password
    """
    #Generates the salt that will be combined with the password
    salt = bcrypt.gensalt();
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def validate_password(stored_password: str, provided_password: str) -> bool:
    """
    Check to see if stored password matches provided password
    :param stored_password: hashed password in database
    :param provided_password: password provided from user, un-hashed
    :return: True if they match, else False
    """
    #Checks passwords against each other and returns a bool value if they are the same
    return bcrypt.checkpw(provided_password.encode("utf-8"), stored_password.encode("utf-8"))



