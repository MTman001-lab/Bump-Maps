# bump_api/routers/bumps.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from pydantic import BaseModel
from database import get_db
from models import Bump, User
from auth import get_current_user
from config import settings

router = APIRouter(prefix="/api/bumps", tags=["bumps"])

# --- Pydantic Schemas ---
class BumpCreate(BaseModel):
    latitude: float
    longitude: float
    severity: int
    description: str

class BumpOut(BaseModel):
    id: int
    latitude: float
    longitude: float
    severity: int
    description: str
    confirmed: int
    removed: bool
    reported_by: str

    class Config:
        orm_mode = True


# --- 1. Report a bump ---
@router.post("/", response_model=BumpOut)
def report_bump(bump: BumpCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Deduplication: Check if a bump already exists within X meters
    dup_radius = 20  # meters
    existing = db.query(Bump).filter(
        func.ST_DWithin(
            Bump.geom, 
            func.ST_SetSRID(func.ST_MakePoint(bump.longitude, bump.latitude), 4326),
            dup_radius
        )
    ).first()

    if existing:
        existing.confirmed += 1
        db.commit()
        db.refresh(existing)
        return existing

    # Create new bump
    new_bump = Bump(
        latitude=bump.latitude,
        longitude=bump.longitude,
        severity=bump.severity,
        description=bump.description,
        reported_by=user.username,
        geom=func.ST_SetSRID(func.ST_MakePoint(bump.longitude, bump.latitude), 4326)
    )
    db.add(new_bump)
    db.commit()
    db.refresh(new_bump)
    return new_bump


# 1. GET bumps near a location
@router.get("/bumps", response_model=list[schemas.BumpOut])
def get_bumps(
    lat: float = Query(...),
    lon: float = Query(...),
    radius: int = Query(1000, description="Radius in meters"),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = text(
        "SELECT * FROM bumps "
        "WHERE ST_DWithin(geom::geography, ST_MakePoint(:lon, :lat)::geography, :radius)"
    )
    bumps = db.execute(query, {"lon": lon, "lat": lat, "radius": radius}).fetchall()
    return [dict(row) for row in bumps]

# 2. Report a bump
@router.post("/report_bump", response_model=schemas.BumpOut)
def report_bump(
    bump: schemas.BumpCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_bump = models.Bump(
        latitude=bump.latitude,
        longitude=bump.longitude,
        severity=bump.severity,
        description=bump.description,
        reported_by=current_user.username,
        geom=f"SRID=4326;POINT({bump.longitude} {bump.latitude})"
    )
    db.add(new_bump)
    db.commit()
    db.refresh(new_bump)
    broadcast_bump(new_bump)
    return new_bump

# 3. Confirm bump
@router.post("/confirm_bump", response_model=schemas.BumpOut)
def confirm_bump(
    bump_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    bump = db.query(models.Bump).get(bump_id)
    if not bump:
        raise HTTPException(status_code=404, detail="Bump not found")
    bump.confirmed += 1
    db.commit()
    db.refresh(bump)
    broadcast_bump(bump)
    return bump

# 4. Remove bump (government only)
@router.post("/remove_bump", response_model=schemas.BumpOut)
def remove_bump(
    bump_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "government":
        raise HTTPException(status_code=403, detail="Only government users can remove bumps")
    bump = db.query(models.Bump).get(bump_id)
    if not bump:
        raise HTTPException(status_code=404, detail="Bump not found")
    bump.removed = True
    db.commit()
    db.refresh(bump)
    broadcast_bump(bump)
    return bump
# 5. Get all bumps (admin only)
@router.get("/all_bumps", response_model=list[schemas.BumpOut])
def get_all_bumps(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.require_role("admin"))
):
    bumps = db.query(models.Bump).all()
    return bumps