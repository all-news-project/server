class BBCXPaths:
    publishing_time_element = "//time[@data-testid='timestamp']"
    article_image = "//article//figure//img"
    articles_elements = "//div[contains(@class, 'gel-layout__item')]/.//a[contains(@href, '/news/') or contains(@href, '/article/')]"
    text_block = "//div[@data-component='text-block']"
    popup_close_button = "//button[@id='close2']"


class TIMEXPaths:
    articles_elements = "//*[@class='topic-section-wrapper']//ul[contains(@class, 'items')]//li[contains(@id,'item')]//a[@href]"
    popup_close_button = "//*[@id='close_icon']"


class NBCXPaths:
    publishing_time_element = "//time[@class='relative z-1']"
    articles_elements = "//a[contains(@href, '/us-news/') or contains(@href, '/politics/') or contains(@href, '/world/')]"
    text_block = "//div[@class='article-body']/.//p[not(@class='byline-bio expanded-byline__bio')]"
    popup_close_button = "//*[@id='close_icon']"
    article_image = "//article//figure//img"
