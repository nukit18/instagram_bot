import asyncio
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random

from loader import bot

browser = None


async def login_chrome(login, password):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # прячет браузер от глаз
    global browser
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(5)
    browser.get('https://www.instagram.com')
    await asyncio.sleep(random.randrange(1, 2))

    _login = browser.find_element(By.NAME, "username")
    _login.clear()
    _login.send_keys(login)

    await asyncio.sleep(random.randrange(1, 2))

    _password = browser.find_element(By.NAME, "password")
    _password.clear()
    _password.send_keys(password)

    await asyncio.sleep(random.randrange(1, 2))

    _password.send_keys(Keys.ENTER)


async def close_browser():
    global browser
    browser.close()
    browser.quit()


async def search_by_hashtag(hashtag, time_start):
    global browser
    browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
    urls = []
    length = 350
    counter = 0
    count_urls_last = 0
    counter_new = 0
    while len(urls) <= length:
        count_urls_last = len(urls)
        if counter >= 5 and len(urls) == 0:
            break
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(random.randrange(3, 7))
        hrefs = browser.find_elements_by_tag_name('a')
        for item in hrefs:
            href = item.get_attribute('href')
            if len(urls) > length:
                break
            if "/p/" in href:
                if not href in urls:
                    urls.append(href)
        if len(urls) == count_urls_last:
            if counter_new >= 7:
                break
            counter_new += 1
        else:
            counter_new = 0
        counter += 1

    count_completed = 0
    for url in urls:
        if await check_time(time_start):
            break
        try:
            browser.get(url)
            like = browser.find_element(By.XPATH,
                                        "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button")
            aria_label_like = like.find_element_by_css_selector('svg').get_attribute("aria-label")
            if aria_label_like == "Нравится":
                await asyncio.sleep(random.randrange(6, 10))
                like.click()


            save = browser.find_element(By.XPATH,
                                        "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[4]/div/div/button")
            aria_label_save = save.find_element_by_css_selector('svg').get_attribute("aria-label")
            if aria_label_save == "Сохранить":
                await asyncio.sleep(random.randrange(2, 6))
                save.click()
            await asyncio.sleep(random.randrange(3, 6))
        except:
            try:
                browser.find_element()
            except:
                break
            continue
        count_completed += 1
    return count_completed


async def like_save_function(login, password, hashtag, user_id):
    await login_chrome(login, password)
    await asyncio.sleep(5)
    count_completed = await search_by_hashtag(hashtag, datetime.now())
    await asyncio.sleep(random.randrange(45, 67))
    await close_browser()
    await bot.send_message(user_id,
                           f"Готово! Количество пройденных постов: {count_completed}\nФункция: *Лайк, сохранение*",
                           parse_mode="Markdown")


async def check_time(start_time):
    return (datetime.now() - start_time).seconds / 60 >= 70  # минуты, поменять на 65


async def close_browser_like_save():
    await close_browser()

if __name__ == '__main__':
    asyncio.run(like_save_function("login", "password", "hashtag", 0))  # тестовая функция
