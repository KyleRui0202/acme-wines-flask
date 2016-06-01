"""
    acmewines.tasks
    ~~~~~~~~~~~~~~~

    This module contains independent (synchonous/asynchronous) tasks.
""" 

from acmewines.models import Order

class OrderFilterTask(object):
    """ Provide a task to filter the output orders. """

    def __init__(self, url_params=None):
        self._allowed_filters = {'constraint': ['limit', 'offset', 'valid'],
            'field_match': ['name', 'email', 'state', 'zipcode'],
            'field_partial_match': ['name', 'email', 'zipcode']
        }
        self._query = Order.query.order_by(Order.id)
        self._effect_filter_params = {}
        if url_params:
            self._parse_filter_params(url_params)

    @property
    def effect_filter_params(self):
        """Get the effect filter parameters for the order filter task"""
        return self._effect_filter_params or None

    def _parse_filter_params(self, url_params):
        if 'constraint' in self._allowed_filters:
            self._parse_constraint_filters(url_params)
        if 'field_match' in self._allowed_filters:
            self._parse_fieldmatch_filters(url_params)
        if 'field_partial_match' in self._allowed_filters:
            self._parse_fieldpartialmatch_filters(url_params)

    def _parse_constraint_filters(self, url_params):
        for filter_name in self._allowed_filters['constraint']:
            if filter_name == 'valid':
                filter_value = url_params.get(filter_name, None,
                    type=self._cast_var_to_boolean)
            else:
                filter_value = url_params.get(filter_name, None,
                    type=self._cast_var_to_positive_int)
            if filter_value is not None:
                if 'constraint' not in self._effect_filter_params:
                    self._effect_filter_params['constraint'] = {}
                self._effect_filter_params['constraint'][filter_name] =\
                    filter_value

    def _parse_fieldmatch_filters(self, url_params):
        for field in self._allowed_filters['field_match']:
            filter_value = url_params.get(field + '_equals', '')
            if filter_value != '':
                if 'field_match' not in self._effect_filter_params:
                    self._effect_filter_params['field_match'] = {}
                self._effect_filter_params['field_match'][field] =\
                    filter_value

    def _parse_fieldpartialmatch_filters(self, url_params):
        for field in self._allowed_filters['field_partial_match']:
            filter_value = url_params.get(field + '_contains', '')
            if filter_value != '':
                if 'field_partial_match' not in self._effect_filter_params:
                    self._effect_filter_params['field_partial_match'] = {}
                self._effect_filter_params['field_partial_match'][field] =\
                    filter_value

    def _cast_var_to_boolean(self, value):
        parsed_value = value.lower()
        if parsed_value in ('1', 'true', 'yes'):
            return True
        elif parsed_value in ('0', 'false', 'no'):
            return False
        else:
            return None

    def _cast_var_to_positive_int(self, value):
        try:
            parsed_value = int(value)
        except ValueError:
            return None
        if parsed_value > 0:
            return parsed_value
        else:
           return None

    def run(self):
        for filter_type in self._effect_filter_params:
            for filter_name, filter_value in\
                self._effect_filter_params[filter_type].items():
                if filter_type == 'constraint':
                    if filter_name == 'limit':
                       self._query = self._query.limit(filter_value)
                    elif filter_name == 'offset':
                       self._query = self._query.offset(filter_value)
                    elif filter_name == 'valid':
                        self._query = self._query.filter_by(
                            valid = filter_value)
                elif filter_type == 'field_match':
                    self._query = self._query.filter(getattr(Order,
                        filter_name + '_column') == filter_value)
                elif filter_type =='field_partial_match':
                    self._query = self._query.filter(getattr(Order,
                        filter_name + '_column').ilike('%' + filter_value + '%'))
        return self._query.all()
