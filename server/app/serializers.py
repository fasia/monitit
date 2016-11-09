from marshmallow import Serializer, fields

class UserSerializer(Serializer):
    class Meta:
        fields = ("id", "email")

class PostSerializer(Serializer):
    user = fields.Nested(UserSerializer)

    class Meta:
        fields = ("id", "title", "body", "user", "created_at")

class CommentSerializer(Serializer):

    class Meta:
        fields= ("id", "content", "user_id", "post_id")

class LikeSerializer(Serializer):

    class Meta:
        fields = ("id", "user_id", "post_id", "comment_id")

class PutSerializer(Serializer):

    class Meta:
        fields = ("id", "title", "body", "user", "created_at")
