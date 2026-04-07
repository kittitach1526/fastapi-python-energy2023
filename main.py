from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers.aircom import router as aircom_router
from routers.pressure import router as pressure_router
from routers.flowsensor import router as flow_router
from routers.status import router as status_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # อนุญาตทุก domain
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE
    allow_headers=["*"],  # header ทุกแบบ
)

app.include_router(aircom_router)
app.include_router(pressure_router)
app.include_router(flow_router)
app.include_router(status_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)