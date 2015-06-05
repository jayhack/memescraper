"""
Module: scraper
===============

defines the scraper
"""
import os
import pickle
import requests

class MemeScraper(object):
	"""
	Class: MemeScraper
	===========================

	Scrapes memes from MemeGenerator
	"""
	data_dir = './data'
	popular_url = "http://version1.api.memegenerator.net/Instances_Select_ByNew"

	def __init__(self):
		pass

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

	def scrape_meme_names(self, load=False):
		"""sets self.meme_names"""
		#=====[ Step 1: set request params	]=====
		params = {
					'languageCode':'en',
					'pageSize':24,
					'urlName':None, #selects the names
					'days':None
				}

		#=====[ Step 2: get meme names	]=====
		page_ix = 0
		display_names = []
		url_names = []
		while True:

			print '=====[ %d ]=====' % page_ix
			params['pageIndex'] = page_ix

			try:
				r = requests.get(self.popular_url, params=params)
				result = r.json()['result']
				display_names += [r['displayName'] for r in result]
				url_names += [r['urlName'] for r in result]
				print [r['urlName'] for r in result]
				if len(result) < 24:
					break
				page_ix += 1
			except:
				break

		#=====[ Step 3: postprocess, return	]=====
		zipped = zip(display_names, url_names)
		zipped = list(set(zipped))
		self.meme_names = zipped
		self.save_meme_names()


	def scrape_meme(self, url_name):
		"""scrapes a meme given it's url name"""
		#=====[ Step 1: set request params	]=====
		params = {
					'languageCode':'en',
					'pageSize':24,
					'urlName':url_name,
					'days':None
				}

		#=====[ Step 2: request until you can't	]=====
		page_ix = 0
		memes = []
		while True:
			print '======[ %d ]=====' % page_ix

			try:
				params['pageIndex'] = page_ix
				r = requests.get(self.popular_url, params=params)
				result = r.json()['result']
				new_memes = [(r['text0'], r['text1'], r['totalVotesScore']) for r in result]
				memes += new_memes
				print new_memes
				memes += [(r['text0'], r['text1'], r['totalVotesScore']) for r in result]
				page_ix += 1

				if len(new_memes) == 0:
					break
			except:
				break

		return memes






if __name__ == '__main__':
	scraper = MemeGeneratorScraper()
	scraper.load_meme_names()
	memes = scraper.scrape_meme(scraper.meme_names[0][1])












