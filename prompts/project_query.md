## query 생성 프롬프트
```
{
  "request_config": {
    "target_agent": "Database Architect & Backend Developer",
    "output_path": "querys/project.sql",
    "description": "Generate SQL schema and CRUD queries based on the provided HTML UI structure."
  },
  "instruction_prompt": {
    "context": "사용자가 제공한 HTML 코드는 'AI 소설 제작' 대시보드와 '새 프로젝트 생성 모달(New Project Modal)'입니다. 이 UI를 기반으로 백엔드 데이터베이스 처리를 위한 SQL 파일을 작성해야 합니다.",
    "requirements": {
      "file_structure": {
        "directory": "querys",
        "filename": "project.sql"
      },
      "database_schema": {
        "table_name": "projects",
        "columns_mapping": [
          {
            "ui_source": "#projectTitle (Modal Input)",
            "db_column": "title",
            "type": "VARCHAR(255)",
            "constraint": "NOT NULL"
          },
          {
            "ui_source": "#projectGenre (Modal Select)",
            "db_column": "genre",
            "type": "VARCHAR(50) OR INT",
            "note": "HTML values are 1-5, map appropriately or store as ID"
          },
          {
            "ui_source": "#projectLogline (Modal Textarea)",
            "db_column": "logline",
            "type": "TEXT"
          },
          {
            "ui_source": "Dashboard Card Image",
            "db_column": "image_url",
            "type": "VARCHAR(255)",
            "default": "Default placeholder URL"
          },
          {
            "ui_source": "Dashboard Metadata (Time)",
            "db_column": "updated_at",
            "type": "TIMESTAMP",
            "default": "CURRENT_TIMESTAMP"
          },
          {
            "ui_source": "System Field",
            "db_column": "created_at",
            "type": "TIMESTAMP",
            "default": "CURRENT_TIMESTAMP"
          }
        ]
      },
      "queries_to_generate": [
        {
          "type": "DDL",
          "description": "Create the 'projects' table if it does not exist."
        },
        {
          "type": "INSERT",
          "description": "Query to add a new project from the Modal inputs (title, genre, logline)."
        },
        {
          "type": "SELECT",
          "description": "Query to fetch all projects to render the Dashboard Grid cards. Should be ordered by updated_at DESC."
        },
        {
          "type": "UPDATE",
          "description": "Query to update project details (title, genre, logline, image_url, updated_at)."
        },
        {
          "type": "DELETE",
          "description": "Query to delete a project by ID."
        }
      ]
    },
    "style_guidelines": [
      "Use standard SQL syntax compatible with MySQL or PostgreSQL.",
      "Include comments explaining which HTML part corresponds to which query.",
      "Ensure logical defaults for fields not present in the modal (e.g., image_url)."
    ]
  }
}
```

## python 코드 작성 프롬프트
```
{
  "request_config": {
    "agent_role": "Python Backend Developer (FastAPI)",
    "output_files": [
      "main.py",
      "routes/project.py"
    ],
    "description": "Create FastAPI application structure and CRUD routes for 'projects' based on the provided reference code style."
  },
  "instruction_prompt": {
    "context": "당신은 FastAPI와 PostgreSQL을 활용하는 백엔드 개발자입니다. 사용자가 제공한 'todos' 예시 코드의 구조와 패턴을 참조하여, 'projects' 테이블을 관리하는 어플리케이션을 작성해야 합니다.",
    "requirements": {
      "file_structure": {
        "root": "main.py (App entry point)",
        "routes_folder": "routes/project.py (Actual CRUD logic)"
      },
      "tech_stack": [
        "FastAPI",
        "Jinja2Templates",
        "psycopg2 (with DictCursor)",
        "uvicorn"
      ],
      "database_schema": "projects table (id, title, genre, logline, image_url, created_at, updated_at)"
    },
    "coding_guidelines": [
      "예시 코드(todos)의 import 스타일과 라우터 설정 방식을 따를 것.",
      "단, SQL 쿼리 작성 시 예시의 f-string 방식은 보안에 취약하므로, 반드시 Parameterized Query (%s) 방식을 사용하여 작성할 것.",
      "DB 연결 함수는 `services.db.get_db_connection`을 import하여 사용한다고 가정할 것."
    ],
    "tasks": [
      {
        "filename": "main.py",
        "instructions": [
          "FastAPI 인스턴스 생성",
          "StaticFiles 마운트 (/static)",
          "routes.project의 router를 include_router로 등록",
          "Uvicorn 실행 코드 포함 (if __name__ == '__main__':)"
        ]
      },
      {
        "filename": "routes/project.py",
        "instructions": [
          "APIRouter 및 Jinja2Templates 설정 (templates 디렉토리 지정)",
          "1. [READ] GET '/': projects 테이블의 모든 데이터를 `updated_at DESC` 정렬로 조회하여 `dashboard.html` 렌더링.",
          "2. [CREATE] POST '/': Form 데이터(title, genre, logline)를 받아 projects 테이블에 INSERT.",
          "3. [UPDATE] POST '/update/{id}': Form 데이터를 받아 해당 ID의 프로젝트 정보(title, genre, logline, updated_at) UPDATE.",
          "4. [DELETE] GET '/delete/{id}': 해당 ID의 프로젝트 DELETE.",
          "모든 C/U/D 작업 후에는 DB 커밋 및 연결 종료를 확실히 하고, 갱신된 목록과 함께 템플릿을 반환하거나 Redirect 할 것."
        ]
      }
    ]
  }
}


```

## html 연결 코드 작성 프롬프트
```
{
  "request_config": {
    "agent_role": "Full Stack Web Developer",
    "output_file": "templates/dashboard.html",
    "description": "Convert static HTML into a dynamic Jinja2 template connected to FastAPI backend."
  },
  "instruction_prompt": {
    "context": "현재 `dashboard.html`은 정적인 하드코딩 데이터만 포함하고 있습니다. 이를 백엔드(FastAPI)에서 전달받은 `projects` 데이터를 표시하고, 사용자 입력(프로젝트 생성)을 백엔드로 전송할 수 있도록 수정해야 합니다.",
    "tasks": [
      {
        "category": "1. Data Rendering (List Call)",
        "instruction": "백엔드에서 넘겨준 `projects` 리스트를 반복문(`{% for project in projects %}`)을 사용하여 카드 영역에 동적으로 출력하시오.",
        "mappings": [
          { "ui_element": "Card Image", "data_field": "{{ project.image_url }}" },
          { "ui_element": "Project Title", "data_field": "{{ project.title }}" },
          { "ui_element": "Description", "data_field": "{{ project.logline }}" },
          { "ui_element": "Genre Badge", "data_field": "{{ project.genre }}" },
          { "ui_element": "Updated Time", "data_field": "{{ project.updated_at }}" },
          { "ui_element": "Link", "data_field": "/project/{{ project.id }}" }
        ]
      },
      {
        "category": "2. Form Action (Create Project)",
        "instruction": "Modal 내의 `<form>` 태그를 수정하여 데이터를 백엔드로 전송할 수 있게 하시오.",
        "requirements": [
          "form tag에 `method='post'`와 `action='/project/create'` 속성 추가",
          "각 input/select/textarea 태그에 백엔드 스키마와 일치하는 `name` 속성 부여 (name='title', name='genre', name='logline')",
          "Submit 버튼의 type을 `submit`으로 변경"
        ]
      },
      {
        "category": "3. Search Interaction (JavaScript)",
        "instruction": "검색창(`.search-input`)에 검색어를 입력하면, 실시간으로 혹은 엔터 키 입력 시 현재 리스트 내에서 제목을 필터링하여 보여주는 간단한 JavaScript를 `<script>` 태그로 하단에 추가하시오."
      }
    ],
    "code_snippet_example": {
      "list_rendering": "{% for project in projects %}\n<div class='col'>...{{ project.title }}...</div>\n{% endfor %}",
      "form_handling": "<form action='/project/create' method='post'>\n<input name='title' ...>"
    }
  }
}
```