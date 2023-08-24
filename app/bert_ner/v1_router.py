import logging

from fastapi import APIRouter

from . import RequestModel, ResponseModel, ErrorMessage, ner_tagger

LOGGER = logging.getLogger(__name__)

v1_router = APIRouter(tags=["v1"])


@v1_router.post('/', include_in_schema=False)
@v1_router.post('', response_model=ResponseModel,
                description="Submit a NER request.",
                responses={
                    200: {"model": ResponseModel},
                    422: {"model": ErrorMessage},
                    408: {"model": ErrorMessage},
                    500: {"model": ErrorMessage}
                })
async def ner(body: RequestModel):
    LOGGER.debug(f"Request: {body}")
    response = ner_tagger.process_request(body)
    LOGGER.debug(f"Response: {response.dict()}")
    return response
