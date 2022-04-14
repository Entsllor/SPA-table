from datetime import datetime
from ..core.database import Base
from sqlalchemy import Date, String, Integer, Column, DECIMAL


class TableRow(Base):
    __tablename__ = "table_row"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), index=True)
    date = Column(Date, index=True, default=datetime.now().date())
    quantity = Column(Integer)
    distance = Column(DECIMAL(precision=7, scale=7))
