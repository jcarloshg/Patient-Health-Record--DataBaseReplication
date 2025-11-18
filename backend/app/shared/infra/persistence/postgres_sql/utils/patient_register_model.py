from typing import List
from typing import Optional
from datetime import date
from uuid import UUID as UUIDType, uuid4
from sqlalchemy import String, Date, ARRAY, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass

class PatientRegisterModel(Base):

    __tablename__ = "patientregister"

    uuid: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    emergency_contact: Mapped[str] = mapped_column(String(50), nullable=False)
    allergies: Mapped[List[str]] = mapped_column(ARRAY(Text), default=list)
    medical_history: Mapped[List[str]] = mapped_column(
        ARRAY(Text), default=list)
    current_medications: Mapped[List[str]] = mapped_column(
        ARRAY(Text), default=list)
