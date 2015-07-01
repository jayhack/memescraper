"""
Module: imgur
=============

Defines scraper for imgur.com
"""
import os
import pickle
import requests
from imgurpython import ImgurClient
from collections import namedtuple

Meme = namedtuple('Meme', ['id', 'views', 'score', 'content'])

class ImgurScraper(object):

	#==========[ Parameters ]==========
	client_id = '8e6c102fd0cb416'
	client_secret = 'a2ab9f76a1b6706b00200fa74270a281c32248bb'
	data_dir = './data'

	def __init__(self):
		self.client = ImgurClient(self.client_id, self.client_secret)
		self.num_scraped  = 0


	################################################################################
	####################[ DATA STORAGE ]############################################
	################################################################################

	def get_dump_filepath(self, memes):
		"""returns filename for scraped memes"""
		filename = '%s-%s.pkl' % (self.num_scraped - len(memes), self.num_scraped)
		filepath = os.path.join(self.data_dir, filename)
		return filepath

	def dump_memes(self, memes, verbose=True):
		"""saves array of memes to disk"""
		path = self.get_scraped_filepath(memes)
		print '-----> Saving %d memes to %s...' % (len(memes), path)
		pickle.dump(memes, open(path, 'w'))
		print '\tSuccess.'

	################################################################################
	####################[ GRABBING MEMES ]##########################################
	################################################################################

	def get_gallery_page(self, page, verbose=True):
		"""returns list of GalleryImages"""
		return client.memes_subgallery(sort='top', page=page)

	def make_meme_url(self, meme_id):
		return 'http://imgur.com/t/meme/%s' % meme_id

	def get_meme_page(self, meme_id):
		return request.get(make_meme_url(meme_id))

	def extract_description(self, meme_page):
		description = tree.xpath('//meta[@name="description"]')[0]
		return description.get('content')

	def get_meme_content(self, meme_id):
		page = get_meme_page(meme_id)
		description = tree.xpath()

	def image_to_meme(self, image):
		"""GalleryImage -> Meme"""
		content = self.get_meme_content(image.id)
		return Meme(id=image.id, views=image.views, score=image.score, content=content)
	


class ImgurScraper(object):
	"""
	Class: ImgurScraper
	===================

	Scrapes memes from Imgur
	"""
	client_id = '8e6c102fd0cb416'
	client_secret = 'a2ab9f76a1b6706b00200fa74270a281c32248bb'

	data_dir = './data'
	popular_url = "http://version1.api.memegenerator.net/Instances_Select_ByNew"

	def __init__(self):
		self.client = ImgurClient(self.client_id, self.client_secret)

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
	scraper = ImgurScraper()
	scraper.load_meme_names()
#	scraper.scrape_meme_names()
	print scraper.meme_names
	memes = scraper.scrape_meme(scraper.meme_names[0][1])












