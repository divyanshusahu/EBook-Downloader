#!/usr/bin/python2.7

import requests
from bs4 import BeautifulSoup
import optparse
import sys
import os

ROOT_URL = 'http://gen.lib.rus.ec/'
DOWNLOAD_ROOT_URL = 'https://libgen.pw/item/detail/id/'
DOWNLOAD_URL = 'https://libgen.pw'

def searchBook(name) :
	name =name.replace(' ','+')
	url = ROOT_URL + 'search.php?req=' + str(name) + '&lg_topic=libgen&open=0&view=simple&res=25&phrase=0&column=def'
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "lxml")
	book_lists = soup.find_all("table")[2]
	
	# there are total 4 tables inside the page, and the third table is storing the list of book
	
	headings = []
	for h in book_lists.tr.find_all("td") :
		headings.append(h.text.encode('utf-8'))
	#print headings

	no_of_available_books = len(book_lists.find_all("tr"))
	print "\n" + str(no_of_available_books - 1) + " Books found."
	available_books = []

	for i in range(1,no_of_available_books) :
		available_books.append(book_lists.find_all("tr")[i])
	# available_books contains list of available books with <tr>

	available_books_details = []
	for b in available_books :
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

def downloadBook(bookID) :
	download_url = DOWNLOAD_ROOT_URL + str(bookID) + "?id=" + str(bookID)
	r = requests.get(download_url)
	
	if r.status_code == 404 :
		print "Book not found"
		os._exit(0)
	
	soup = BeautifulSoup(r.text, "lxml")
	bookClass = soup.find_all("div",{'class','book'})
	durl = ''
	bookname = ''
	for b1 in bookClass :
		durl = b1.find_all("a")[0]['href']
	durl = DOWNLOAD_URL + durl

	for b2 in bookClass :
		bookname = b2.find_all("div", {'class':'book-info__title'})[0].text

	r2 = requests.get(durl)
	soup2 = BeautifulSoup(r2.text, "lxml")
	download_url = soup2.find_all("a")[0]['href']
	download_url = DOWNLOAD_URL + download_url

	r3 = requests.get(download_url, stream=True)
	with open(bookname,"wb") as f :
		print "Downloading %s" % bookname
		f.write(r3.content)

def main() :	
	parser = optparse.OptionParser()
	parser.add_option('-s', help="Search for ebook by name", dest="bname")
	parser.add_option('-d', help="Download book by id", dest="bdwl")

	(options, args) = parser.parse_args()

	if len(sys.argv) == 1 :
		print str(parser.print_help())[:-4]
		os._exit(0)

	if sys.argv[1] == '-s' :
		bookName = options.bname
		if len(bookName) <= 3 :
			print "Book name must be greater then 3 character string"
			os._exit(0)
		searchBook(bookName)

	if sys.argv[1] == '-d' :
		bookID = options.bdwl
		downloadBook(bookID)

if __name__ == '__main__':
	main()