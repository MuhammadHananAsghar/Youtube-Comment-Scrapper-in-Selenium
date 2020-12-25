from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import json




class CommentGrabber:
	
	def __init__(self, video_id):
		"""
		Initializing Bot
		"""
		self.driver_path = "/XXXXXXXXXXXXXX/geckodriver"
		self.video = "https://www.youtube.com/watch?v="+video_id
		self.bot = webdriver.Firefox(options=self.__options(), executable_path=self.driver_path)
		self.__start(self.bot, self.video)


	def __start(self, bot, video):
		"""
		Starting Bot
		"""
		bot.get(video)
		sleep(10)
		with open("channel.txt", "w") as file:
			file.write(json.dumps(self.__channel(bot)))
		file.close()
		self.__scroll(bot)
		comment_tags = bot.find_elements_by_tag_name("ytd-comment-thread-renderer")
		comment_id = 0
		with open('comments.txt', 'w') as file:
			for tag in comment_tags:
				try:
					comment_id += 1
					return_result = self.__comment(tag, comment_id)
					print(return_result)
					file.write(json.dumps(return_result))
					file.write("\n")
				except:
					pass
		file.close()


	def __comment(self, main, id):
		header_area = main.find_element_by_id("header-author")
		author_name = header_area.find_element_by_id("author-text").find_element_by_tag_name("span").text
		author_channel_link = header_area.find_element_by_id("author-text").get_attribute("href")
		time_posted = header_area.find_element_by_tag_name("yt-formatted-string").find_element_by_tag_name("a").text
		comment_posted = main.find_element_by_id("content").find_element_by_id("content-text").text
		return {
		"Comment ID":id,
		"Author":author_name,
		"Author Channel":author_channel_link,
		"Comment Time":time_posted,
		"Comment":comment_posted.strip()
		}


	def __channel(self, bot):
		video_details = bot.find_element_by_tag_name("ytd-video-primary-info-renderer")
		video_meta_data = video_details.find_elements_by_tag_name("h1")
		video_title = video_meta_data[0].text
		video_views = video_details.find_element_by_tag_name("yt-view-count-renderer").text
		video_upload_time = video_details.find_element_by_id("date").find_element_by_tag_name("yt-formatted-string").text
		video_likes = video_details.find_elements_by_tag_name("ytd-toggle-button-renderer")[0].find_element_by_tag_name("yt-formatted-string").text
		video_dislikes = video_details.find_elements_by_tag_name("ytd-toggle-button-renderer")[1].find_element_by_tag_name("yt-formatted-string").text
		video_channel_details = bot.find_element_by_tag_name("ytd-video-secondary-info-renderer").find_element_by_tag_name("ytd-video-owner-renderer")
		video_channel = video_channel_details.find_element_by_tag_name("ytd-channel-name").find_element_by_tag_name("yt-formatted-string").text
		video_channel_subscribers = video_channel_details.find_element_by_id("upload-info").text.split("\n")[-1]
		return {
			"Title":video_title.strip(),
			"Views":video_views,
			"Time":video_upload_time,
			"Likes":video_likes,
			"Dislikes":video_dislikes,
			"Channel Name":video_channel,
			"Channel Subscribers": video_channel_subscribers
		}

	def __scroll(self, driver):
		print("Bot is Scrolling")
		while True:
			scroll_height = 2000
			document_height_before = driver.execute_script("return document.documentElement.scrollHeight")
			driver.execute_script(f"window.scrollTo(0, {document_height_before + scroll_height});")
			sleep(2)
			document_height_after = driver.execute_script("return document.documentElement.scrollHeight")
			if document_height_after == document_height_before:
				break

	def __options(self):
		"""
		Configuring options of the Bot
		"""
		options = Options()
		options.add_argument("Cache-Control=no-cache")
		options.add_argument("--no-sandbox")
		options.add_argument("--dns-prefetch-disable")
		options.add_argument("--disable-dev-shm-usage")
		options.add_argument("--disable-web-security")
		options.add_argument("--ignore-certificate-errors")
		options.page_load_strategy = 'none'
		options.add_argument("--ignore-certificate-errors-spki-list")
		options.add_argument("--ignore-ssl-errors")
		return options


cg = CommentGrabber("BqrQoWBAeL4")
