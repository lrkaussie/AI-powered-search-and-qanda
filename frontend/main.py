"""Frontend application for document search and Q&A."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from frontend import routes

# Initialize FastAPI app
app = FastAPI(title="Document Q&A Frontend")

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="frontend/templates")

# Register routes
app.get("/")(routes.index)
app.post("/upload")(routes.upload_document)
app.post("/search")(routes.search_documents)
app.post("/ask")(routes.ask_question)
