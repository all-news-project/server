class BBCXPaths:
    publishing_time_element = "//time[@data-testid='timestamp']"
    article_image = "//article//figure//img"
    articles_elements = "//div[contains(@class, 'gel-layout__item')]/.//a[contains(@href, '/news/') or contains(@href, '/article/')]"
    text_block = "//div[@data-component='text-block']"
    popup_close_button = "//button[@id='close2']"


class TIMEXPaths:
    article_image = "//div[@class='article-content']//img[contains(@src,'api.time.com/wp-content')]"
    publishing_time_element = "//meta[@property='article:published_time']"
    text_article = "//div[@id='article-body']/div/p[not(@class)] | //div[@id='article-body']/div/ul/li"
    articles_elements = "//*[@class='topic-section-wrapper']//ul[contains(@class, 'items')]//li[contains(@id,'item')]//a[@href]"
    popup_close_button = "//*[@id='close_icon']"