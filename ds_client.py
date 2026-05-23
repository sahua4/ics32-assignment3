# ds_client.py
# AKASH SAHU
# SAHUA4@UCI.EDU
# 34488929

import socket
import ds_protocol


def _send_command(f_send, f_recv, msg: str) -> ds_protocol.DataTuple:
    f_send.write(msg + '\r\n')
    f_send.flush()
    resp = f_recv.readline()
    return ds_protocol.extract_json(resp)


def _join(f_send, f_recv, username: str, password: str) -> str:
    msg = ds_protocol.join(username, password)
    result = _send_command(f_send, f_recv, msg)
    if result.type == 'ok':
        return result.token
    return None


def _post(f_send, f_recv, token: str, message: str) -> bool:
    msg = ds_protocol.post(token, message)
    result = _send_command(f_send, f_recv, msg)
    return result.type == 'ok'


def _bio(f_send, f_recv, token: str, bio_entry: str) -> bool:
    msg = ds_protocol.bio(token, bio_entry)
    result = _send_command(f_send, f_recv, msg)
    return result.type == 'ok'


def send(server: str, port: int, username: str, password: str,
         message: str, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both.

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    has_message = message and message.strip()
    has_bio = bio and bio.strip()

    if not has_message and not has_bio:
        return False

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server, int(port)))
            f_send = sock.makefile('w')
            f_recv = sock.makefile('r')

            token = _join(f_send, f_recv, username, password)
            if token is None:
                return False

            if has_message:
                if not _post(f_send, f_recv, token, message):
                    return False

            if has_bio:
                if not _bio(f_send, f_recv, token, bio):
                    return False

            return True

    except Exception:
        return False