import os
#import Image
from PIL import Image
from flask import url_for
from flaskblog import app



def save_picture(form_picture):
	#random_hex = secrets.token_hex(8)
	random_hex = os.urandom(8).hex()
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex+f_ext
	picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
	output_size = (125,125)
	image = Image.open(form_picture)
	image.thumbnail(output_size)

	image.save(picture_path)
	return picture_fn
