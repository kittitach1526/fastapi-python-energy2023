from fastapi import APIRouter
from database import get_collection
from models.aircom import AirComSchema
from datetime import datetime, timedelta
router = APIRouter(prefix="/pressure", tags=["Pressure"])

collection = get_collection()


@router.get("/{pressure_id}")
async def get_pressue_flat(pressure_id:str):
    pipeline = [
        {"$unwind": "$pressures"},
        {"$match": {"pressures.pressure_id": pressure_id}},
        {
            "$project": {
                "_id": 0,
                "pressure_id":"$pressures.pressure_id",
                "value":"$pressures.value",
                "time": "$time"
            }
        }
    ]

    result = []
    async for doc in collection.aggregate(pipeline):
        result.append(doc)

    return result

@router.get("/{pressure_id}/today")
async def get_pressure_today(pressure_id: str):

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
        {"$unwind": "$pressures"},

        # ✅ กรองเครื่อง
        {"$match": {"pressures.pressure_id": pressure_id}},

        # ✅ เลือก field
        {
            "$project": {
                "_id": 0,
                "prssure_id":"$pressures.pressure_id",
                "value":"$pressures.value",
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