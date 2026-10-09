from fastapi import APIRouter, Depends

from src.authentication import check_authentication
from src.api.dependencies import SessionDep

# Для взаимодействия с каким-нибудь отчётом нужно быть залогиненым в систему.
# Будем использовать токен авторизации, который будет передаваться в заголовке запроса.
# Для проверки этого токена будем использовать зависимоть, которую внедрили на уровне роутера.
reports_router = APIRouter(tags=["Reports"], dependencies=[Depends(check_authentication)])

# Create
@reports_router.post("/reports")
async def create_report(session : SessionDep):
    
    return {"message": "Create report"}


# Read
@reports_router.get("/reports")
async def get_reports():
    
    return {"message": "Get all reports"}

@reports_router.get("/reports/{report_id}")
async def get_report(report_id: str):
    return {"message": f"Get report by ID: {report_id}"}


# Update
@reports_router.put("/reports/{report_id}")
async def update_report(report_id: str):
    return {"message": f"Update report by ID: {report_id}"}


# Delete
@reports_router.delete("/reports/{report_id}")
async def delete_report(report_id: str, a = """is_admin: bool = Depends(check_authentication)"""): # тут нужно сделать проверку роли
    return {"message": f"Delete report by ID: {report_id}"}

