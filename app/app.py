import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from . import api_settings, health_router
from .bert_ner import v1_router

logger = logging.getLogger(__name__)

app = FastAPI(title="Named Entity Recognition (NER) API",
              version=api_settings.version if api_settings.version else "dev",
              description="An API that annotates Estonian named entities using a BERT language model. "
                          "Developed by TartuNLP - the NLP research group of the University of Tartu.",
              terms_of_service="https://www.tartunlp.ai/andmekaitsetingimused",
              license_info={
                  "name": "MIT license",
                  "url": "https://github.com/TartuNLP/bert-ner-api/blob/main/LICENSE"
              },
              contact={
                  "name": "TartuNLP",
                  "url": "https://tartunlp.ai",
                  "email": "ping@tartunlp.ai",
              })

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logger.debug(f"{request}: {exc_str}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc_str}
    )


app.include_router(v1_router, prefix="/v1")
app.include_router(health_router, prefix="/health", include_in_schema=False)