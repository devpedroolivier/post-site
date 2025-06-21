# app/main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

load_dotenv()  # Carrega variáveis do .env

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse(request, "home.html", {})

@app.get("/contato", response_class=HTMLResponse)
async def contato(request: Request):
    return templates.TemplateResponse(request, "contato.html", {})

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
        return templates.TemplateResponse(request, "contato.html", {
            "mensagem_sucesso": "Mensagem enviada com sucesso!"
        })
    except Exception as e:
        return templates.TemplateResponse(request, "contato.html", {
            "mensagem_erro": f"Erro ao enviar: {str(e)}"
        })

@app.get("/servicos", response_class=HTMLResponse)
async def servicos(request: Request):
    return templates.TemplateResponse(request, "servicos.html", {})

@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio(request: Request):
    projetos = [
        {
            "titulo": "Automação Reclamações Sabesp",
            "descricao": "Extração de dados do Power BI, análise com Pandas e envio via WhatsApp e Outlook.",
            "imagem": "reclamacoes.png",
            "tags": ["Python", "Selenium", "WhatsApp API", "Outlook"],
            "ano": 2025
        },
        {
            "titulo": "Agente IA via WhatsApp",
            "descricao": "Sistema com FastAPI e API oficial Meta para gerar relatórios por comando.",
            "imagem": "agente_ia.png",
            "tags": ["FastAPI", "Meta API", "Relatórios", "Comandos Inteligentes"],
            "ano": 2025
        },
        {
            "titulo": "Aplicação Web – Monitoramento Falta d’Água",
            "descricao": "Visualização interativa de gráficos por setor e polo com dados em tempo real, utilizando FastAPI e Chart.js.",
            "imagem": "aplicacao_web.png",
            "tags": ["FastAPI", "Chart.js", "Pandas", "Power BI"],
            "ano": 2025
        }
    ]
    return templates.TemplateResponse("portfolio.html", {"request": request, "projetos": projetos})


@app.get("/quem-somos", response_class=HTMLResponse)
async def quem_somos(request: Request):
    return templates.TemplateResponse(request, "quem-somos.html", {})

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
