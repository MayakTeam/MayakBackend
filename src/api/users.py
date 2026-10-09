from fastapi import APIRouter

router = APIRouter()

@router.get("/current_user")
async def get_current_user():
    
    return {"message": "Current user information"}