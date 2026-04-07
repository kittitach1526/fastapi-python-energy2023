from fastapi import APIRouter
from database import get_collection
from models.aircom import AirComSchema
from datetime import datetime, timedelta
router = APIRouter(prefix="/aircom", tags=["AirCom"])

collection = get_collection()


# ✅ POST
@router.post("/")
async def create_aircom(data: AirComSchema):
    result = await collection.insert_one(data.dict())
    return {
        "status": "success",
        "inserted_id": str(result.inserted_id)
    }


# # ✅ GET latest
# @router.get("/latest")
# async def get_latest():
#     doc = await collection.find_one({}, sort=[("time", -1)], projection={"_id": 0})
#     return doc


# ✅ GET by aircom_id (ใช้ pipeline)
@router.get("/{ac_id}")
async def get_aircoms_flat(ac_id:str):
    pipeline = [
        {"$unwind": "$aircoms"},
        {"$match": {"aircoms.aircom_id": ac_id}},
        {
            "$project": {
                "_id": 0,
                "aircom_id": "$aircoms.aircom_id",
                "pressure": "$aircoms.pressure",
                "temp": "$aircoms.temp",
                "power_ac": "$aircoms.power_ac",
                "total_run": "$aircoms.total_run",
                "delay": "$aircoms.delay",
                "state": "$aircoms.state",
                "warning": "$aircoms.warning",
                "danger": "$aircoms.danger",
                "time": "$time"
            }
        }
    ]

    result = []
    async for doc in collection.aggregate(pipeline):
        result.append(doc)

    return result


@router.get("/{ac_id}/today")
async def get_aircom_today(ac_id: str):

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
        {"$unwind": "$aircoms"},

        # ✅ กรองเครื่อง
        {"$match": {"aircoms.aircom_id": ac_id}},

        # ✅ เลือก field
        {
            "$project": {
                "_id": 0,
                "aircom_id": "$aircoms.aircom_id",
                "pressure": "$aircoms.pressure",
                "temp": "$aircoms.temp",
                "power_ac": "$aircoms.power_ac",
                "total_run": "$aircoms.total_run",
                "delay": "$aircoms.delay",
                "state": "$aircoms.state",
                "warning": "$aircoms.warning",
                "danger": "$aircoms.danger",
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