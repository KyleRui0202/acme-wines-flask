"""
    manage
    ~~~~~~

    This script provides ready-to-use commands for
    * database migration
    * running local development server
"""

from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade, downgrade

from acmewines import app, db
from acmewines.utils.populate import seed_test_data

migrate = Migrate(app, db)

manager = Manager(app)

from acmewines.models import Order

# Migration commands 
manager.add_command('db_migration', MigrateCommand)

# Run local server
manager.add_command('runserver', Server('localhost', port=8888))

# Interactive project shell
def _make_shell_context():
   return dict(app=app, db=db)
manager.add_command('shell', Shell(make_context=_make_shell_context))

@manager.command
def initdb():
    """Create the database through migration."""

    upgrade()

@manager.command
def cleanupdb():
    """Clear up the database through migration."""

    downgrade(revision='base')
    upgrade()

@manager.command
def seeddb(initdb=False, cleanupdb=False):
    """Seed fake data into the database.
    To create new database use the '-i' or '--initdb' option
    To clear up the existing database use the '-c' or '--cleanupdb' option.
    """

    if initdb:
        print("Creating database...")
        upgrade()

    if cleanupdb:
        print("Cleaning up database...")
        downgrade(revision='base')
        upgrade()

    seeded_data = seed_test_data()
    print("Created and saved test data into database: %r" % seeded_data)

if __name__ == '__main__':
    manager.run()
