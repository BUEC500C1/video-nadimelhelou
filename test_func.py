from PIL import Image, ImageFont, ImageDraw
import os
from video import *

# Test the delete_images() function
def test_delete_images():
	img = Image.new('RGB', (600, 400), color=(65,5,184))
	img.save("image1.png")
	delete_images("image")

	flag = True
	for image in os.listdir('.'):
		if image.startswith("image") & image.endswith('.png'):
			flag = False

	assert flag == True


# Test the delete_video() function
def test_delete_video():
	delete_video("nadimelhelou")

	flag = True
	for video in os.listdir('.'):
		if video.startswith("daily_tweets_nadimelhelou") & video.endswith('.mp4'):
			flag = False

	assert flag == True
