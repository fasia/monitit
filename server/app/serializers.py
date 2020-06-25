from marshmallow import Schema, fields, ValidationError
from app.server import ma

class UserSerializer(ma.Schema):
    class Meta:
        fields = ('id', 'email')

user_serializer = UserSerializer()
users_serializer = UserSerializer(many=True)


class UnitSerializer(ma.Schema):
    class Meta:
        fields = ('id', 'name')

unit_serializer = UnitSerializer()
units_serializer = UnitSerializer(many=True)

class RecipeItemSerializer(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'qty', 'unit', 'recipe_id', 'ingredients')
    
    unit = ma.Nested(UnitSerializer, many = True)
    #recipe = ma.Nested(RecipeSerializer)

recipeItem_serializer = RecipeItemSerializer()
recipeItems_serializer = RecipeItemSerializer(many=True)

class RecipeSerializer(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'instruction', 'price', 'created_at', 'owner_id', 'user', 'recipeitems')
    
    user = ma.Nested(UserSerializer)
    recipeitems = ma.Nested(RecipeItemSerializer, many= True)

recipe_serializer = RecipeSerializer()
recipes_serializer = RecipeSerializer(many=True)


""" class CommentSerializer(Serializer):

    class Meta:
        fields= ("id", "content", "user_id", "post_id")

class LikeSerializer(Serializer):

    class Meta:
        fields = ("id", "user_id", "post_id", "comment_id")

class PutSerializer(Serializer):

    class Meta:
        fields = ("id", "title", "body", "user", "created_at")
"""