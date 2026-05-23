# ui.py
# AKASH SAHU
# SAHUA4@UCI.EDU
# 34488929

import shlex
from pathlib import Path
from Profile import Profile, Post, DsuFileError, DsuProfileError
import ds_client

DEFAULT_PORT = 3001


def cmd_create(args, profile, path):
    """
    Handle C command: create a new .dsu file.
    Format: C /path -n name -usr user -pwd pass [-bio bio] [-srv server]
    If file already exists, load it instead.
    Returns (profile, path).
    """
    try:
        n_index = args.index('-n')
        name = args[n_index + 1]
        dir_path = Path(args[0])
    except (ValueError, IndexError):
        print("ERROR")
        return profile, path

    if not dir_path.exists() or not dir_path.is_dir():
        print("ERROR")
        return profile, path

    file_path = dir_path / (name + '.dsu')

    if file_path.exists():
        return cmd_open([str(file_path)], profile, path)

    try:
        usr_index = args.index('-usr')
        username = args[usr_index + 1]
        pwd_index = args.index('-pwd')
        password = args[pwd_index + 1]
    except (ValueError, IndexError):
        print("ERROR")
        return profile, path

    if not username.strip() or not password.strip():
        print("ERROR")
        return profile, path

    if ' ' in username or ' ' in password:
        print("ERROR")
        return profile, path

    bio_val = ''
    try:
        bio_index = args.index('-bio')
        bio_val = args[bio_index + 1]
    except (ValueError, IndexError):
        pass

    server = '127.0.0.1'
    try:
        srv_index = args.index('-srv')
        server = args[srv_index + 1]
    except (ValueError, IndexError):
        pass

    file_path.touch()
    print(file_path)

    new_profile = Profile()
    new_profile.username = username
    new_profile.password = password
    new_profile.bio = bio_val
    new_profile.dsuserver = server

    try:
        new_profile.save_profile(str(file_path))
    except DsuFileError:
        print("ERROR")
        file_path.unlink()
        return profile, path

    return new_profile, file_path


def cmd_open(args, profile, path):
    """
    Handle O command: open and load an existing .dsu file.
    Returns (profile, path).
    """
    if len(args) != 1:
        print("ERROR")
        return profile, path

    file_path = Path(args[0])

    if not file_path.exists() or file_path.suffix != '.dsu':
        print("ERROR")
        return profile, path

    try:
        new_profile = Profile()
        new_profile.load_profile(str(file_path))
        print(f"Loaded: {file_path}")
        return new_profile, file_path
    except DsuProfileError:
        print("ERROR")
        return profile, path
    except DsuFileError:
        print("ERROR")
        return profile, path


def process_command(user_input, profile, path):
    """
    Parse and dispatch a single command string.
    Returns (profile, path) after processing.
    """
    try:
        parts = shlex.split(user_input)
    except ValueError:
        print("ERROR")
        return profile, path

    if not parts:
        print("ERROR")
        return profile, path

    command = parts[0].upper()

    if command == 'C':
        profile, path = cmd_create(parts[1:], profile, path)
    elif command == 'O':
        profile, path = cmd_open(parts[1:], profile, path)
    else:
        print("ERROR")

    return profile, path
