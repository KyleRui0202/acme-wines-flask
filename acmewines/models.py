import re

from datetime import datetime, date
from sqlalchemy.dialects.postgresql import JSON as PSQLJSON

from flask import json

from acmewines import db

class Order(db.Model):
    __tablename__ = 'orders'
    __mapper_args__ = {
        'exclude_properties': ['created_at', 'updated_at']
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name_column = db.Column('name', db.String(128), nullable=True, index=True)
    email_column = db.Column('email', db.String(254), nullable=True, index=True)
    state_column = db.Column('state', db.String(30), nullable=True)
    zipcode_column = db.Column('zipcode', db.String(20), nullable=True)
    birthday_column = db.Column('birthday', db.Date, nullable=True)
    valid = db.Column(db.Boolean, nullable=True)
    validation_failure = db.Column(PSQLJSON, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.text('NOW()'))
    updated_at = db.Column(db.DateTime, server_default=db.text('NOW()'),
        onupdate=datetime.now)
    ix_state_zipcode = db.Index('ix_orders_state_zipcode', state_column, zipcode_column)

    _visible = ('id', 'name', 'email', 'state', 'zipcode', 'birthday',
        'valid', 'validation_failure')

    from acmewines.configs.validation import required_fields
    _required = required_fields

    # Properties
    @property
    def name(self):
        """Get the name of the orderer"""
        return self.name_column

    @name.setter
    def name(self, value):
        self.name_column = value.strip()
        validation_errors = self._validate_name(self.name_column)
        self._update_validation_failure(validation_errors)

    @property
    def email(self):
        """Get the email of the orderer"""
        return self.email_column

    @email.setter
    def email(self, value):
        self.email_column = value.strip().lower()
        validation_errors = self._validate_email(self.email_column)
        self._update_validation_failure(validation_errors)

    @property
    def state(self):
        """Get the state of the order"""
        return self.state_column

    @state.setter
    def state(self, value):
        self.state_column = value.strip().upper()
        validation_errors = self._validate_state(self.state_column)
        self._update_validation_failure(validation_errors)

    @property
    def zipcode(self):
        """Get the zipcode of the order"""
        return self.zipcode_column

    @zipcode.setter
    def zipcode(self, value):
        self.zipcode_column = value.strip()
        validation_errors = self._validate_zipcode(self.zipcode_column)
        self._update_validation_failure(validation_errors)

    @property
    def birthday(self):
        """Get the birthday of the orderer"""
        if self.birthday_column:
            return self.birthday_column.isoformat()
        else:
            return None

    @birthday.setter
    def birthday(self, value):
        self.birthday_column, validation_errors =\
            self._parse_and_validate_birthday(value.strip())
        self._update_validation_failure(validation_errors)

    def __init__(self, id, name=None, email=None,
        state=None, zipcode=None, birthday=None):
        self.id = id
        self.valid = True
        self.validation_failure = None

        if name:
            self.name = name
        if email:
            self.email = email
        if state:
            self.state = state
        if zipcode:
            self.zipcode = zipcode
        if birthday:
            self.birthday = birthday

    def __repr__(self):
        return '<Order: id=%d>' % self.id

    def _update_validation_failure(self, validation_errors):
        if validation_errors:
            if self.validation_failure is None:
                self.validation_failure = {}
            for error_name in validation_errors:
                if validation_errors[error_name]:
                    self.validation_failure[error_name] =\
                        validation_errors[error_name]
                elif error_name in self.validation_failure:
                    del self.validation_failure[error_name]
            if self.validation_failure:
                if self.valid != False:
                    self.valid = False
            else:
                self.validation_failure = None
                if self.valid != True:
                    self.valid = True

    def _validate_missing_fields(self):
        validation_errors = {}
        for field in Order._required:
            if getattr(self, field, None) is None:
                validation_errors['required_'+field] =\
                    'The %s is missing' % field
        return validation_errors or None
     
    def _validate_name(self, value):
        return None

    def _validate_email(self, value):
        email_errors = {'email_validation': None}
        from validate_email import validate_email
        is_valid = validate_email(value)
        if not is_valid:
            email_errors['email_validation'] =\
                'The email address is not valid'
        return email_errors

    def _validate_state(self, value):
        state_errors = {'state_validation': None,
            'allowed_states': None}
        from acmewines.configs.validation import (
            states, states_not_allowed)
        if value in states:
            if value in states_not_allowed:
                state_errors['allowed_states'] =\
                    "We don't ship to " + value
        else:
            state_errors['state_validation'] = value +\
                ' is not a valid/allowed U.S. state abbreviation'
        return state_errors

    def _validate_zipcode(self, value):
        zipcode_errors = {'zipcode_validation': None,
            'zipcode_digit_sum': None}
        from acmewines.configs.validation import (
            zipcode_pattern, zipcode_max_digit_sum)
        is_valid = re.match(zipcode_pattern, value)
        if is_valid:
            zipcode_digit_sum = 0
            for digit in value:
                if digit != '-':
                    zipcode_digit_sum += int(digit)
            if zipcode_digit_sum > zipcode_max_digit_sum:
                zipcode_errors['zipcode_digit_sum'] =\
                    "The sum of zipcode's digits " +\
                    'is too large (> %d)' % zipcode_max_digit_sum
        else:
            zipcode_errors['zipcode_validation'] = value + ' is not a valid' +\
                '5-digit (e.g., 00000) or 9-digit (e.g., 00000-0000) zipcode'
        return zipcode_errors

    def _parse_and_validate_birthday(self, value):
        parsed_birthday = None
        birthday_errors = {'birthday_validation': None,
            'age_restriction': None}
        from acmewines.configs.validation import (
            birthday_format, min_age)
        try:
            parsed_birthday = datetime.strptime(value, birthday_format).date()
        except ValueError:
            pass
        if parsed_birthday:
            today = date.today()
            max_birth_date = date(today.year-21, today.month, today.day)
            if parsed_birthday > max_birth_date:
                birthday_errors['age_restriction'] =\
                    'You must be %d or older to order' % min_age
        else:
            birthday_errors['birtday_validation'] =\
                '%s is not a valid birthday format: %s' %\
                (value, birthday_format)
        return parsed_birthday, birthday_errors

    def toDict(self):
        fieldDict = {}
        for field_name in Order._visible:
            field_value = getattr(self, field_name, None)
            if field_value is not None:
                fieldDict[field_name] = field_value
        return fieldDict

    def save(self):
        missing_field_errors = self._validate_missing_fields()
        self._update_validation_failure(missing_field_errors)  
        db.session.add(self)
        db.session.commit()
