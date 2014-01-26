from feedformatter import Feed
from urllib2 import Request, urlopen
import json
import time

'''
Convert a g+ feed to an atom feed, workaround strange server apikey limitations
'''

public_host = "localhost"

base_uri = "https://www.googleapis.com/plus/v1"

author_uri = "%s/people/%s?fields=displayName&key=%s" % (base_uri, user_id, public_key)

feed_uri = "%s/people/%s/activities/public?key=%s" % (base_uri, user_id, public_key)

def get_data(uri):
    req = Request(uri)
    req.add_header("Referer", public_host)
    r = urlopen(req)
    return json.load(r)

author = get_data(author_uri)['displayName']

feed = Feed()

feed.feed['title'] = author + " G+"
feed.feed['link'] = "https://plus.google.com/%s/posts" % (user_id)
feed.feed['author'] = author

for item in get_data(feed_uri)['items']:
    feed_item = {}
    feed_item['title']   = item['title']
    feed_item['url']     = item['url']
    feed_item['pubDate'] = time.strptime(item['published'].split(".")[0],
                                         "%Y-%m-%dT%H:%M:%S")
    feed_item['title']   = ""
    feed_item['content'] = item['object']['content']
    feed.items.append(feed_item)

print feed.format_atom_string()

