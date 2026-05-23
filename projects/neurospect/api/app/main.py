from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.coach.router import events_router, webhook_router
from app.config import settings
from app.database import engine
from app.routers.analytics import router as analytics_router
from app.routers.billing import router as billing_router
from app.routers.prop_shield import router as prop_shield_router
from app.routers.screenshots import router as screenshots_router
from app.routers.trades import router as trades_router
from app.routers.tradovate import router as tradovate_router
from app.routers.tv_tokens import router as tv_tokens_router

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=0.2,
        environment="production" if not settings.debug else "development",
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="Neurospect API",
    description="Trade journal, analytics, and AI coach backend",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — frontend SPA on a different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}


# Auth
app.include_router(auth_router)

# Trade journal
app.include_router(trades_router)
app.include_router(screenshots_router)
app.include_router(analytics_router)

# Prop Shield (Phase 3)
app.include_router(prop_shield_router)
app.include_router(billing_router)

# AI Coach
app.include_router(tv_tokens_router)
app.include_router(tradovate_router)
app.include_router(webhook_router)
app.include_router(events_router)
