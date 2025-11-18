from __future__ import annotations
from pathlib import Path
from typing import List
from datetime import datetime

from config import get_app_config
from models import EnvSyncEntry

def _env_root() -> Path:
    cfg = get_app_config()
    return Path(cfg.get("env_sync_root", "/data/public/ENV_SYNC"))

def list_master_sync() -> List[EnvSyncEntry]:
    """List timestamped master sync runs under ENV_SYNC/MasterSync."""
    root = _env_root() / "MasterSync"
    entries: List[EnvSyncEntry] = []
    if root.exists():
        for p in root.iterdir():
            if p.is_dir():
                try:
                    mtime = datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds")
                except Exception:
                    mtime = None
                entries.append(EnvSyncEntry(
                    name=p.name,
                    path=str(p),
                    kind="master",
                    last_modified=mtime,
                ))
    # sort newest first
    entries.sort(key=lambda e: e.last_modified or "", reverse=True)
    return entries

def list_branch_sync(branch: str) -> List[EnvSyncEntry]:
    """Placeholder for future branch sync listing."""
    root = _env_root() / "BranchSync" / branch
    entries: List[EnvSyncEntry] = []
    if root.exists():
        for p in root.iterdir():
            entries.append(EnvSyncEntry(
                name=p.name,
                path=str(p),
                kind="branch",
                last_modified=None,
            ))
    return entries

def list_branch_history(branch: str) -> List[EnvSyncEntry]:
    root = _env_root() / "BranchSyncHistory" / branch
    entries: List[EnvSyncEntry] = []
    if root.exists():
        for p in root.iterdir():
            entries.append(EnvSyncEntry(
                name=p.name,
                path=str(p),
                kind="history",
                last_modified=None,
            ))
    return entries
