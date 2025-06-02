from sqladmin import ModelView
from .models import users, posts, comments


class UserAdmin(ModelView, model=users):
    column_list = [
        users.id,
        users.name,
        users.email,
        users.phone,
        users.email_verified,
        users.created_at,
    ]
    column_labels = {
        users.email_verified: "Email Verified",
        users.phone: "Phone Number",
    }
    column_searchable_list = [users.name, users.email, users.phone]
    column_filters = [users.email_verified, users.created_at]
    form_columns = [
        users.name,
        users.email,
        users.phone,
        users.address,
        users.email_verified,
        users.phone_verified,
    ]
    name = "User"
    name_plural = "Users"


class PostAdmin(ModelView, model=posts):
    column_list = [
        posts.id,
        posts.title,
        posts.content,
        posts.published,
        posts.owner_id,
        posts.created_at,
    ]
    column_searchable_list = [posts.title, posts.content]
    name = "Post"
    name_plural = "Posts"


class CommentAdmin(ModelView, model=comments):
    column_list = [
        comments.comment_id,
        comments.comment,
        comments.post_id,
        comments.user_id,
        comments.commentree,
        comments.created_at,
    ]
    name = "Comment"
    name_plural = "Comments"
