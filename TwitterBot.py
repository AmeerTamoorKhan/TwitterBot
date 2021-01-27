from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd
import numpy as np
import streamlit as st


class TwitterBot:
    def __init__(self, trend, no_tweets, progress=None):

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument(f'user-agent={user_agent}')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument("--proxy-bypass-list=*")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--enable-javascript")
        self.driver = webdriver.Chrome(executable_path="Driver/chromedriver", options=self.options)

        self.progress = progress
        self.trend = trend
        self.no_tweets = no_tweets
        self.i = 100/self.no_tweets
        self.twitter = self.driver.get('https://twitter.com/MaryamNSharif')

        #self.driver.fullscreen_window()
        self.Tweets = []
        self.flag = True
        self.counter = 0
        self.df = pd.DataFrame(columns=['Name', 'Id', 'Tweet', 'Time', 'Retweet Count', 'Likes Count'], index=np.arange(0, self.no_tweets))
        self.unique_tweets = set()
        self.search()
        #self.scrap_tweets()

    def search(self):
        #time.sleep(2)
        #st.text(self.driver.page_source)
        print(100)
        element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]'))
            )
        print(1000)
        search = element.send_keys([self.trend, Keys.RETURN])

    def tweets_collection(self, tweets):
        try:
            user_name = tweets.find_element_by_xpath('.//span').text
            user_id = tweets.find_element_by_xpath('.//span[contains(text(), "@")]').text

            tweet = tweets.find_element_by_xpath('./div[2]/div[2]//div').text

            timestamp = tweets.find_element_by_xpath('.//time').get_attribute('datetime')

            retweets = tweets.find_element_by_xpath('.//div[@data-testid="retweet"]').get_attribute('aria-label').split(' ')[0]
            likes = tweets.find_element_by_xpath('.//div[@data-testid="like"]').get_attribute('aria-label').split(' ')[0]

            # html_source = self.driver.page_source
            # file = open('temp.html', 'w')
            # file.write(html_source)
            # st.text(html_source)

            TWEET = (user_name, user_id, tweet, timestamp, retweets, likes)

        except (NoSuchElementException, StaleElementReferenceException):
            print("Exception")
            return

        return TWEET

    def dataFrameWork(self, tweet, i):
        print(i)
        self.df.iloc[i, 0] = tweet[0]
        self.df.iloc[i, 1] = tweet[1]
        self.df.iloc[i, 2] = tweet[2]
        self.df.iloc[i, 3] = tweet[3]
        self.df.iloc[i, 4] = tweet[4]
        self.df.iloc[i, 5] = tweet[5]

    def scrap_tweets(self):
        count = 0
        #time.sleep(2)
        while self.flag:
            cards = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.XPATH, '//div[@data-testid="tweet"]'))
            )
            #cards = self.driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
            if cards:
                for card in cards:
                    if self.counter != self.no_tweets:

                        tweet = self.tweets_collection(card)

                        if tweet:
                            tweet_id = "".join(tweet)
                            if tweet_id not in self.unique_tweets:
                                self.unique_tweets.add(tweet_id)
                                self.dataFrameWork(tweet, self.counter)
                                # progress['value'] += self.i
                                # progress.update()
                                count = count + 1/self.no_tweets
                                if count >= 1:
                                    count = 1.0
                                if self.progress:
                                    self.progress.progress(count)
                                self.counter += 1
                    else:
                        self.flag = False
                        break

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                #time.sleep(1)
            else:
                self.flag = False
            del cards

        return self.df

    def save_tweets(self, file_name):
        self.df.to_csv(file_name, index=False)

    def close(self):
        self.driver.close()


if __name__ == "__main__":
    bot = TwitterBot('tesla', 10)
    print(bot.scrap_tweets())

