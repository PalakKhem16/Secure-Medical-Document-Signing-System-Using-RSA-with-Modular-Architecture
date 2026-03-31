"""
main.py — FastAPI application entry point.
Registers all routers and configures CORS for frontend access.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes import (
    auth_routes,
    admin_routes,
    doctor_routes,
    sign_routes,
    verify_routes,
    shred_routes,
    steg_routes,
)

app = FastAPI(
    title="Secure Medical Document Signing System",
    description="RSA-based digital document signing for medical professionals.",
    version="1.0.0",
)

#  CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins (dev mode)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Static files (uploaded/steganography images) 
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

#  Routers 
app.include_router(auth_routes.router,   prefix="/auth",   tags=["Auth"])
app.include_router(admin_routes.router,  prefix="/admin",  tags=["Admin"])
app.include_router(doctor_routes.router, prefix="/doctor", tags=["Doctor"])
app.include_router(sign_routes.router,   prefix="/sign",   tags=["Sign"])
app.include_router(verify_routes.router, prefix="/verify", tags=["Verify"])
app.include_router(shred_routes.router,  prefix="/shred",  tags=["Shred"])
app.include_router(steg_routes.router,   prefix="/steg",   tags=["Steganography"])


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "MediSign API is running"}
