from fastapi import APIRouter
from database import get_collection
from models.aircom import AirComSchema
from datetime import datetime, timedelta
router = APIRouter(prefix="/status", tags=["Status"])

collection = get_collection()


@router.get("/{status_id}")
async def get_status_flat(status_id:str):
    pipeline = [
        {"$unwind": "$statuses"},
        {"$match": {"statuses.status_id": status_id}},
        {
            "$project": {
                "_id": 0,
                "status_id":"$statuses.status_id",
                "status":"$stautses.status",
                "time": "$time"
            }
        }
    ]

    result = []
    async for doc in collection.aggregate(pipeline):
        result.append(doc)

    return result

@router.get("/{status_id}/today")
async def get_status_today(status_id: str):

    # 🔥 หาช่วงเวลาวันนี้ (00:00 → 23:59)
    now = datetime.utcnow()
    start_of_day = datetime(now.year, now.month, now.day)
    end_of_day = start_of_day + timedelta(days=1)

    pipeline = [
        # ✅ กรองวันก่อน (เร็วขึ้น)
        {
            "$match": {
                "time": {
                    "$gte": start_of_day,
                    "$lt": end_of_day
                }
            }
        },

        # ✅ แตก array
        {"$unwind": "$statuses"},

        # ✅ กรองเครื่อง
        {"$match": {"statuses.status_id": status_id}},

        # ✅ เลือก field
        {
            "$project": {
                "_id": 0,
                "status_id":"$statuses.status_id",
                "status":"$stautses.status",
                "time": "$time"
            }
        },

        # 🔥 เรียงจากล่าสุด
        {"$sort": {"time": -1}}
    ]

    result = []
    async for doc in collection.aggregate(pipeline):
        result.append(doc)

    return result