from django.contrib.auth.password_validation import validate_password
from user_profiles.models import Profile
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from recommender.models import Routine
from recommender.serializers import RoutineSerializer
from django.contrib.auth.models import User
from user_profiles.validators import MinLengthValidator, SpecialCharValidator


class UserSerializer(serializers.Serializer):
    """
    Create as a general serializer over model serializer to allow the addition of validators
    """
    first_name = serializers.CharField(max_length=30, required=True, validators=[
        SpecialCharValidator(['"', '\'', '<', '>', ':', ';', '{', '}', '(', ')'])])
    username = serializers.CharField(max_length=100, required=True, validators=[
        UniqueValidator(queryset=User.objects.all()), SpecialCharValidator(['"', '\'', '<', '>', ':', ';', '{', '}', '(', ')', " "])])
    password = serializers.CharField(max_length=100, required=True, write_only=True, validators=[MinLengthValidator(9),
        SpecialCharValidator(['"', '\'', '<', '>', ':', ';', '{', '}', '(', ')'])])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all()),
        SpecialCharValidator(['"', '\'', '<', '>', ':', ';', '{', '}', '(', ')'])])

    def create(self, validated_data):
        """ Overwrite create method to allow for password hashing on creation"""
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    routine_id added as an additional field to allow for simpler updating of nested fields.
    """
    lookup_field = 'user__username'
    user = UserSerializer(many=False, read_only=True)
    routine = RoutineSerializer(many=False, required=False)
    routine_id = serializers.CharField(max_length=3) # TODO: Add validator

    class Meta:
        model = Profile
        fields = ('id', 'user', 'routine', 'routine_id')

    def update(self, instance, validated_data):
        """
        :param instance: Profile instance
        :param ordered_dict created from JSON:
        :return: instance
        Routine is updated by querying for routine_id.
        """
        # TODO: Handle invalid routine_id probably by adding validator
        routine_id = validated_data.pop('routine_id')
        routine_obj = Routine.objects.get(pk=routine_id)
        instance.routine = routine_obj
        instance.save()
        return instance


class UpdatePasswordSerializer(serializers.Serializer):
    """
    Change password serializer
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(max_length=100, required=True, validators=[MinLengthValidator(9),
        SpecialCharValidator(['"', '\'', '<', '>', ':', ';', '{', '}', '(', ')'])])

    def validate_new_password(self, value):
        validate_password(value)
        return value