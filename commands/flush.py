from alembic.config import Config
from alembic import command

def run():
    cfg = Config("alembic.ini")

    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")