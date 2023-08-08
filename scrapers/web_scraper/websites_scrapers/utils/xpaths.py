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


class NBCXPaths:
    publishing_time_element = "//time[@class='relative z-1']"
    articles_elements = "//a[contains(@href, '/us-news/') or contains(@href, '/politics/') or contains(@href, '/world/')]"
    text_block_1 = "//div[@class='article-body']/.//p[not(@class='byline-bio expanded-byline__bio')]"
    text_block_2 = "//div[@class='article-body__content']/p"
    text_block_3 = "//div[@class='article-body__content']/h2"
    text_block = f"{text_block_1} | {text_block_2} | {text_block_3}"
    popup_close_button = "//*[@id='close_icon']"
    article_image = "//article//figure//img"



class CNNXPaths:
    publishing_time_element = "//div[@class='timestamp']"
    article_image = "//div[@class='image__picture']//img"
    articles_elements = "//a[contains(@data-link-type, 'article')]"
    text_block = "//main[@class='article__main']//p[@data-component-name='paragraph']"
    popup_close_button="//*[@class='bx-close bx-close-link bx-close-inside']"

