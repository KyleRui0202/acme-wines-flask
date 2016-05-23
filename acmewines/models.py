from datetime import datetime

from sqlalchemy.dialects.postgresql import JSON as PSQLJSON

from acmewines.extensions import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(128), nullable=False, index=True)
    email = db.Column(db.String(254), nullable=False, index=True)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    valid = db.Column(db.Boolean)
    validation_failure = db.Column(PSQLJSON)
    created_at = db.Column(db.DateTime, server_default=db.text('NOW()'))
    updated_at = db.Column(db.DateTime, server_default=db.text('NOW()'), onupdate=datetime.now)
    ix_state_zipcode = db.Index('ix_state_zipcode', state, zipcode)

