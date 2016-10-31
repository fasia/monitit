from flask import g, request
from flask.ext import restful

from server import api, db, flask_bcrypt, auth
from models import User, Post,Comment, Like
from forms import UserCreateForm, SessionCreateForm, PostCreateForm, CommentCreateForm
from serializers import UserSerializer, PostSerializer, CommentSerializer


@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.user = user
    return flask_bcrypt.check_password_hash(user.password, password)


class UserView(restful.Resource):
    def post(self):
        form = UserCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return UserSerializer(user).data


class SessionView(restful.Resource):
    def post(self):
        form = SessionCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User.query.filter_by(email=form.email.data).first()
        if user and flask_bcrypt.check_password_hash(user.password, form.password.data):
            return UserSerializer(user).data, 201
        return '', 401


class PostListView(restful.Resource):
    def get(self):
        posts = Post.query.all()
        return PostSerializer(posts, many=True).data

    @auth.login_required
    def post(self):
        form = PostCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        post = Post(form.title.data, form.body.data)
        db.session.add(post)
        db.session.commit()
        return PostSerializer(post).data, 201


class PostView(restful.Resource):
    def get(self, id):
        posts = Post.query.filter_by(id=id).first()
        return PostSerializer(posts).data

class CommentListView(restful.Resource):
    def get(self,postid):
        postComments = Comment.query.filter_by(post_id=postid).all()#request.args.get('postid')
        print postComments
        return CommentSerializer(postComments, many=True).data

    @auth.login_required
    def post(self,postid):
        form = CommentCreateForm()
        if not form.validate_on_submit():
            return form.errors,422
        #comment = Comment(content = form.content.data, user_id = form.user_id.data, post_id = form.post_id.data)
        comment = Comment(form.content.data, postid)
        db.session.add(comment)
        db.session.commit()
        return CommentSerializer(comment).data, 201


class LikeListView(restful.Resource):
    # get likes of a post
    def get(self, postid):
        postLikes = Like.query.filter_by(post_id=postid).all()
        print postLikes
        return LikeSerializer(postLikes, many=True).data

    # get likes of a comment
    def get(self, commentid):
        commenttLikes = Like.query.filter_by(comment_id=commentid).all()
        print commentLikes
        return LikeSerializer(commentLikes, many=True).data



api.add_resource(UserView, '/api/v1/users')
api.add_resource(SessionView, '/api/v1/sessions')
api.add_resource(PostListView, '/api/v1/posts')
api.add_resource(PostView, '/api/v1/posts/<int:id>')
api.add_resource(CommentListView, '/api/v1/posts/<int:postid>/comments')
