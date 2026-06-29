from slowapi import Limiter
from slowapi.util import get_remote_address

""" The limiter object used for limiting endpoints. """
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://redis:6379",
    default_limits=["100/minute"],
)
