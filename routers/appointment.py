import datetime
from fastapi import APIRouter, Depends, HTTPException
from db.models import Appointment
from db import get_session
from pydantic import BaseModel
from sqlmodel import Session, select
router = APIRouter()

class AppointmentRequest(BaseModel):
    start_at: datetime.datetime

@router.post("/appointment/", tags=["appointment"])
async def create_appointment(appointment_req:AppointmentRequest, session: Session = Depends(get_session)):
    a_datetime = Appointment(start_at=appointment_req.start_at)
    session.add(a_datetime)
    session.commit()
    session.refresh(a_datetime)
    return a_datetime

@router.get("/appointment/", tags=["appointment"])
async def getLatest_appointment(session: Session = Depends(get_session)):
    query = select(Appointment).order_by(Appointment.id.desc())
    details_of_appointment = session.exec(query).first()
    return details_of_appointment

@router.get("/appointment/all", tags=["appointment"])
async def getAll_appointments(session: Session = Depends(get_session)):
    # https://www.geeksforgeeks.org/get-current-date-and-time-using-python/
    query = select(Appointment).where(Appointment.start_at > datetime.datetime.now())
    all_appointments = session.exec(query).all()
    return all_appointments


@router.patch("/appointment/{id}", tags=["appointment"])
async def update_appointment(appointment_req:AppointmentRequest, id, session: Session = Depends(get_session)):
    appointment = session.get(Appointment, id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    print(appointment_req.start_at.astimezone(datetime.timezone.utc))
    appointment.start_at = appointment_req.start_at
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    return appointment


@router.delete("/appointment/{id}", tags=["appointment"])
async def delete_appointment(id, session: Session = Depends(get_session)):
    appointment = session.get(Appointment, id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    session.delete(appointment)
    session.commit()
    return {"ok": "Appoint was deleted"}