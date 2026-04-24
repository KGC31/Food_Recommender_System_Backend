from alembic.config import Config
from alembic import command

cfg = Config("alembic.ini")


def run(args):
    command.downgrade(cfg, "-1")