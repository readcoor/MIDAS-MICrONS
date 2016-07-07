import json
import numbers
from rest_framework import serializers
from django.core.validators import RegexValidator

class NameValidator(RegexValidator):
    regex = "^[a-zA-Z0-9_-]*$"
    message = u'Invalid Name.'


def validate_coords(string):
    try:
        data = json.loads(string)
    except ValueError: 
        raise serializers.ValidationError("Could not parse as JSON: '%s'" % string)        

    if not isinstance(data, list):
        raise serializers.ValidationError("Not a list of coordinates. '%s'" % (data,))
    for coord in data:
        if not isinstance(coord, list):
            raise serializers.ValidationError("Coordinate is not a list: %s" % (coord,))
        if not len(coord) == 3:
            raise serializers.ValidationError("Coordinate is not a triple: %s" % (coord,))
        if not all([isinstance(x, numbers.Number) for x in coord]):
            raise serializers.ValidationError("Non-number in coordinate: %s" % (coord,))
    return True 

