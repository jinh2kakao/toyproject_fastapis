from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, Optional

# Assume this import exists for database connection
# In a real scenario, you'd create this file and function
from services.db import get_db_connection

import psycopg2
from psycopg2.extras import DictCursor

project_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@project_router.get("/", response_class=HTMLResponse)
async def read_projects(request: Request):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute("SELECT id, title, genre, logline, image_url, updated_at, created_at FROM projects ORDER BY updated_at DESC;")
        projects = cur.fetchall()
        cur.close()
        return templates.TemplateResponse("dashboard.html", {"request": request, "projects": projects})
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "message": "Error fetching projects."}, status_code=500)
    finally:
        if conn:
            conn.close()

@project_router.get("/project/{project_id}", response_class=HTMLResponse)
async def read_project_detail(request: Request, project_id: int):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute("SELECT id, title, genre, logline, image_url, updated_at, created_at FROM projects WHERE id = %s;", (project_id,))
        project = cur.fetchone()
        cur.close()
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return templates.TemplateResponse("project_detail.html", {"request": request, "project": project})
    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        print(f"Error fetching project detail: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "message": "Error fetching project detail."}, status_code=500)
    finally:
        if conn:
            conn.close()

@project_router.post("/", response_class=RedirectResponse)
async def create_project(
    title: Annotated[str, Form()],
    genre: Annotated[str, Form()],
    logline: Annotated[Optional[str], Form()] = None
):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO projects (title, genre, logline) VALUES (%s, %s, %s);",
            (title, genre, logline)
        )
        conn.commit()
        cur.close()
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail="Error creating project")
    finally:
        if conn:
            conn.close()

@project_router.post("/update/{project_id}", response_class=RedirectResponse)
async def update_project(
    project_id: int,
    title: Annotated[str, Form()],
    genre: Annotated[str, Form()],
    logline: Annotated[Optional[str], Form()] = None,
    image_url: Annotated[Optional[str], Form()] = None # Assuming image_url can also be updated via form
):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE projects SET title = %s, genre = %s, logline = %s, image_url = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s;",
            (title, genre, logline, image_url, project_id)
        )
        conn.commit()
        cur.close()
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Error updating project: {e}")
        raise HTTPException(status_code=500, detail="Error updating project")
    finally:
        if conn:
            conn.close()

@project_router.get("/project/delete/{project_id}", response_class=RedirectResponse)
async def delete_project(project_id: int):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM projects WHERE id = %s;", (project_id,))
        conn.commit()
        cur.close()
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Error deleting project: {e}")
        raise HTTPException(status_code=500, detail="Error deleting project")
    finally:
        if conn:
            conn.close()

