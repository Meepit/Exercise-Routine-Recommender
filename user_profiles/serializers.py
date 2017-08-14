from user_profiles.models import Profile
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from progress.serializers import ProgressSerializer
from progress.models import Progress
from recommender.serializers import RoutineSerializer
from django.contrib.auth.models import User
from user_profiles.validators import MinLengthValidator, SpecialCharValidator


class UserSerializer(serializers.Serializer):  # serializers.ModelSerializer):
    # class Meta:
    #     model = User
    #     email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    #     fields = ('username', 'password', 'first_name', 'email')
    #     # extra_kwargs allows for additional write fields that wont be displayed views
    #     extra_kwargs = {
    #         'password': {
    #             'write_only': True},
    #     }
    username = serializers.CharField(max_length=100, required=True, validators=[
        UniqueValidator(queryset=User.objects.all()), SpecialCharValidator(['"', '\'', '<', '>', ':', ';', '{', '}', '(', ')'])])
    password = serializers.CharField(max_length=100, required=True, validators=[MinLengthValidator(9),
        SpecialCharValidator(['"', '\'', '<', '>', ':', ';', '{', '}', '(', ')'])])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all()),
        SpecialCharValidator(['"', '\'', '<', '>', ':', ';', '{', '}', '(', ')'])])

    extra_kwargs = {
        'password': {
            'write_only': True
        },
    }

    # class Meta:
    #    fields = ('username', 'password', 'email')

    def create(self, validated_data):
        """ Overwrite create method to allow for password hashing on creation"""
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    lookup_field = 'user__username'
    user = UserSerializer(many=False, read_only=True)
    routine = RoutineSerializer(many=False)
    # routine = serializers.HyperlinkedRelatedField(view_name='routine-detail', format='html', read_only=True)
    # get_progress = serializers.HyperlinkedIdentityField(many=True, view_name='progress-detail', format='html')
    get_progress = ProgressSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'routine', 'get_progress')
