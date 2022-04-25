import json
import logging

from pydantic import AnyUrl
from requests import request
from requests.models import Response

from app.core.config import settings

logger = logging.getLogger(__name__)


def get_name_service(url):
    services = [settings.IAM_SERVICE_URL]
    for index, service in enumerate(services):
        if service in url:
            if index == 0:
                return 'Iam service'
    return 'Unknow service'


def call_api(url: AnyUrl, token_iam: str = None, method: str = 'get', params: dict = None,
             data: dict = None) -> Response:
    try:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if token_iam:
            headers['Authorization'] = token_iam
        response = request(method=method, url=url,
                           headers=headers, json=data, params=params)

        if response.status_code // 100 > 2:
            logger.warning("Calling URL: %s, message: %s" % (url, response.json()))
        else:
            logger.info("Calling URL: %s, message: Success" % (url))
        logger.info("Body request: " + str(data) + ", params: " + str(params))
        return response
    except Exception as e:
        logger.warning("cannot Connect IAM")
