import datetime
import asyncio
from sqlmodel import select, Session
from therapistai.db.models import Appointment
from therapistai.db import engine


def check_datetime():
    current_time =datetime.datetime.now(datetime.timezone.utc)
    query = select(Appointment).where(Appointment.start_at > current_time, Appointment.start_at <= current_time + datetime.timedelta(hours=24))
    with Session(engine) as session:
        appointments = session.exec(query).all()
        print("appointment in the next 24 hours:", appointments)

async def check_loop():
    while True:
        check_datetime()
        await asyncio.sleep(3600)