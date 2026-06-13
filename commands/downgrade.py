from alembic import command
from commands import cfg

def run():
    command.downgrade(cfg, "-1")