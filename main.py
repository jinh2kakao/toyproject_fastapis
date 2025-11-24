from fastapi import FastAPI
from fastapi.templating import Jinja2Templates # 템플릿 엔진(Jinja2) 사용을 위한 임포트
from fastapi.requests import Request # 템플릿 렌더링 시 필요한 HTTP 요청 객체
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="templates"), name="static")

templates = Jinja2Templates(directory="templates")

# 1. index.html (홈 페이지)
# 로컬 호출 경로: http://localhost:8000/
@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 2. mypage.html (마이 페이지)
# 템플릿 파일 경로: quests/templates/mypage.html
# 로컬 호출 경로: http://localhost:8000/mypage
@app.get("/mypage")
async def read_mypage(request: Request):
    return templates.TemplateResponse("mypage.html", {"request": request})

# orchestra.html (오케스트라 페이지)
@app.get("/orchestra")
async def read_orchestra(request: Request):
    return templates.TemplateResponse("orchestra.html", {"request": request})

# 3. pro-plan.html (프로 플랜 안내 페이지)
# 템플릿 파일 경로: quests/templates/pro-plan.html
# 로컬 호출 경로: http://localhost:8000/plan/pro
@app.get("/plan/pro")
async def read_pro_plan(request: Request):
    return templates.TemplateResponse("pro-plan.html", {"request": request})

# 4. output-detail.html (결과 상세 페이지)
# 템플릿 파일 경로: quests/templates/output-detail.html
# 로컬 호출 경로: http://localhost:8000/output/detail
@app.get("/output/detail")
async def read_output_detail(request: Request):
    return templates.TemplateResponse("output-detail.html", {"request": request})

# 5. settings.html (일반 설정 페이지)
# 템플릿 파일 경로: quests/templates/settings.html
# 로컬 호출 경로: http://localhost:8000/settings
@app.get("/settings")
async def read_settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

# 6. templates.html (템플릿 목록 페이지)
# 템플릿 파일 경로: quests/templates/templates.html
# 로컬 호출 경로: http://localhost:8000/templates
@app.get("/templates")
async def read_templates(request: Request):
    return templates.TemplateResponse("templates.html", {"request": request})