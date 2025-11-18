from __future__ import annotations
from typing import Dict, Any
from env_sync import list_master_sync, list_branch_sync, list_branch_history

def main_dashboard_context() -> Dict[str, Any]:
    master = list_master_sync()
    return {
        "master_count": len(master),
        "master_runs": master[:5],
    }

def master_sync_context() -> Dict[str, Any]:
    return {
        "runs": list_master_sync()
    }

def branch_sync_context(branch: str = "master") -> Dict[str, Any]:
    return {
        "branch": branch,
        "runs": list_branch_sync(branch)
    }

def branch_history_context(branch: str = "master") -> Dict[str, Any]:
    return {
        "branch": branch,
        "history": list_branch_history(branch)
    }

def run_reports_context() -> Dict[str, Any]:
    return {
        "info": "Configure and trigger comparison, dump, and author log flows here (future)."
    }
