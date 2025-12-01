from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, users, animals, applications, favorites

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(animals.router, prefix=f"{settings.API_V1_STR}/animals", tags=["animals"])
app.include_router(applications.router, prefix=f"{settings.API_V1_STR}/applications", tags=["applications"])
app.include_router(favorites.router, prefix=f"{settings.API_V1_STR}/favorites", tags=["favorites"])

@app.get("/")
async def root():
    return {"message": "Shelter API", "version": settings.VERSION}

@app.get("/health")
async def health():
    return {"status": "healthy"}
