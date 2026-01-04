from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from src.api.query import router as query_router
from src.api.admin import router as admin_router


app = FastAPI(title="Project 180 - Agentic AI Backend", version="0.1")

@app.get("/health")
def health():
    return {"status": "ok", "service": "project-180"}

app.include_router(query_router, prefix="")
app.include_router(admin_router, prefix="")


# ✅ Add Bearer Auth to Swagger (Authorize button)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="Secure NLSQL Agent Backend with RBAC + MCP Tools",
        routes=app.routes,
    )

    # Security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Apply globally (all endpoints)
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
