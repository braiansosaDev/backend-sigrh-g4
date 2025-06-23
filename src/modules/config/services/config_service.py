from dotenv import load_dotenv
import os

load_dotenv()

def get_str(key: str) -> str:
    res = os.getenv(key)
    if res is None:
        raise ValueError(f"Environment variable {key} not found.")
    return res


def get_bool(key: str) -> bool:
    return get_str(key).lower() == "true"
