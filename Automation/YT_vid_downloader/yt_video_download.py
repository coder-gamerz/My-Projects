from pytube import YouTube
from sys import argv

link = 'https://www.youtube.com/watch?v=a7DryiA60nY&ab_channel=BecauseScience'

yt = YouTube(link)

y = yt.streams.get_highest_resolution()

y.download(output_path=r'C:\Users\shrey\OneDrive\Documents\Automation\YT_vid_downloader\Downloaded_vids')

print('Completed downloading video!')

# A simple YT video downloader
