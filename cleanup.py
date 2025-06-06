from database import SessionLocal
from models import Message
from datetime import datetime, timedelta

db = SessionLocal()
cutoff = datetime.utcnow() - timedelta(hours=24)
db.query(Message).filter(Message.timestamp < cutoff).delete()
db.commit()

