import sys, imp, os
from bs4 import BeautifulSoup
from pytube import YouTube
import requests 
from urlparse import urljoin

def downloaded(loc, filename):
    """ Check if the video is already downloaded in the required folder OR not.
        There is some code that takes care of some encoding issues.
        
        loc : location to be checked for the already downloaded video
        filename : name of the video to be searched 
    """
    filenames = os.listdir(loc)
    filename = str(filename.encode('utf-8','ignore'))
    search_file=''
    for ch in filename:
        if ch.isalpha() or ch.isdigit():
            search_file=search_file+ch
    for _file in filenames:
        file_present=''
        for ch in _file:
            if ch.isalpha() or ch.isdigit():
                file_present=file_present+ch
        if str(search_file) in str(file_present):
            return True
    return False
 
def parse(url):
    """ Parse a youtube playlist page to extract links of all videos and return the links as a list.
        The url of the playlist will be given as input to the function.
    
        url : the web address of the Youtube Playlist
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    a_tags = soup.find_all("a",{"class":["yt-uix-tile-link","playlist-video"]})
    links = []
    base_href = "https://www.youtube.com"
    for ele in a_tags:
        link=urljoin(base_href,str(ele.get('href')))
        links.append(link)
    return links

def download_videos(links, loc, quality):
    """ Download the video in the lowest mp4 quality available and store it in a folder.
        Age-restricted videos are ignored.
        
        The Downloading resumes if there was any interruption last time.
        
        links   : list of the links in the Youtube Playlist
        loc     : file location for the downloading of videos
        quality : 1 for best quality & 2 for minimum quality
    """
    print "\nPress Ctrl+Z for stopping downloads at any moment.\n"
    print "DOWNLOADING " + str(len(links)) + " VIDEOS \n"
    video_count=0
    for link in links:
        try:
            video_count=video_count+1
            yt = YouTube(link)
            yt.set_filename(yt.filename)
            print "Video #" + str(video_count) + ": \t"+ str(yt.filename.encode('ascii','ignore'))
            if downloaded(loc,yt.filename):
                print "\t\tAlready Downloaded \n"
                continue
            quality_idx=0
            if quality==1:
                quality_idx=-1
            video = yt.filter('mp4')[quality_idx] 
            print "\t\tDownloading ........"
            video.download(loc)
            print "\t\tDownload Done \n"
        except:
            print "Video #" + str(video_count) + ": \t" + "Could Not Download" + "\n"

if __name__ == '__main__':
    """ Two Command line arguments expected :
        1.)Link to the Youtube Playlist (To be downloaded) 
        2.)The location (absolute) where it is to be downloaded
    """
    print "Please make sure if you have already run the following: \n"
    print "\tpip install -r requirements.txt\n"
    inp = raw_input("Press y to continue OR n to break. [y/n]: ")
    if inp=='n' or inp=='N':
        exit()
    quality_inp = int(raw_input("Type 1 for Downloading in maximum quality OR 2 for minimum quality : "))
    url = str(sys.argv[1])
    my_links = parse(url)
    location = str(sys.argv[2])
    location.replace('\\','/')
    download_videos(my_links, location, quality_inp)
