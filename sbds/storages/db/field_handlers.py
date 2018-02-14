# -*- coding: utf-8 -*-
import structlog
from sbds import sbds_json

logger = structlog.get_logger(__name__)


def amount_field(value, num_func=int, no_value=0):
    if not value:
        return num_func(no_value)
    try:
        return num_func(value.split()[0])
    except Exception as e:
        logger.error('amount handler error', original=value, num_func=num_func, no_value=no_value, error=e)
        return num_func(no_value)


def amount_symbol_field(value, no_value=''):
    if not value:
        return no_value
    try:
        return value.split()[1]
    except Exception as e:
        logger.error('amount_symbol handler error', original=value, no_value=no_value, error=e)
        return no_value


def comment_body_field(value):
    if isinstance(value, bytes):
        return value.decode('utf8')
    return value


def json_string_field(value):
    if value:
        try:
            return sbds_json.dumps(value)
        except Exception as e:
            logger.exception(e)
            return None
