from database import SessionLocal
from models import Message
from datetime import datetime, timedelta
import csv

def export_chat_logs():
    db = SessionLocal()
    cutoff = datetime.utcnow() - timedelta(hours=24)
    messages = db.query(Message).filter(Message.timestamp > cutoff).order_by(Message.timestamp).all()

    with open("chat_logs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "username", "real_username", "ip_address", "text"])
        for msg in messages:
            writer.writerow([msg.timestamp, msg.username, msg.real_username, msg.ip_address, msg.text])

    print("Chat logs exported to chat_logs.csv")

if __name__ == "__main__":
    export_chat_logs()

