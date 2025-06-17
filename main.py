# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

from fastapi import Form
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

@app.get("/contato", response_class=HTMLResponse)
async def contato(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request})

@app.post("/enviar-contato")
async def enviar_contato(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    mensagem: str = Form(...)
):
    corpo = f"Nome: {nome}\nE-mail: {email}\nMensagem:\n{mensagem}"
    msg = MIMEText(corpo)
    msg["Subject"] = "Novo contato via site POST"
    msg["From"] = os.getenv("EMAIL_REMETENTE")
    msg["To"] = os.getenv("EMAIL_DESTINO")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(os.getenv("EMAIL_REMETENTE"), os.getenv("EMAIL_SENHA"))
            smtp.send_message(msg)
        return templates.TemplateResponse("contato.html", {
            "request": request,
            "mensagem_sucesso": "Mensagem enviada com sucesso!"
        })
    except Exception as e:
        return templates.TemplateResponse("contato.html", {
            "request": request,
            "mensagem_erro": f"Erro ao enviar: {str(e)}"
        })

@app.get("/servicos", response_class=HTMLResponse)
async def servicos(request: Request):
    return templates.TemplateResponse("servicos.html", {"request": request})

@app.get("/quem-somos", response_class=HTMLResponse)
async def quem_somos(request: Request):
    return templates.TemplateResponse("quem_somos.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)