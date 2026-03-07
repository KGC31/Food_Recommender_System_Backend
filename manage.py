import sys
from alembic.config import Config
from alembic import command

cfg = Config("alembic.ini")

def main():
    if len(sys.argv) < 2:
        print_help()
        return

    cmd = sys.argv[1]
    comment = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None

    if cmd == "make_migrations":
        command.revision(cfg, autogenerate=True, message=comment or "auto migration")

    elif cmd == "migrate":
        command.upgrade(cfg, "head")

    elif cmd == "rollback":
        command.downgrade(cfg, "-1")

    elif cmd == "history":
        command.history(cfg)

    elif cmd == "current":
        command.current(cfg)

    elif cmd == "revision":
        command.revision(cfg, message=comment or "manual migration")

    else:
        print_help()


def print_help():
    print(
        """
        Available commands:

        make_migrations "message"   Create migration with autogenerate
        revision "message"          Create empty migration
        migrate                     Upgrade database to latest
        rollback                    Downgrade one migration
        history                     Show migration history
        current                     Show current database revision
        """
    )


if __name__ == "__main__":
    main()