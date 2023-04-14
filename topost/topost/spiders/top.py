import scrapy
#subreddit=['funny','memes','wholesomememes']
class topost(scrapy.Spider):
    name='top'
    allowed_domains = ['reddit.com']
    start_urls = ['https://www.reddit.com/r/memes/top/', 'https://www.reddit.com/r/funny/top/', 'https://www.reddit.com/r/wholesomememes/top/']
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json',
        'FEED_EXPORT_OVERWRITE': True,
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
        
    def parse(self,response):
        vid=False
        try:
            sauce=response.css('img._2_tDEnGMLxpM6uOa2kaDB3.ImageBox-image.media-element._1XWObl-3b9tPy64oaG6fax').attrib['src']
        except:
            sauce=response.css('source').attrib['src']
            vid=True
        yield {
            'url':response.css('a.SQnoC3ObvgnGjWt90zD9Z._2INHSNB8V5eaWp4P0rY_mE').attrib['href'],
            'status':response.css('h3._eYtD2XCVieq6emjKBH3m::text').get(),
            'source':sauce,
            'upvotes':response.css('div._1rZYMD_4xY3gRcSS3p8ODO._3a2ZHWaih05DgAOtvu6cIo::text').get(),
            'comments':response.css('span.FHCV02u6Cp2zYL0fhQPsO::text').get().strip(' comments'),
            'isvid':vid,
        }
        
#scrapy crawl top -O output.json 