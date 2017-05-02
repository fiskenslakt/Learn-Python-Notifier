import time

import praw

import RPi.GPIO as gpio
gpio.setwarnings(False)

channel = 7
gpio.setmode(gpio.BOARD)
gpio.setup(channel, gpio.OUT)

def toggle(channel=channel):
    gpio.output(channel, not gpio.input(channel))

def blink(n=8, delay=0.05):
    for i in range(n*2):
        toggle()
        time.sleep(delay)

blink()

while True:
    try:
        reddit = praw.Reddit(client_id='',
                             client_secret='',
                             user_agent='')
        failedResponses = 0
        oldPosts = [submission for submission in reddit.subreddit('learnpython').new(limit=10)]
        topPost = oldPosts[0]
        postCount = 0

        while True:
            if topPost.id not in map(lambda post: post.id, oldPosts):
                postCount += 1
                print '[{}] {}. {}'.format(topPost.id, postCount, topPost.title)
                blink()
                oldPosts = [submission for submission in reddit.subreddit('learnpython').new(limit=10)]
                time.sleep(10)
            else:
                time.sleep(10)
                topPost = next(reddit.subreddit('learnpython').new(limit=1))
    except KeyboardInterrupt:
        print '\nStopping...\n'
        raise SystemExit
    except:
        failedResponses += 1
        print 'Unexpected error.\nReddit is probably down or something, sleeping...\n'
        if failedResponses <= 3:
            time.sleep(120)
        elif failedResponses == 4:
            time.sleep(600)
        else:
            time.sleep(3600)
