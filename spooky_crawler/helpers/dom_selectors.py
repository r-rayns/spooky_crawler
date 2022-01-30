# To test new publications the selectors can be tested in the dev console using $x('<selector>')
title_selectors = (
    lambda doc: doc.xpath('//meta[contains(@name, "title")]/@content').get(),
    lambda doc: doc.css('title::text').get(),
    lambda doc: doc.xpath('//meta[contains(@property, "og:title")]/@content').get(),
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
        doc.xpath('//div[@id="content-wrapper"]//p[not(a)]').getall())
)
