from rest_framework import serializers


class MinLengthValidator(object):
    def __init__(self, min_size):
        self.min_size = min_size

    def __call__(self, value):
        if len(value) < self.min_size:
            raise serializers.ValidationError('Value too short')


class SpecialCharValidator(object):
    def __init__(self, special_chars):
        if not type(special_chars) is list:
            raise ValueError("special_chars must be list")
        self.special_chars = special_chars

    def __call__(self, value):
        for i in value:
            if i in self.special_chars:
                raise serializers.ValidationError("Cannot contain {0}".format(self.special_chars))