from __future__ import annotations
from fastapi import Request, HTTPException, status
from typing import Dict, Optional
from uuid import uuid4

from config import get_users_config

SESSION_COOKIE = "envsync_session"
_sessions: Dict[str, str] = {}  # token -> username

def authenticate(username: str, password: str) -> bool:
    users = get_users_config()
    for u in users:
        if u.get("username") == username and u.get("password") == password:
            return True
    return False

def login_user(username: str) -> str:
    token = str(uuid4())
    _sessions[token] = username
    return token

def logout_user(token: str):
    _sessions.pop(token, None)

def get_current_user(request: Request) -> Optional[str]:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    return _sessions.get(token)

def ensure_authenticated(request: Request):
    user = get_current_user(request)
    if not user:
        # redirect by raising 303 with Location header
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"},
            detail="Not authenticated",
        )
    return user
