from fastapi import FastAPI, HTTPException, Depends
from models.user import User
from services.storage import StorageService
from models.checkin import Checkin
from models.checkin_request import CheckinRequest
import os

app = FastAPI()


@app.get("/api/registrations")
def list_registrations(storage_service: StorageService = Depends()) -> list[User]:
    """List all registrations in the system."""
    return storage_service.get_registrations()


@app.post("/api/registrations")
def new_registration(user: User, storage_service: StorageService = Depends()) -> User:
    """Create a new user/registration."""
    try:
        return storage_service.create_registration(user)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/api/reset")
def reset(storage_service: StorageService = Depends()) -> str:
    """Development-only route for resetting storage module and adding fake user and checkin."""
    if "MODE" in os.environ and os.environ["MODE"] == "production":
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        storage_service.reset()
        storage_service.create_registration(User(pid=710453084, first_name="Kris", last_name="Jordan"))
        storage_service.create_registration(User(pid=730470759, first_name="Ben", last_name="Goroshnik"))
        storage_service.create_checkin(710453084)
        storage_service.create_checkin(730470759)
        return "OK"
    

@app.post("/api/checkins")
def create_checkin(checkin_request: CheckinRequest, storage_service: StorageService = Depends()) -> Checkin:
    """Create a new checkin."""
    try:
        pid = checkin_request.pid
        print(f"Debug: Checkin object is {checkin_request}")
        print(f"Debug: pid is {pid}")
        return storage_service.create_checkin(pid)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    

@app.get("/api/checkins")
def list_checkins(storage_service: StorageService = Depends()) -> list[Checkin]:
    """List all checkins in the system."""
    return storage_service.get_checkins()


@app.delete("/api/registrations/{pid}")
def delete_registration(pid: int, storage_service: StorageService = Depends()):
    """Deletes a user from registration and checkin."""
    try:
        deleted = storage_service.delete_registration(pid)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))