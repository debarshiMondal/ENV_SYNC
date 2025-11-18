from __future__ import annotations
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import get_app_config, get_menu_config, get_page_config
from auth import (
    authenticate,
    login_user,
    logout_user,
    get_current_user,
    ensure_authenticated,
    SESSION_COOKIE,
)
from flows import (
    main_dashboard_context,
    master_sync_context,
    branch_sync_context,
    branch_history_context,
    run_reports_context,
)
from services.master_sync_engine import run_master_sync

app = FastAPI(title="ENV_SYNC Dashboard")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse("/main", status_code=303)
    return RedirectResponse("/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    app_cfg = get_app_config()
    menu_cfg = get_menu_config()
    page_cfg = get_page_config("login")
    return templates.TemplateResponse("login.html", {
        "request": request,
        "app_cfg": app_cfg,
        "menu_cfg": menu_cfg,
        "page_cfg": page_cfg,
        "user": get_current_user(request),
        "error": None,
    })

@app.post("/auth/login")
def login_action(request: Request, username: str = Form(...), password: str = Form(...)):
    if not authenticate(username, password):
        app_cfg = get_app_config()
        menu_cfg = get_menu_config()
        page_cfg = get_page_config("login")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "app_cfg": app_cfg,
            "menu_cfg": menu_cfg,
            "page_cfg": page_cfg,
            "user": None,
            "error": "Invalid username or password",
        })
    token = login_user(username)
    resp = RedirectResponse("/main", status_code=303)
    resp.set_cookie(SESSION_COOKIE, token, httponly=True)
    return resp

@app.get("/auth/logout")
def logout(request: Request):
    resp = RedirectResponse("/login", status_code=303)
    resp.delete_cookie(SESSION_COOKIE)
    return resp

def common_context(request: Request, page_key: str):
    app_cfg = get_app_config()
    menu_cfg = get_menu_config()
    page_cfg = get_page_config(page_key)
    user = get_current_user(request)
    return {
        "request": request,
        "app_cfg": app_cfg,
        "menu_cfg": menu_cfg,
        "page_cfg": page_cfg,
        "user": user,
    }

@app.get("/main", response_class=HTMLResponse)
def main_dashboard(request: Request, user: str = Depends(ensure_authenticated)):
    ctx = common_context(request, "main_dashboard")
    ctx.update(main_dashboard_context())
    return templates.TemplateResponse("main_dashboard.html", ctx)

@app.get("/master-sync", response_class=HTMLResponse)
def master_sync(request: Request, user: str = Depends(ensure_authenticated)):
    ctx = common_context(request, "master_sync")
    ctx.update(master_sync_context())
    ctx["last_result"] = None
    return templates.TemplateResponse("master_sync.html", ctx)

@app.post("/master-sync/start", response_class=HTMLResponse)
def master_sync_start(request: Request, take_dump: str = Form("no"), user: str = Depends(ensure_authenticated)):
    take = take_dump.lower() == "yes"
    result = run_master_sync(take_dump=take)
    ctx = common_context(request, "master_sync")
    ctx.update(master_sync_context())
    ctx["last_result"] = result
    return templates.TemplateResponse("master_sync.html", ctx)

@app.get("/branch-sync", response_class=HTMLResponse)
def branch_sync(request: Request, branch: str = "master", user: str = Depends(ensure_authenticated)):
    ctx = common_context(request, "branch_sync")
    ctx.update(branch_sync_context(branch))
    return templates.TemplateResponse("branch_sync.html", ctx)

@app.get("/branch-sync/history", response_class=HTMLResponse)
def branch_history(request: Request, branch: str = "master", user: str = Depends(ensure_authenticated)):
    ctx = common_context(request, "branch_sync_history")
    ctx.update(branch_history_context(branch))
    return templates.TemplateResponse("branch_sync_history.html", ctx)

@app.get("/run-reports", response_class=HTMLResponse)
def run_reports_page(request: Request, user: str = Depends(ensure_authenticated)):
    ctx = common_context(request, "run_reports")
    ctx.update(run_reports_context())
    return templates.TemplateResponse("run_reports.html", ctx)
