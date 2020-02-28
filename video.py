from PIL import Image, ImageFont, ImageDraw
import textwrap
import os
import requests
from io import BytesIO
from twitter import Twitter


def convert_to_images(tweets, username):
    if len(tweets) == 0:
        return
    else:
        nb = 1
        # Create an image for each tweet
        for tweet in tweets:
            text = tweet.text
            img = Image.new('RGB', (600, 400), color=(255,255,255))
            img_drawn = ImageDraw.Draw(img)
            wrapped = textwrap.wrap(text, width=35)
            font = ImageFont.truetype("arial.ttf", 30)

            # Write tweet's text to image
            i = 0
            for line in wrapped:
                img_drawn.text((60, 40 + i), text=line, fill=(0,0,0), font=font)
                i = i + 30

            # If the tweet has a photo, add it
            if 'media' in tweet.entities:
                response = requests.get(tweet.entities['media'][0]['media_url_https'])
                media = Image.open(BytesIO(response.content))
                media.thumbnail((400, 300-i), Image.ANTIALIAS)
                img.paste(media, (60, i+50))

            # Save image
            name = username + str(nb) + ".png"
            img.save(name)
            nb += 1


def delete_images(username):
    # Delete all older images for a given username
    for image in os.listdir('.'):
        if image.startswith(username) & image.endswith('.png'):
            os.remove(image)


def delete_video(username):
    # Delete all older videos for a given username
    for video in os.listdir('.'):
        if video.startswith('daily_tweets_' + username) & video.endswith('.mp4'):
            os.remove(video)


def delete_all_videos():
	for video in os.listdir('.'):
		if video.startswith('daily_tweets_') & video.endswith('.mp4'):
			os.remove(video)
