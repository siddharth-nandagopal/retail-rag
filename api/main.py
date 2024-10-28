from fastapi import FastAPI
# from endpoints.data_queries import router as data_queries_router
# from endpoints.semantic_search import router as semantic_search_router
from endpoints import data_queries_router, semantic_search_router

app = FastAPI(
    title="Retail RAG API",
    description="API for handling structured data queries and vector-based searches for the Retail RAG application.",
    version="1.0.0"
)

# Include routers
app.include_router(data_queries_router, prefix="/data")
app.include_router(semantic_search_router, prefix="/search")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Retail RAG API"}
