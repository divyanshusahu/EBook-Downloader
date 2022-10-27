# EBook Downloader

###### This downloader is made to download the book from http://gen.lib.rus.ec/

#### Dependencies

- Python2.x
- python requests
- BeautifulSoup

#### Screenshot

<img src='s1.gif'></img>


#### log file is generated, whenever user run the script
python downloader.py


#### DockerFile to dockerise the downloader script.
docker run -it --rm --name downloader -v "$PWD":/usr/src/app -w /usr/src/app python:2 python downloader.py