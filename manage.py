"""
    manage
    ~~~~~~

    This script provides ready-to-use commands for
    * database migration
    * running local development server
"""

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from acmewines import app, db

migrate = Migrate(app, db)

manager = Manager(app)

from acmewines.models import Order

# Migration commands 
manager.add_command('db_migration', MigrateCommand)

# Run local server
manager.add_command('runserver', Server('localhost', port=8888))

if __name__ == '__main__':
    manager.run()
