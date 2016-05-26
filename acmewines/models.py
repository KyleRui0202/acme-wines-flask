from datetime import datetime, date

from sqlalchemy.dialects.postgresql import JSON as PSQLJSON

from acmewines import db

class Order(db.Model):
    id_column = db.Column('id', db.Integer, primary_key=True, autoincrement=False)
    name_column = db.Column('name', db.String(128), nullable=True, index=True)
    email_column = db.Column('email', db.String(254), nullable=True, index=True)
    state_column = db.Column('state', db.String(2), nullable=True)
    zipcode_column = db.Column('zipcode', db.String(10), nullable=True)
    birthday_column = db.Column('birthday', db.Date, nullable=True)
    valid = db.Column(db.Boolean, nullable=True)
    validation_failure = db.Column(PSQLJSON, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.text('NOW()'))
    updated_at = db.Column(db.DateTime, server_default=db.text('NOW()'),
        onupdate=datetime.now)
    ix_state_zipcode = db.Index('ix_state_zipcode', state_column, zipcode_column)

    # Properties
    @property
    def name(self):
        """Get the name of the orderer"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.strip()
        validation_errors = self._validate_name(self._name)
        self._update_validation_failure(validation_errors)

    @property
    def email(self):
        """Get the email of the orderer"""
        return self._email

    @email.setter
    def email(self, value):
        self._email = value.strip().lower()
        validation_errors = self._validate_email(self._email)
        self._update_validation_failure(validation_errors)

    @property
    def state(self):
        """Get the state of the order"""
        return self._state

    @state.setter
    def state(self, value):
        self._state = value.strip().upper()
        validation_errors = self._validate_state(self._state)
        self._update_validation_failure(validation_errors)

    @property
    def zipcode(self):
        """Get the zipcode of the order"""
        return self._zipcode

    @zipcode.setter
    def zipcode(self, value):
        self._zipcode = value.strip()
        validation_errors = self._validate_zipcode(self._zipcode)
        self._update_validation_failure(validation_errors)

    @property
    def birthday(self):
        """Get the birthday of the orderer"""
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        self._birthday, validation_errors =\
            self._parse_and_validate_birthday(value.strip())
        self._update_validation_failure(validation_errors)

    def __init__(self, id, name=None, email=None,
        state=None, zipcode=None, birthday=None):
        self.id = id
        self.valid = None
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

    def _update_validation_failure(validation_errors):
        if validation_errors:
            if self.validation_failure is None:
                self.validation_failure = {}
            self.validation_failure.update(validation_errors)
            if self.valid or self.valid is None:
                self.valid = False

    def _parse_required_field(field, value):
        is_valid = True

        if value:
            setattr(self, field, value)
            field_validation_method = getattr(self, '_validate_' + field)
            validation_errors = field_validation_method(value)
            if valid_errors:
                is_valid = False
                self.validation_failure.update(validation_errors)
        else:
            is_valid = False
            self.validation_failure['required_'+field] = 'The ' + field +\
                ' is missing'

        if self.valid and not is_valid:
            self.valid = False
        
    def _validate_name(value):
        return None 

    def _validate_email(value):
        from validate_email import validate_email
        is_valid = validate_email(value)
        if is_valid:
            return None
        else:
            return {'email_validation': 'The email address is not valid'}

    def _validate_state(value):
        from acmewines.configs.validation import states, states_not_allowed
        if value in states:
            if value in states_not_allowed:
                return {'allowed_states': "We don't ship to " + value}
            else:
                return None
        else:
            return {'state_validation': value + ' is not a valid/allowed' +\
                ' U.S. state abbreviation'}

    def _validate_zipcode(value):
        from acmewines.configs.validation import zipcode_pattern, zipcode_max_digit_sum
        is_valid = re.match('\d{5}([\-]\d{4})?$', value)
        if is_valid:
            zipcode_digit_sum = 0
            for digit in digit_only_zipcode:
                if digit != '-':
                    zipcode_digit_sum += int(digit)
            if zipcode_digit_sum > zipcode_max_digit_sum:
                return {'zip_code_sum': 'Your zipcode is too large (>' +\
                    zipcode_max_digit_sum + ')'}
            else:
                return None
        else:
            return {'zipcode_validation': value + ' is not a valid' +\
                '5-digit zipcode (e.g., 00000) or 9-digit zipcode (e.g., 00000-0000)'}

    def _parse_and_validate_birthday(value):
        parsed_birthday = None
        validation_errors = None
        from acmewines.configs.validation import birthday_format, min_age
        try:
             parsed_birthday = datetime.strptime(value, birthday_format).date()
        except ValueError:
             pass
        if parsed_birthday:
            today = date.today()
            max_birth_date = date(today.year-21, today.month, today.day)
            if parsed_birthday > max_birth_date:
                validation_errors = {'age_restriction': 'You must be ' +\
                    min_age + ' or older to order'}
        else:
            validation_errors = {'birtday_validation': value +\
                ' is not a valid birthday format: ' + birthday_format}
        return (parsed_birthday, validation_errors)
