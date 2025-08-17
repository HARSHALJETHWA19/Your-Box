from fastapi import APIRouter
router = APIRouter()

@router.get("")
def get_quota():
    return {"usedBytes": 0, "softLimitBytes": 1099511627776, "hardLimitBytes": 1159641169920}
