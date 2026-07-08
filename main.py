from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid
import time

EMAIL = "24f2001122@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-76j6p5.example.com"

app = FastAPI()

# Strict CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# Middleware to add required headers
@app.middleware("http")
async def process_time_middleware(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    return response


@app.get("/")
def home():
    return {"status": "ok"}


@app.get("/stats")
def stats(values: str = Query(...)):
    try:
        nums = [int(x.strip()) for x in values.split(",")]
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "values must contain integers only"}
        )

    if len(nums) == 0:
        return JSONResponse(
            status_code=400,
            content={"error": "No values supplied"}
        )

    total = sum(nums)

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": total,
        "min": min(nums),
        "max": max(nums),
        "mean": total / len(nums)
    }
