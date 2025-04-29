from passlib.context import CryptContext

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
