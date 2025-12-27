from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from ..config import settings
from ..utils import get_hora_peru

class JWTService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = get_hora_peru() + expires_delta
        else:
            expire = get_hora_peru() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        to_encode = data.copy()
        expire = get_hora_peru() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    def validate_token(token: str, expected_type: str = "access") -> Optional[Dict[str, Any]]:
        payload = JWTService.decode_token(token)
        if payload and payload.get("type") == expected_type:
            # La expiración es validada automáticamente por jwt.decode
            return payload
        return None
