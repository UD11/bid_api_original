from rest_framework import serializers

from bidapp.models import User, team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'email', 'username', 'password', 'year', 'user_image',
                  'player_position', 'owner', 'coowner' ,'player_value', 'marquee', 'captain', 'department', 'host','sold','vicecaptain','team']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class teamSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    coowner = UserSerializer(read_only=True)
    captain = UserSerializer(read_only=True)
    vicecaptain = UserSerializer(read_only=True)
    marquee = UserSerializer(read_only=True)
    players = UserSerializer(many=True, read_only=True)

    class Meta:
        model = team

        fields = ['id','team_name','captain','owner','coowner','players','pot','vicecaptain','marquee']