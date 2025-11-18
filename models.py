from __future__ import annotations
from pydantic import BaseModel
from typing import List

class LoginForm(BaseModel):
    username: str
    password: str

class UserConfig(BaseModel):
    username: str
    password: str  # NOTE: plain text for now; replace with hash later
    role: str | None = None

class EnvSyncEntry(BaseModel):
    name: str
    path: str
    kind: str  # e.g. "master", "branch", "history"
    last_modified: str | None = None

class MasterSyncResult(BaseModel):
    timestamp: str
    run_folder: str
    status: str            # "success" or "failed"
    message: str
    errors: List[str] = []
