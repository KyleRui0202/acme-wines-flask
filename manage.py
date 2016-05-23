from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from acmewines import app, db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db_migration', MigrateCommand)

if __name__ == '__main__':
    manager.run()
