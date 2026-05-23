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


def cmd_edit(args, profile, path):
    """
    Handle E command: edit profile fields.
    Supports: -usr -pwd -bio -addpost -delpost -srv
    Stops processing on first error.
    Returns updated profile.
    """
    if profile is None or path is None:
        print("ERROR")
        return profile

    i = 0
    while i < len(args):
        opt = args[i]
        if opt == '-usr':
            if i + 1 >= len(args):
                print("ERROR")
                return profile
            val = args[i + 1]
            if ' ' in val or not val.strip():
                print("ERROR")
                return profile
            profile.username = val
            i += 2
        elif opt == '-pwd':
            if i + 1 >= len(args):
                print("ERROR")
                return profile
            val = args[i + 1]
            if ' ' in val or not val.strip():
                print("ERROR")
                return profile
            profile.password = val
            i += 2
        elif opt == '-bio':
            if i + 1 >= len(args):
                print("ERROR")
                return profile
            val = args[i + 1]
            if not val.strip():
                print("ERROR")
                return profile
            profile.bio = val
            i += 2
        elif opt == '-addpost':
            if i + 1 >= len(args):
                print("ERROR")
                return profile
            entry = args[i + 1]
            if not entry.strip():
                print("ERROR")
                return profile
            profile.add_post(Post(entry))
            i += 2
        elif opt == '-delpost':
            if i + 1 >= len(args):
                print("ERROR")
                return profile
            try:
                post_id = int(args[i + 1])
                if not profile.del_post(post_id):
                    print("ERROR")
                    return profile
            except ValueError:
                print("ERROR")
                return profile
            i += 2
        elif opt == '-srv':
            if i + 1 >= len(args):
                print("ERROR")
                return profile
            profile.dsuserver = args[i + 1]
            i += 2
        else:
            print("ERROR")
            return profile

    try:
        profile.save_profile(str(path))
    except DsuFileError:
        print("ERROR")

    return profile


def cmd_print(args, profile):
    """
    Handle P command: print profile data to screen.
    Supports: -usr -pwd -bio -posts -post [ID] -all
    """
    if profile is None:
        print("ERROR")
        return

    i = 0
    while i < len(args):
        opt = args[i]
        if opt == '-usr':
            print(profile.username)
            i += 1
        elif opt == '-pwd':
            print(profile.password)
            i += 1
        elif opt == '-bio':
            print(profile.bio)
            i += 1
        elif opt == '-posts':
            posts = profile.get_posts()
            if not posts:
                print("No posts found.")
            for idx, p in enumerate(posts):
                print(f"{idx}: {p.entry}")
            i += 1
        elif opt == '-post':
            if i + 1 >= len(args):
                print("ERROR")
                return
            try:
                post_id = int(args[i + 1])
                posts = profile.get_posts()
                print(posts[post_id].entry)
            except (ValueError, IndexError):
                print("ERROR")
                return
            i += 2
        elif opt == '-all':
            print(f"Username: {profile.username}")
            print(f"Password: {profile.password}")
            print(f"Bio: {profile.bio}")
            print(f"Server: {profile.dsuserver}")
            posts = profile.get_posts()
            if not posts:
                print("No posts found.")
            for idx, p in enumerate(posts):
                print(f"{idx}: {p.entry}")
            i += 1
        else:
            print("ERROR")
            return


def cmd_delete(args):
    """Handle D command: delete a .dsu file."""
    if len(args) != 1:
        print("ERROR")
        return

    file_path = Path(args[0])

    if not file_path.exists() or file_path.suffix != '.dsu':
        print("ERROR")
        return

    print(f"{file_path} DELETED")
    file_path.unlink()


def cmd_read(args):
    """Handle R command: read raw contents of a .dsu file."""
    if len(args) != 1:
        print("ERROR")
        return

    file_path = Path(args[0])

    if not file_path.exists() or file_path.suffix != '.dsu':
        print("ERROR")
        return

    content = file_path.read_text()

    if not content.strip():
        print("EMPTY")
        return

    print(content, end='')


def cmd_publish(profile, path, port=DEFAULT_PORT):
    """
    Publish the most recent post and/or bio to the DSP server.
    Returns True on success, False on failure.
    """
    if profile is None or path is None:
        print("ERROR: No profile loaded.")
        return False

    if not profile.dsuserver:
        print("ERROR: No server configured.")
        return False

    posts = profile.get_posts()
    message = posts[-1].entry if posts else ''
    bio_val = profile.bio if profile.bio and profile.bio.strip() else None

    if not message.strip() and bio_val is None:
        print("ERROR: Nothing to publish.")
        return False

    result = ds_client.send(
        profile.dsuserver,
        port,
        profile.username,
        profile.password,
        message,
        bio_val
    )

    if result:
        print("Successfully published to server.")
    else:
        print("ERROR: Failed to publish to server.")

    return result


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
    elif command == 'E':
        profile = cmd_edit(parts[1:], profile, path)
    elif command == 'P':
        cmd_print(parts[1:], profile)
    elif command == 'D':
        cmd_delete(parts[1:])
    elif command == 'R':
        cmd_read(parts[1:])
    elif command == 'T':
        port = DEFAULT_PORT
        if len(parts) > 1:
            try:
                port = int(parts[1])
            except ValueError:
                print("ERROR")
                return profile, path
        cmd_publish(profile, path, port)
    else:
        print("ERROR")

    return profile, path