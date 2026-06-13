from alembic import command
from commands import cfg

def run():
    command.upgrade(cfg, "head")