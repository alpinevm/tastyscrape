import logging

from tastyscrape.models import session

LOGGER = logging.getLogger(__name__)


def create_new_session(username, password):
    return session.TastyAPISession(username, password)
