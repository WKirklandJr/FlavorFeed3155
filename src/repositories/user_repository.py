from src.models import db, User

class UserRepository:

    def get_all_users():
        all_users = User.query.all()
        return all_users

    def get_user_by_id(self, user_id):
        get_user = User.query.get(user_id)
        return get_user

    def update_user(self, user_id, username , skill, social, about, profile_picture):
        update_user = User.query.get(user_id)
        update_user.username = username
        update_user.skill = skill
        update_user.social = social
        update_user.about = about
        update_user.profile_picture = profile_picture
        db.session.commit()
        return update_user


user_repository_singleton = UserRepository()
