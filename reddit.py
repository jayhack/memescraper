"""
Module: reddit
==============

Defines scraper for imgurtranscriber
"""
import os
import pickle
import praw

class RedditScraper(object):
	"""
	Class: RedditScraper
	====================

	Scrapes memes from Reddit, using user imgurtranscriber
	"""
	data_dir = './data'
	user_agent = 'in_the_fresh'
	block_size = 1000
	print_size = 100

	def __init__(self):
		self.client = praw.Reddit(user_agent=self.user_agent)
		self.num_scraped = 0



	################################################################################
	####################[ LOAD/SAVE ]###############################################
	################################################################################

	def load_meme_names(self):
		"""loads self.meme_names"""
		path = os.path.join(self.data_dir, 'meme_names.pkl')
		self.meme_names = pickle.load(open(path, 'r'))

	def save_meme_names(self):
		"""saves self.meme_names"""
		path = os.path.join(self.data_dir, 'meme_names.pkl')
		pickle.dump(self.meme_names, open(path, 'w'))


	################################################################################
	####################[ SCRAPE ]##################################################
	################################################################################

	def parse_meme_name(self, s):
		return s.strip().split('*')[3]

	def parse_title(self, s):
		return s.strip().split('*')[-2]

	def parse_text(self, s):
		return s.strip().split('*')[-2]

	def parse_comment(self, comment):
		"""icomment -> meme_name, title, top, bottom"""
		splits = comment.split('\n')
		meme_name = self.parse_meme_name(splits[2])
		title = self.parse_title(splits[4])
		top = self.parse_text(splits[6])
		bottom = self.parse_text(splits[8])
		return meme_name, title, top, bottom

	def dump_memes(self, memes, verbose=True):
		"""saves array of memes to disk"""
		filename = '%s-%s.pkl' % (self.num_scraped - len(memes), self.num_scraped)
		path = os.path.join(self.data_dir, filename)
		print '-----> Saving %d memes to %s...' % (len(memes), path)
		pickle.dump(memes, open(path, 'w'))
		print '\tSuccess.'


	def scrape_memes(self):
		"""scrapes a meme given it's url name"""
		memes = []
		user = self.client.get_redditor('imgurtranscriber')

		for c in user.get_comments(limit=None):

			#=====[ Step 1: add meme	]=====
			try:
				meme_name, title, top, bottom = self.parse_comment(c.body)
				meme = (meme_name, title, top, bottom)
				memes.append(meme)
				self.num_scraped += 1
			except:
				pass

			#=====[ Step 2: dump if appropriate	]=====
			if (self.num_scraped % self.block_size) == 0:
				self.dump_memes(memes)
				memes = []

			#=====[ Step 3: print if appropriate	]=====
			if self.num_scraped % self.print_size == 0:
				print 'scraped %d' % self.num_scraped


		#=====[ Step 3: dump remaining memes	]=====
		self.dump_memes(memes)






if __name__ == '__main__':
	scraper = RedditScraper()
	memes = scraper.scrape_memes()












