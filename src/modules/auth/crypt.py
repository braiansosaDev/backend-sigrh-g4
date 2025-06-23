from passlib.context import CryptContext
import string
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Retorna el hash de la contraseña.
    Args:
        password (str): Contraseña en texto plano.
    Returns:
        str: Contraseña hasheada.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña en texto plano coincide con el hash.
    Args:
        plain_password (str): Contraseña en texto plano.
        hashed_password (str): Contraseña hasheada.
    Returns:
        bool: True si coinciden, False en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_secure_random_password(
    length: int = 50,
    digits: bool = True,
    punctuation: bool = True,
    min_digits: int = 5,
    min_punctuation: int = 5,
):
    alphabet = string.ascii_letters
    if digits:
        alphabet += string.digits
    if punctuation:
        alphabet += string.punctuation
    if min_punctuation < 0:
        raise ValueError("min_punctuation must not be negative")
    if min_digits < 0:
        raise ValueError("min_digits must not be negative")
    if min_digits + min_punctuation >= length:
        raise ValueError("Minimum digits plus minimum punctuation should be less than the length.")

    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (
            sum(c.isdigit() for c in password) >= min_digits
            and sum(c in string.punctuation for c in password) >= min_punctuation
        ):
            return password
