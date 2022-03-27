import scrapy,re
import simplejson as json

class TargetUsSpider(scrapy.Spider):
    name = 'target_us'
    allowed_domains = ['www.target.com']
    
    def __init__(self, url=None, *args, **kwargs):
        super(TargetUsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
    
    def parse(self, response):
        page_data={}
        json_data=json.loads(response.xpath('//script[@id="json"]//text()').extract_first()).get('@graph',[{}])[0]
        
        ##ingredients data is avaible under <script>
        TGT_data=re.search('window.__TGT_DATA__ = JSON.parse\("(.*?)"\);', response.text)
        page_data['title']=response.xpath("//h1[@class='Heading__StyledHeading-sc-1mp23s9-0 kmgmYA h-text-bold h-margin-b-tight']/span/text()").get()
        
        page_data['url']=response.request.url
        
        if TGT_data:
            TGT_data=json.loads(TGT_data.group(1).replace('\\"','"').replace('\\\\','\\'))
            page_data['ingredients']=TGT_data.get('__PRELOADED_QUERIES__').get('queries')[1][1].get('product').get('item').get('enrichment').get('nutrition_facts').get('ingredients').split(",")
        else:
            page_data['ingredients']=None
        
        page_data['currency']=json_data.get('offers',{}).get('priceCurrency')
        page_data['upc']=json_data.get('gtin13',{})
        page_data['tcin']=json_data.get('sku',{})
        page_data['price']=json_data.get('offers',{}).get('price')
        page_data['description']=json_data.get('description',{})
        page_data['stock']=json_data.get('offers',{}).get('availability')
        page_data['currency']=json_data.get('offers',{}).get('priceCurrency')
        
        
        print (page_data)
        yield page_data
        pass
