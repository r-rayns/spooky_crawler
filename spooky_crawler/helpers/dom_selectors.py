
title_selectors = (
    lambda doc: doc.xpath('//meta[contains(@name, "title")]/@content').get(),
    lambda doc: doc.css('title::text').get(),
)

description_selectors = (
    lambda doc: doc.xpath(
        '//meta[contains(@name, "description")]/@content').get(),
)

publisher_selectors = (
    lambda doc: doc.xpath(
        '//meta[@property="og:site_name"]/@content').get(),
)

date_selectors = (
    lambda doc: doc.xpath(
        '//meta[@property="article:published_time"]/@content').get(),
)

article_body_selectors = (
    lambda doc: ' '.join(
        doc.xpath('//div[@class="article-body"]//p').getall()),
    lambda doc: ' '.join(
        doc.xpath('//div[@id="content-wrapper"]//p').getall())
)