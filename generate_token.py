from jwt import encode
import datetime
from common.config import settings

SECRET_KEY = settings.SECRET_KEY

payload = {
    "sub": "user123",
    "iat": datetime.datetime.utcnow(),
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
}

token = encode(payload, SECRET_KEY, algorithm="HS256")
print("Bearer", token)
