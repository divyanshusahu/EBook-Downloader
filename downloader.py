#!/usr/bin/python2.7

import requests
from bs4 import BeautifulSoup
import optparse
import sys

ROOT_URL = 'http://gen.lib.rus.ec/'

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
		for r in range(8) :
			print headings[r] + " => " + item[r]

def main() :	
	parser = optparse.OptionParser()
	parser.add_option('-s', help="Search for ebook by name", dest="bname")
	parser.add_option('-d', help="download book by id", dest="bdwl")

	(options, args) = parser.parse_args()

	if len(sys.argv) == 1 :
		print parser.print_help()
		exit(0)

	if sys.argv[1] == '-s' :
		bookName = options.bname
		searchBook(bookName)


if __name__ == '__main__':
	main()