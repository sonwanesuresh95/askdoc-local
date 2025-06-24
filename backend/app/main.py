from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_upload, routes_query, routes_document, routes_debug_vectorstore

app = FastAPI(title="AskDoc-Local")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(routes_upload.router, prefix="/api", tags=["Upload"])
app.include_router(routes_query.router, prefix="/api", tags=["Query"])
app.include_router(routes_document.router, prefix="/api", tags=["Document"])
app.include_router(routes_debug_vectorstore.router, prefix="/api", tags=["Debug Vectorstore"])
