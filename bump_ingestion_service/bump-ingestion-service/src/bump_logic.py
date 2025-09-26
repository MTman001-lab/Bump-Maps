from db import Session, Bump, BumpState
import uuid

def find_or_create_bump(lat, lon):
    session = Session()
    bump = session.query(Bump).filter_by(lat=lat, lon=lon).first()
    if not bump:
        bump = Bump(id=str(uuid.uuid4()), lat=lat, lon=lon)
        session.add(bump)
    session.commit()
    return bump

def process_auto_bump(lat, lon):
    bump = find_or_create_bump(lat, lon)
    bump.auto_count += 1
    if bump.auto_count >= 30 and bump.state == BumpState.PENDING:
        bump.state = BumpState.ACTIVE
    Session().commit()

def process_manual_flag(lat, lon, flag_type):
    bump = find_or_create_bump(lat, lon)
    if flag_type == "ADD":
        bump.manual_add_count += 1
        if bump.manual_add_count >= 50 and bump.state == BumpState.PENDING:
            bump.state = BumpState.ACTIVE
    elif flag_type == "REMOVE":
        bump.manual_remove_count += 1
        if bump.manual_remove_count >= 100 and bump.state == BumpState.ACTIVE:
            bump.state = BumpState.REMOVED
    Session().commit()
