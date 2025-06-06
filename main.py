from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from database import get_db
from models import Message
from datetime import datetime, timedelta

import random

from models import Message
from database import SessionLocal, engine, Base
from auth import router as auth_router, get_current_user


from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import secrets

security = HTTPBasic()

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "yourpassword123")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username



# Create tables
Base.metadata.create_all(bind=engine)

# App setup
app = FastAPI()
app.include_router(auth_router, prefix="/auth")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Display messages (last 24 hours)
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    db = SessionLocal()
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=24)
    messages = db.query(Message).filter(Message.timestamp > cutoff).order_by(Message.timestamp).all()
    return templates.TemplateResponse("chat.html", {"request": request, "messages": messages})
@app.post("/send")
async def send_message(
    request: Request,
    text: str = Form(...),
    user = Depends(get_current_user),
):
    db = SessionLocal()

    # Temporary anonymous name
    anon_id = f"anonymous{random.randint(10000, 99999)}"
    client_ip = request.client.host

    msg = Message(
        username=anon_id,
        text=text.strip(),
        ip_address=client_ip,
        real_username=user.username  # visible to admin only
    )
    db.add(msg)
    db.commit()

    return RedirectResponse("/", status_code=303)

from fastapi.responses import PlainTextResponse

@app.get("/admin/logs", response_class=PlainTextResponse)
def get_logs_cli(username: str = Depends(verify_admin)):
    db = SessionLocal()
    messages = db.query(Message).order_by(Message.timestamp).all()

    lines = []
    for m in messages:
        timestamp_str = m.timestamp.strftime("%Y-%m-%d %H:%M")
        line = f"[{timestamp_str}] {m.username} ({m.ip_address}): {m.text}"
        lines.append(line)

    return "\n".join(lines)

