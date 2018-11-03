#!/usr/bin/python2

import requests
from bs4 import BeautifulSoup
import optparse
import sys
import os

class SearchBook :

	ROOT_URL = 'http://gen.lib.rus.ec/'
	available_books = []
	download_links = []

	def __init__(self, name) :

		self.sb(name)

	def sb(self, name) :

		if len(name) < 3 :
			print 'Book Name must contain minimum three characters'
			os._exit(0)

		name = name.replace(' ','+')
		url = self.ROOT_URL + 'search.php?req=' + str(name) + '&lg_topic=libgen&open=0&view=simple&res=25&phrase=0&column=def'
		try :
			r = requests.get(url)
		except :
			print 'gen.lib.rus.ec is unavailable at the moment.'
		soup = BeautifulSoup(r.text, "lxml")
		book_lists = soup.find_all("table")[2]
		# there are total 4 tables inside the page, and the third table is storing the list of book

		headings = []
		for h in book_lists.tr.find_all("td") :
			headings.append(h.text.encode('utf-8'))
		#print headings

		no_of_available_books = len(book_lists.find_all("tr"))
		print "\n" + str(no_of_available_books - 1) + " Books listed."

		for i in range(1,no_of_available_books) :
			self.available_books.append(book_lists.find_all("tr")[i])
		# available_books contains list of available books with <tr>
		#print self.available_books[0]

		for i in self.available_books :
			count = 0
			cur_inf = {}
			cur_inf['book_id'] = i.find_all('td')[0].text.encode('utf-8')
			for j in i.find_all('a') :
				count += 1
				if count in range(3,8) :
					cur_inf[str(count-2)] = j['href']
			self.download_links.append(cur_inf)
			#print cur_inf
		
		#print self.download_links

		available_books_details = []
		for b in self.available_books :
			book = []
			for s in b.find_all("td") :
				book.append(s.text.encode('utf-8'))
			available_books_details.append(book)
		#print available_books_details

		# Display of each book
		for item in available_books_details :
			print ""
			for r in range(9) :
				print headings[r] + " => " + item[r]

class DownloadBook :

	def __init__(self, binfo, mirror) :

		self.download(binfo, mirror)

	def download(self, binfo, mirror) :

		if mirror == 1 :

			d_url1 = binfo[str(mirror)]
			try :
				r1 = requests.get(d_url1)
			except :
				print 'Mirror 1 Down, Try different mirror'
			s1 = BeautifulSoup(r1.text, 'lxml')
			d1_url = s1.find_all('a')[0]['href']

			r11 = requests.get(d1_url, stream=True)
			with open(binfo['bookname'],'wb') as f :
				print 'Download in progress .....'
				f.write(r11.content)
			print 'Download Completed.'

		elif mirror == 2 :

			d_url2 = binfo[str(mirror)]
			try :
				r2 = requests.get(d_url2)
			except :
				print 'Mirror 2 down, Try different mirror.'
			s2 = BeautifulSoup(r2.text,'lxml')
			d2_url = s2.find_all('a')[1]['href']

			r22 = requests.get(d2_url, stream=True)
			with open(binfo['bookname'], 'wb') as f :
				print 'Download in progress .....'
				f.write(r22.content)
			print 'Download Completed.'

		elif mirror == 3 :

			DOWNLOAD_URL = 'https://libgen.pw'

			d_url3 = binfo[str(mirror)]
			try :
				r3 = requests.get(d_url3)
			except :
				print 'Mirror 3 down, Try different mirror.'
			s3 = BeautifulSoup(r3.text, 'lxml')
			d33 = DOWNLOAD_URL + s3.find_all('a')[-1]['href']

			r33 = requests.get(d33)
			s33 = BeautifulSoup(r33.text, 'lxml')
			d3_url = DOWNLOAD_URL + s33.find_all('a')[1]['href']

			r333 = requests.get(d3_url, stream=True)
			with open(binfo['bookname'], 'wb') as f :
				print 'Download in progress .....'
				f.write(r333.content)
			print 'Download Completed.'

		else :
			print 'Mirror in between 1-3.'
			os._exit(0)

def main() :

	parser = optparse.OptionParser()
	parser.add_option('-s', help="Search for ebook by name", dest="bname")
	#parser.add_option('-d', help="Download book by id", dest="bdwl")

	(options, args) = parser.parse_args()

	if len(sys.argv) == 1 :
		print str(parser.print_help())[:-4]
		os._exit(0)

	if sys.argv[1] == '-h' or sys.argv[1] == '--help' :
		print str(parser.print_help())
		os._exit(0)

	if sys.argv[1] == '-s' : 
		bookName = options.bname
		sb_obj = SearchBook(bookName)
		#print sb_obj.download_links
		#print sb_obj.available_books[0].find_all('td')[2].text
		#print sb_obj.available_books[0].find_all('td')[1].text
		#print sb_obj.available_books[0].find_all('td')[0].text

	d_bookId = raw_input('\nEnter Book Id to download : ')

	try :
		d_bookId = int(d_bookId)
	except :
		print 'BookId must be integer'
		os._exit(0)

	cur_d_info = {}

	for j in sb_obj.download_links :
		if j['book_id'] == str(d_bookId) :
			cur_d_info = j
			break

	if cur_d_info == {} :
		print 'Mentioned BookId is not listed in the search'
		os._exit(0)

	bookname = ''
	author = ''

	for k in sb_obj.available_books :
		if k.find_all('td')[0].text == str(d_bookId) :
			bookname = k.find_all('td')[2].text
			author = k.find_all('td')[1].text
			break

	print '%s by %s is selected.' % (bookname, author)

	cur_d_info['bookname'] = bookname
	cur_d_info['author'] = author

	d_mirror = raw_input('Select the download Mirror(1-3) : ')

	try :
		d_mirror = int(d_mirror)
	except :
		print 'Mirror should be integer'
		os._exit(0)

	d_obj = DownloadBook(cur_d_info, d_mirror)

if __name__ == '__main__':

	main()