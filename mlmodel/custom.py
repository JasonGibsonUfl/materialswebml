"""
contians custom fields for models
"""
from django.db import models
import pickle
import numpy as np
import ast
from collections import defaultdict


class NumpyArrayField(models.TextField):
    description = "Stores a Numpy ndarray."
    # __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(NumpyArrayField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, list):
            value = np.array(list)
        if isinstance(value, np.ndarray):
            return value

        if not value:
            return np.array([])

        return np.array(pickle.loads(str(value)))

    def get_prep_value(self, value):
        if isinstance(value, list):
            return str(value)
        elif isinstance(value, np.ndarray):
            return str(value.tolist())
            # return pickle.dumps(value.tolist())
        else:
            raise TypeError("%s is not a list or numpy array" % value)


class DictField(models.TextField):
    # __metaclass__ = models.SubfieldBase
    description = "Stores a python dictionary"

    def __init__(self, *args, **kwargs):
        super(DictField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = {}

        if isinstance(value, dict):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        if isinstance(value, defaultdict):
            value = dict(value)

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class JSONField(models.TextField):
    # __metaclass__ = models.SubfieldBase
    description = "Stores a python dictionary"

    def __init__(self, *args, **kwargs):
        super(JSONField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return value
        if not isinstance(value, str):
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        print("get prep value", value)
        return json.dumps(value)
