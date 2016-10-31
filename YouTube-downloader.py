import sys, imp, os

def check_module(libs = []):
    """Check if the list of modules is available. 
    
    If not, first install the modules using pip.
    """
    for lib in libs:
        try:
            imp.find_module(lib)
            found = True
        except ImportError:
            found = False
        if not found:
            os.system('pip install ' + lib)

def parse(url):
    """ Parse a youtube playlist page to extract links of all videos and return the links as a list.
        
    The url of the playlist will be given as input to the function.
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    a_tags = soup.find_all('a')
    links = []
    for ele in a_tags:
        link="https://www.youtube.com"+str(ele.get('href'))
        s='index='
        if s in link:
            links.append(link)
    links = list(set(links))
    return links

def download_videos(links, loc):
    """ Download the video in the lowest mp4 quality available and store it in a folder.
        Age-restricted videos are ignored.
    """
    ct=0
    for link in links:
        ct=ct+1
        try:
            yt = YouTube(link)
            yt.set_filename(yt.filename+str(ct))
            print(yt.filename)
            video = yt.filter('mp4')[0]
            video.download(loc)
            print "Download done."
        except:
            continue

if __name__ == '__main__':
    """ Command line argument expected : Link to the Youtube Playlist (To be downloaded)"""
    url = str(sys.argv[1])
    url.replace('&', '^&')
    print url
    modules = ['bs4', 'requests', 'pytube']
    #print modules
    check_module(modules)
    from bs4 import BeautifulSoup
    from pytube import YouTube
    import requests 
    my_links = parse(url)
    location = "C:/Users/swamiji/Documents/ANKIT/python/bs4/video1"
    download_videos(my_links, location)
    
    
    