from passlib.context import CryptContext

# Hashing Passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto")

def hash(password: str):
    return pwd_context.hash(password)

# Verify password against hashedpassword
def verify(plain_password, hashedpassword):
    return pwd_context.verify(plain_password, hashedpassword)

