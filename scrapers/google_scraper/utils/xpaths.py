class TrendXPaths:
    trends_link = "//div[contains(@id, 'content')]//span[not(contains(@class, 'guide'))]//a"


class IconsScraperXPaths:
    media_icon_1 = "//article//div//div[not(@jsaction)]//img[contains(@src,'encrypted')]"
    media_icon_2 = "//article//div[not(@jsaction)]//img[contains(@src,'encrypted')]"
    media_icon = f"{media_icon_1} | {media_icon_2}"
    media_text_1 = "./following-sibling::div/div"
    media_text_2 = "./following-sibling::div/a"
    media_text = f"{media_text_1 } | {media_text_2}"
    search = "//input[@aria-label='Search for topics, locations & sources']"
