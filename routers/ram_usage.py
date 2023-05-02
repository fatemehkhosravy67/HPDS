from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, RAMUsage

router = APIRouter()


@router.get("/")
def home_page():
    return {"message": "Hello World"}


@router.get("/ram_usage/")
async def read_ram_usage(n: int, db: Session = Depends(get_db)):
    if n < 1:
        raise HTTPException(status_code=400, detail="n should be a positive integer")
    rows = db.query(RAMUsage).order_by(RAMUsage.timestamp.desc()).limit(n).all()
    if len(rows) == 0:
        raise HTTPException(status_code=404, detail="No data found")
    # if len(rows) < n:
    #     raise HTTPException(status_code=404, detail='')
    result = []
    for row in rows:
        result.append({
            "id": row.id,
            "total": row.total,
            "free": row.free,
            "used": row.used,
            "timestamp": row.timestamp
        })
    return result
