import scrapy


class MagazinesSpider(scrapy.Spider):
    name = 'magazines'
    allowed_domains = ['scimagojr.com']
    start_urls = ['https://www.scimagojr.com/journalrank.php?country=CO',
                    'https://www.scimagojr.com/journalrank.php?country=MX',
                    'https://www.scimagojr.com/journalrank.php?country=CL',
                    'https://www.scimagojr.com/journalrank.php?country=AR',
                    'https://www.scimagojr.com/journalrank.php?country=PE',
                    'https://www.scimagojr.com/journalrank.php?country=ES',
                    'https://www.scimagojr.com/journalrank.php?country=US']

    def parse(self, response):
        for link in response.css('td.tit a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_link_magazine)
        
        next_page = response.xpath('//div[@class="pagination_buttons"]/a[2]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_link_magazine(self, response):
        magazine = response.css('div.background div.journaldescription')
        yield {
            'Name': magazine.css('h1::text').get().strip(),
            'Country': magazine.xpath('//div[1]/p/a/text()').get(),
            'H-INDEX': magazine.xpath('//div/div[4]/p/text()').get(),
            'Category': magazine.css('ul.treecategory li a::text').getall(),
            'ISSN': magazine.xpath('//div/div[6]/p/text()').get(),
            'Link': magazine.css('[id="question_journal"]::attr(href)').get(),
        }

