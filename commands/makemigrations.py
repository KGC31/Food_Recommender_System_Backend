from alembic.config import Config
from alembic import command

cfg = Config("alembic.ini")


def run(args):
    message = " ".join(args) if args else "auto migration"
    command.revision(cfg, autogenerate=True, message=message)