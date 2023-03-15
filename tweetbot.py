import tweepy
import json
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from topost.topost.spiders import top
import urllib.request as get


keydoc=open('keys.json')
keys=json.load(keydoc)
auth=tweepy.OAuthHandler(keys['apikey'],keys['apikey_secret'])
auth.set_access_token(keys['apitoken'],keys['apitoken_secret'])

api=tweepy.API(auth,wait_on_rate_limit=True)

def quality(likes,comments):
    if 'k' in likes:
        likes=float(likes.strip('k'))*1000
    else:
        likes=float(likes)
    if 'k' in comments:
        likes=float(comments.strip('k'))*1000
    else:
        likes=float(comments)
    k1,k2=1,3
    return k1*likes+k2*comments

def post(img,text,url):
    newpost=api.update_status_with_media(filename=img,status=text)
    api.update_status(status=url, in_reply_to_status_id=newpost.id_str, auto_populate_reply_metadata=True)

def getpost():
    spider = top()
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider)
    process.start()
    doc=open('topost/output.json','r')
    posts=json.load(doc)
    max_index=0
    max_value=-1
    j=0
    img=''
    for i in posts:
        v=quality(i['upvotes'],i['comments'])
        if v>max_value:
            max_index=j
        j=j+1
    if posts[max_index]['isvid']:
        img='media/this.mp4'
        get.urlretrieve(posts[max_index]['source'],img)
    else:
        img='media/this.png'
        get.urlretrieve(posts[max_index]['source'],img)

    post(img,posts[max_index]['status'],posts[max_index]['url'])
    


