from fastapi import APIRouter
router = APIRouter()

@router.get("")
def list_folders():
    return {"items": []}
