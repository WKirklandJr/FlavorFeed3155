from flask import Blueprint, session, render_template, request, redirect, abort
from src.models import db
from src.repositories.user_repository import user_repository_singleton
from werkzeug.utils import secure_filename
import os

profile_router = Blueprint('profiles', __name__, url_prefix='/profile')

# GET edit profile
@profile_router.get('/<int:user_id>/edit')
def get_edit_profile(user_id):
    
    if 'user' not in session:
        return redirect('/login')
    

    username = session.get('user')['username']
    session_user = user_repository_singleton.get_user_by_username(username)
    user_id = session_user.user_id

    if user_id != session_user.user_id:
        print('Incorrect session user. Access denied.')
        abort(400) 
    else:   
        single_user = user_repository_singleton.get_user_by_id(user_id)
        return render_template('edit_profile.html', user=single_user)

#POST profile
@profile_router.post('/<int:user_id>/edit')
def update_user(user_id):

    username = request.form.get('username')
    skill = request.form.get('skill')
    social = request.form.get('social')
    about  = request.form.get('about')

    #image file data
    print(request.files)
    if 'profile_picture' not in request.files:
        print('No profile image file was uploaded')
        abort(400)
    
    profile_picture = request.files['profile_picture']

    if profile_picture.filename == '' or profile_picture.filename.rsplit('.', 1)[1] not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
        print('Invalid file format for profile image')
        abort(400)

    img_filename = secure_filename(profile_picture.filename)
    profile_picture.save(os.path.join('static', 'profile-images', img_filename))

    user_repository_singleton.update_user(user_id, username, skill, social, about, img_filename)
    
    return redirect(f'/users/{user_id}')
