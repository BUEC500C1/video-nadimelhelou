# Nadim El Helou - EC 500 C1 - HW4 Twitter Video API

# References: 
# https://developer.twitter.com/en/docs/api-reference-index
# https://code-maven.com/create-images-with-python-pil-pillow
# https://trac.ffmpeg.org/wiki/Slideshow
# https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
# https://stackoverflow.com/questions/15312953/choose-a-file-starting-with-a-given-string

import flask
from flask import request, jsonify, send_file
import requests
from video import *
from twitter import Twitter
import queue
import threading


app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Queue of all processes
q = queue.Queue(maxsize=20)

# Where video are stored when done
finished_videos = []

# Track all API calls
history = []


@app.route('/', methods=['GET'])
def home():
    return "<h1>Twitter Video API</h1><p>This API returns a video with a given user's tweets. By Nadim El Helou</p>"


@app.route('/tracking', methods=['GET'])
def track():
	out = "All API calls: "
	for call in history:
		out += call[0] + " (" + call[1] + "). "
	return out


@app.route('/tweets', methods=['GET'])
def api_id():
    # Check if a username was given
    if 'username' in request.args:
        username = request.args['username']
    else:
        return "<h1>Error: No username provided. Please enter a twitter username.</h1>"
    
    # Connect to twitter and get tweets
    twit = Twitter("keys")
    tweets = twit.get_tweets(username)
    if tweets == -1:
    	return "<h1>Error: Given twitter username does not exist. Please enter another one.</h1>"
    elif tweets == []:
    	return "<h1>No tweets found for this username in the past day. Please enter another one.</h1>"
    else:
    	q.put(username)
    	delete_video(username)
    	curr_video = "daily_tweets_" + username + ".mp4"
    	history.append([username, "in progress"])
    	
    	print("\nStarted " + username + "'s video")
    	
    	while curr_video not in finished_videos:
    		temp = 1

    	ind = history.index([username, "in progress"])
    	history[ind][1] = "completed"
    	
    	finished_videos.remove(curr_video)
    	
    	return send_file(curr_video)


def create_video():
	# Get most recent username from queue
	username = q.get()
	twit = Twitter("keys")
	tweets = twit.get_tweets(username)

	# Delete any older images/videos
	delete_video(username)
	delete_images(username)
	
	# Create images and video
	convert_to_images(tweets, username)
	os.system("ffmpeg -framerate 1/5 -i " + username + "%d.png -c:v libx264 -r 30 -pix_fmt yuv420p daily_tweets_" + username + ".mp4")
	finished_videos.append("daily_tweets_" + username + ".mp4")

	# Delete the images (we don't need them anymore)
	delete_images(username)

	return 1


if __name__ == '__main__':

	delete_all_videos()
	max_threads = 4
	q.join()
	threads = []

	# Create threads
	for i in range(max_threads):
		t = threading.Thread(target=create_video)
		t.setDaemon(True)
		threads.append(t)

	# Start threads
	for t in threads:
		t.start()

	app.run()
