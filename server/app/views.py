from flask import g, request
from flask.ext import restful
from flask.ext.restful import reqparse

from flask_restful import abort

from server import api, db, flask_bcrypt, auth
from models import User, Post,Comment, Like
from forms import UserCreateForm, SessionCreateForm, PostCreateForm, CommentCreateForm, CommentUpdateForm, PostUpdateForm
from serializers import UserSerializer, PostSerializer, CommentSerializer, PutSerializer


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

    def delete(self):
        usr = User.query.filter_by(id=user_id).first()
        db.session.delete(usr)
        #return '', 200

class SessionView(restful.Resource):
    def post(self):
        form = SessionCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User.query.filter_by(email=form.email.data).first()
        if user and flask_bcrypt.check_password_hash(user.password, form.password.data):
            return UserSerializer(user).data, 201
        return '', 401

class LogOut(restful.Resource):
    @auth.login_required
    def get(self):
        user = User.query.filter_by(email = g.user.email).first()
        print g.user.email, ' ,,, ',user.id
        if user is None:
            return 'User not found!', 405
        if user.id != g.user.id:
            return 'You cannot logout the user!',405
        logout_user(user)
        return 200


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
        if posts == None:
            abort(404)
        return PostSerializer(posts).data

    @auth.login_required
    def delete(self, id):
        post = Post.query.filter_by(id=id).first()
        if post == None:
            abort(404)
        if  post.user_id != g.user.id:
            abort(403)
        db.session.delete(post)
        db.session.commit()

    @auth.login_required
    def put(self, id):
        form = PostUpdateForm()
        if not form.validate_on_submit():
            return form.errors,422
        post = Post.query.filter_by(id=id).first()#request.args.get('postid')
        if post.user_id != g.user.id:
            abort(403)#,{'message':'You are not the owner of the post! You cannot edit it!'})
        post.body = form.body.data
        post.title = form.title.data
        db.session.commit()
        return PostSerializer(post).data, 200

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

class ManageComment(restful.Resource):
    def get(self,commentid):
        print 'we are here!!!!'
        cmt = Comment.query.filter_by(id=commentid).first()#request.args.get('postid')
        print cmt
        return CommentSerializer(cmt, many=False).data

    @auth.login_required
    def put(self,commentid):
        #if current_user != put.author:
         #  abort(403)
        form = CommentUpdateForm()
        if not form.validate_on_submit():
            return form.errors,422
        cmt = Comment.query.filter_by(id=commentid).first()#request.args.get('postid')
        if cmt.user_id != g.user.id:
            abort(403)
        cmt.content = form.content.data
        db.session.commit()
        return CommentSerializer(cmt).data, 200

    @auth.login_required
    def delete(self, commentid):
        cmt = Comment.query.filter_by(id=commentid).first()
        if  cmt.user_id != g.user.id:
            abort(403)
        db.session.delete(cmt)
        db.session.commit()

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
api.add_resource(ManageComment, '/api/v1/comments/<int:commentid>')
api.add_resource(LogOut, '/api/v1/logout')
