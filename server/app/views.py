__author__ = 'fsiavash'

from flask import g, request
from flask.ext import restful, login
from flask.ext.restful import reqparse

from flask_restful import abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.server import api, db, flask_bcrypt, auth
from app.models import User, Post,Comment
from app.forms import UserCreateForm, SessionCreateForm, PostCreateForm, CommentCreateForm, CommentUpdateForm, PostUpdateForm, ProfileUpdateForm
from app.serializers import UserSerializer, PostSerializer, CommentSerializer, PutSerializer


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
    def get(self, id): # manage article 
        posts = Post.query.filter_by(id=id).first()
        if posts == None:
            abort(404)
        return PostSerializer(posts).data

    @auth.login_required
    def delete(self, id): # delete article
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
        #print postComments
        return CommentSerializer(postComments, many=True).data

    @auth.login_required
    def post(self,postid): # add comment

        form = CommentCreateForm()
        if not form.validate_on_submit():
            return form.errors,422
        #comment = Comment(content = form.content.data, user_id = form.user_id.data, post_id = form.post_id.data)
        comment = Comment(form.content.data, postid)
        db.session.add(comment)
        db.session.commit()
        return CommentSerializer(comment).data, 201

class ManageComment2(restful.Resource):
    #@auth.login_required
    def get(self,commentid):  # get one comment
        #print 'we are here!!!!'
        cmt = Comment.query.filter_by(id=commentid).first()
                        #request.args.get('postid')
        #print cmt
        return CommentSerializer(cmt, many=False).data

    @auth.login_required
    def put(self,commentid): # edit one comment
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


class ManageComment(restful.Resource):
    @auth.login_required
    def get(self,userid):  # get all comments by a user (athorised)
        #print 'we are here!!!!'
        cmt = Comment.query.filter_by(user_id=userid).all()
                        #request.args.get('postid')
        #print cmt
        return CommentSerializer(cmt, many=True).data





class UserProfile(restful.Resource):
    # get likes of a post
    @auth.login_required
    def get(self, userid):

        user = User.query.filter_by(id = userid).first()
        if user== None:
            abort(403)
        print(user)
        if user.id != g.user.id:
            print("user ", user.id, " current user ", g.user.id)
            print("You are not athorised to have access to user profile.")
            abort(403)
        return UserSerializer(user).data, 200

    @auth.login_required
    def put(self, userid):
        form = ProfileUpdateForm()
        if not form.validate_on_submit():
            return form.errors,422
        prof = User.query.filter_by(id=userid).first()#request.args.get('postid')
        if prof.id != g.user.id:
            abort(403)

        prof.email = form.email.data
          #  set_password(self, form.password.data)
        db.session.commit()

        return UserSerializer(prof).data, 200






api.add_resource(UserView, '/api/v1/users')
api.add_resource(SessionView, '/api/v1/sessions')
api.add_resource(PostListView, '/api/v1/posts')
api.add_resource(PostView, '/api/v1/posts/<int:id>')
api.add_resource(CommentListView, '/api/v1/posts/<int:postid>/comments')
api.add_resource(ManageComment, '/api/v1/usercomments/<int:userid>')
api.add_resource(ManageComment2, '/api/v1/comments/<int:commentid>')
api.add_resource(LogOut, '/api/v1/logout')
api.add_resource(UserProfile, '/api/v1/profile/<int:userid>')