from rest_framework import serializers
from pybo.models import User, Tale, Child, Ttssetting, Qna, Rate, Likes, Favorite, Commentlikes, RecentReads


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['account', 'passwd', 'nickname', 'email', 'mobile']


class TaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tale
        fields = ['num', 'imglink', 'title', 'content', 'likes', 'reviews', 'views']


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['num', 'name', 'age', 'type', 'personality', 'parent']


class TtsSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ttssetting
        fields = ['num', 'ttsspeed', 'ttsvoice', 'childnum']

class QnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qna
        fields = ['num', 'q', 'a', 'direction', 'childnum', 'parent', 'likes', 'talenum']

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['num', 'rate', 'childnum', 'talenum']

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['num', 'childnum', 'talenum']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['num', 'childnum', 'talenum']

class CommentlikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentlikes
        fields = ['num', 'childnum', 'commentid']

class RecentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentReads
        fields = ['num', 'childnum', 'talenum', 'readdate']