import tweepy
import os
import time
import socket
from dotenv import load_dotenv

load_dotenv()
bear_token = os.getenv("API_KEY_2")

# Create a socket and connect to the server
s = socket.socket()  # Create a socket object
host = "127.0.0.1"  # Get local machine name
port = 5554  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

print("Listening on port: %s" % str(port))

s.listen(5)  # Now wait for client connection.
c, addr = s.accept()  # Establish connection with client.

print("Received request from: " + str(addr))


class MyStream(tweepy.StreamingClient):
    def on_connect(self):
        print("Connected")

    def on_tweet(self, tweet):
        c.send(tweet.text.encode("utf-8"))
        print("Sent tweet: ", tweet.text)
        return

    def reset_rules(self):
        try:
            for x in stream.get_rules().data:
                stream.delete_rules(x.id)
        except Exception as e:
            print(f"Error resetting rules: {e}")


stream = MyStream(bearer_token=bear_token, wait_on_rate_limit=True, daemon=True)
stream.reset_rules()

rules = ["#crypto", "#music"]
for rule in rules:
    r = rule + " lang:en -is:retweet"
    stream.add_rules(tweepy.StreamRule(value=r))

stream.filter(
    expansions=["author_id"],
    tweet_fields=["created_at", "referenced_tweets", "geo", "public_metrics"],
)
