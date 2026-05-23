# ds_protocol.py
# AKASH SAHU
# SAHUA4@UCI.EDU
# 34488929

import json
import time
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def join(username: str, password: str) -> str:
    """Create a JSON join message."""
    return json.dumps({
        "join": {
            "username": username,
            "password": password,
            "token": ""
        }
    })


def post(token: str, entry: str) -> str:
    """Create a JSON post message."""
    return json.dumps({
        "token": token,
        "post": {
            "entry": entry,
            "timestamp": str(time.time())
        }
    })


def bio(token: str, entry: str) -> str:
    """Create a JSON bio message."""
    return json.dumps({
        "token": token,
        "bio": {
            "entry": entry,
            "timestamp": str(time.time())
        }
    })


def extract_json(json_msg: str) -> DataTuple:
    """
    Parse a JSON response from the DSP server.
    Returns DataTuple with type, message, and token fields.
    """
    try:
        json_obj = json.loads(json_msg)
        resp_type = json_obj['response']['type']
        message = json_obj['response'].get('message', '')
        token = json_obj['response'].get('token', '')
        return DataTuple(resp_type, message, token)
    except json.JSONDecodeError:
        return DataTuple('error', 'Json cannot be decoded.', '')
    except KeyError:
        return DataTuple('error', 'Invalid response format.', '')
