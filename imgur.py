"""
Module: imgur
=============

Defines scraper for imgur.com
"""
import os
import sys
import pickle
import requests
import time
import datetime
from lxml import html
from imgurpython import ImgurClient
from collections import namedtuple

Meme = namedtuple('Meme', ['id', 'views', 'score', 'content'])

class ImgurScraper(object):

	#==========[ Parameters ]==========
	client_id = '8e6c102fd0cb416'
	client_secret = 'a2ab9f76a1b6706b00200fa74270a281c32248bb'
	base_data_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data/imgur/')
	block_size = 500
	print_size = 60

	def __init__(self):

		#=====[ Step 1: get data_dir	]=====
		self.data_dir = os.path.join(self.base_data_dir, str(datetime.datetime.now().date()))
		if not os.path.exists(self.data_dir):
			os.mkdir(self.data_dir)

		#=====[ Step 2: get client	]=====
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
		path = self.get_dump_filepath(memes)
		print '-----> Saving %d memes to %s...' % (len(memes), path)
		pickle.dump(memes, open(path, 'w'))
		print '\tSuccess.'

	################################################################################
	####################[ GRABBING MEMES ]##########################################
	################################################################################

	def make_image_url(self, image_id):
		return 'http://imgur.com/t/meme/%s' % image_id

	def get_image_page(self, image_id):
		return requests.get(self.make_image_url(image_id))

	def extract_description(self, image_id):
		page = self.get_image_page(image_id)
		tree = html.fromstring(page.text)
		description = tree.xpath('//meta[@name="description"]')[0]
		return description.get('content')

	def image_to_meme(self, image):
		"""GalleryImage -> Meme"""
		content = self.extract_description(image.id)
		return Meme(id=image.id, views=image.views, score=image.score, content=content)

	def get_gallery_page(self, page, verbose=True):
		"""returns list of GalleryImages"""
		return self.client.memes_subgallery(sort='top', page=page)

	def scrape_memes(self, page_ix=0):
		memes = []
		self.num_scraped = 60*page_ix
		while (True):
			
			#=====[ Step 1: get images	]=====
			try:
				images = self.get_gallery_page(page_ix)
			except:
				print '>>gallery failed; continuing<<'
				continue

			#=====[ Step 2: get memes	]=====
			for image in images:
				try:
					memes.append(self.image_to_meme(image))
					self.num_scraped += 1
					print '.',
				except:
					e = sys.exc_info()[0]
					print 'x',
				time.sleep(0.3)

				#=====[ Step 3: print if appropriate	]=====
				if self.num_scraped % self.print_size == 0:
					print '\nscraped %d' % self.num_scraped

				#=====[ Step 4: dump if appropriate	]=====
				if (self.num_scraped % self.block_size) == 0:
					self.dump_memes(memes)
					memes = []


			page_ix += 1

			if self.num_scraped >= 2000:
				print '\n>>>FINISHED<<<'
				break



if __name__ == '__main__':
	scraper = ImgurScraper()
	print scraper.data_dir
	scraper.scrape_memes()













