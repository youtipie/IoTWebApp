import uvicorn
from asgiref.wsgi import WsgiToAsgi

from app import create_app
from config import Config

app = WsgiToAsgi(create_app(Config))

if __name__ == "__main__":
    try:
        uvicorn.run("asgi:app", port=5000, log_level="info", reload=False)
    except KeyboardInterrupt:
        exit()
