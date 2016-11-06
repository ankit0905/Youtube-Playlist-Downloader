import sys, imp, os
from bs4 import BeautifulSoup
from pytube import YouTube
import requests 

def downloaded(loc, filename):
    """ Check if the video is already downloaded in the required folder OR not.
    """
    files = os.listdir(loc)
    for _file in files:
        if filename in _file:
            return True
    return False
 
def parse(url):
    """ Parse a youtube playlist page to extract links of all videos and return the links as a list.
    The url of the playlist will be given as input to the function.
    
    The Downloading resumes if there is any interruption.
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    a_tags = soup.find_all("a",{"class":"yt-uix-tile-link"})
    links = []
    for ele in a_tags:
        link="https://www.youtube.com"+str(ele.get('href'))
        links.append(link)
    links = list(set(links))
    return links

def download_videos(links, loc):
    """ Download the video in the lowest mp4 quality available and store it in a folder.
        Age-restricted videos are ignored.
    """
    for link in links:
        try:
            yt = YouTube(link)
            yt.set_filename(yt.filename)
            print(yt.filename)
            if downloaded(loc,yt.filename) == True:
                print "Already Downloaded"
                continue
            video = yt.filter('mp4')[0]
            print "Downloading......."
            video.download(loc)
            print "Download done."  
        except:
            continue

if __name__ == '__main__':
    """ Two Command line arguments expected :
        1.)Link to the Youtube Playlist (To be downloaded) 
        2.)The location (absolute) where it is to be downloaded
    """
    url = str(sys.argv[1])
    my_links = parse(url)
    location = str(sys.argv[2])
    location.replace('\\','/')
    download_videos(my_links, location)