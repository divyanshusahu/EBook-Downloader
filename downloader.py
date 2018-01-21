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
	soup = BeautifulSoup(r.text)
	print soup.prettify()


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