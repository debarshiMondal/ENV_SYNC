# ENV_SYNC Dashboard (FastAPI)

FastAPI-based internal dashboard for:
- Login-protected access
- Overview dashboard
- Master Sync
- Branch Sync
- Branch Sync History
- Run Reports (comparison / dump / author log – future)

All labels, paths, and behavior are driven by JSON config files in `conf/`.
Master Sync runs operate under `/data/public/ENV_SYNC/MasterSync/{timestamp}`.
