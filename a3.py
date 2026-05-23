# a3.py
# AKASH SAHU
# SAHUA4@UCI.EDU
# 34488929

from ui import process_command, cmd_publish, DEFAULT_PORT


def print_menu():
    """Print the friendly UI menu."""
    print("\n=============================")
    print("       DSU Journal A3")
    print("=============================")
    print("1. Create new journal (C)")
    print("2. Open existing journal (O)")
    print("3. Edit journal (E)")
    print("4. Print journal data (P)")
    print("5. Publish to server (T)")
    print("6. Delete file (D)")
    print("7. Read file (R)")
    print("8. Quit")
    print("=============================")
    print("Tip: Type commands directly or choose a number.")
    print("C format: C /path -n name -usr user -pwd pass")
    print("         [-bio bio] [-srv server]")
    print("E format: E -usr user -pwd pass -bio text")
    print("         -addpost post -delpost id")
    print("P format: P -all | -usr | -pwd | -bio")
    print("         -posts | -post id")


def run_admin_mode():
    """
    Admin mode: accepts raw commands until Q is entered.
    No prompts printed via input().
    """
    profile = None
    path = None

    while True:
        user_input = input()

        if not user_input.strip():
            print("ERROR")
            continue

        if user_input.strip().upper() == 'Q':
            break

        profile, path = process_command(user_input, profile, path)


def run_ui_mode(profile=None, path=None):
    """
    Friendly UI mode with numbered menu system.
    """
    print("\nWelcome to DSU Journal!")
    print("Your personal journaling program.\n")

    while True:
        print_menu()
        user_input = input("\nEnter command or number: ").strip()

        if not user_input:
            continue

        if user_input == '8' or user_input.upper() == 'Q':
            print("Goodbye!")
            break
        elif user_input == '1':
            print("\nCreate a new journal.")
            print("Format: C /path/to/dir -n name -usr username -pwd password")
            print("Optional: -bio 'your bio' -srv server_ip")
            cmd = input("Enter C command: ").strip()
            profile, path = process_command(cmd, profile, path)
            if path:
                print(f"Journal created: {path}")
        elif user_input == '2':
            print("\nOpen an existing journal.")
            print("Format: O /path/to/file.dsu")
            cmd = input("Enter O command: ").strip()
            profile, path = process_command(cmd, profile, path)
        elif user_input == '3':
            if profile is None:
                print("No journal loaded. Create or open one first.")
            else:
                print("\nEdit journal.")
                print("Options: -usr name -pwd pass -bio text -addpost 'post'")
                print("         -delpost id -srv server_ip")
                cmd = input("Enter E command: ").strip()
                profile, path = process_command('E ' + cmd, profile, path)
                print("Journal updated.")
        elif user_input == '4':
            if profile is None:
                print("No journal loaded. Create or open one first.")
            else:
                print("\nPrint options: -all -usr -pwd -bio -posts -post id")
                cmd = input("Enter P command: ").strip()
                process_command('P ' + cmd, profile, path)
        elif user_input == '5':
            if profile is None:
                print("No journal loaded. Create or open one first.")
            else:
                port_str = input(
                    f"Enter server port (default {DEFAULT_PORT}): ").strip()
                port = int(port_str) if port_str.isdigit() else DEFAULT_PORT
                cmd_publish(profile, path, port)
        elif user_input == '6':
            print("Format: D /path/to/file.dsu")
            cmd = input("Enter D command: ").strip()
            process_command(cmd, profile, path)
        elif user_input == '7':
            print("Format: R /path/to/file.dsu")
            cmd = input("Enter R command: ").strip()
            process_command(cmd, profile, path)
        else:
            profile, path = process_command(user_input, profile, path)


def main():
    """Entry point for the DSU Journal program."""
    first = input(
        "Welcome to DSU Journal!\n"
        "Type 'admin' for admin mode, or press Enter for the UI: "
    ).strip()

    if first.lower() == 'admin':
        run_admin_mode()
    else:
        profile = None
        path = None
        if first:
            profile, path = process_command(first, profile, path)
        run_ui_mode(profile, path)


if __name__ == "__main__":
    main()
