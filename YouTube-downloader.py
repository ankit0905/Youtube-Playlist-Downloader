import sys, imp, os
from bs4 import BeautifulSoup
from pytube import YouTube
import requests 

def downloaded(loc, filename):
    """ Check if the video is already downloaded in the required folder OR not.
    """
    filenames = os.listdir(loc)
    filename = str(filename.encode('ascii','ignore'))
    search_file=''
    for ch in filename:
        if ch.isalpha() or ch.isdigit():
            search_file=search_file+ch
    for _file in filenames:
        file_present=''
        for ch in _file:
            if ch.isalpha() or ch.isdigit():
                file_present=file_present+ch
        if search_file in file_present:
            return True
    return False
 
def parse(url):
    """ Parse a youtube playlist page to extract links of all videos and return the links as a list.
    The url of the playlist will be given as input to the function.
    
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    a_tags = soup.find_all("a",{"class":"yt-uix-tile-link"})
    links = []
    for ele in a_tags:
        link="https://www.youtube.com"+str(ele.get('href'))
        links.append(link)
    return links

def download_videos(links, loc):
    """ Download the video in the lowest mp4 quality available and store it in a folder.
        Age-restricted videos are ignored.
        
        The Downloading resumes if there was any interruption last time.
    """
    print 
    print "Press Ctrl+Z for stopping downloads at any moment.\n"
    print "DOWNLOADING " + str(len(links)) + " VIDEOS \n"
    ct=0
    for link in links:
        ct=ct+1
        try:
            yt = YouTube(link)
            yt.set_filename(yt.filename)
            print "Video #" + str(ct) + ": \t"+ (yt.filename)
            if downloaded(loc,yt.filename):
                print "\t\tAlready Downloaded \n"
                continue
            print "\t\tDownloading ........"
            print "\t\tDownload Done \n"
            video = yt.filter('mp4')[0] 
            video.download(loc)
        except:
            print "Video #" + str(ct) + ": \t" + "Could Not Download" + "\n"

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