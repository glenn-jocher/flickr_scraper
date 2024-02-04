import argparse
import os
import time
from dotenv import load_dotenv

from flickrapi import FlickrAPI

from utils.general import download_uri

load_dotenv()

key = os.getenv('FLICKR_API_KEY', '')
secret = os.getenv('FLICKR_API_SECRET', '')

def get_urls(search='honeybees on flowers', n=10, download=False):
    t = time.time()
    flickr = FlickrAPI(key, secret)
    license = ()  # https://www.flickr.com/services/api/explore/?method=flickr.photos.licenses.getInfo
    photos = flickr.walk(text=search,  # http://www.flickr.com/services/api/flickr.photos.search.html
                         extras='url_o',
                         per_page=500,  # 1-500
                         license=license,
                         sort='relevance')

    if download:
        dir = os.getcwd() + os.sep + 'images' + os.sep + search.replace(' ', '_') + os.sep  # save directory
        if not os.path.exists(dir):
            os.makedirs(dir)

    urls = []
    for i, photo in enumerate(photos):
        if i <= n:
            try:
                # construct url https://www.flickr.com/services/api/misc.urls.html
                url = photo.get('url_o')  # original size
                if url is None:
                    url = f"https://farm{photo.get('farm')}.staticflickr.com/{photo.get('server')}/{photo.get('id')}_{photo.get('secret')}_b.jpg"


                # download
                if download:
                    download_uri(url, dir)

                urls.append(url)
                print('%g/%g %s' % (i, n, url))
            except:
                print('%g/%g error...' % (i, n))

        else:

            # import pandas as pd
            # urls = pd.Series(urls)
            # urls.to_csv(search + "_urls.csv")
            print('Done. (%.1fs)' % (time.time() - t) + ('\nAll images saved to %s' % dir if download else ''))
            break

class PreserveQuotesAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, ' '.join(values))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', nargs='+', default='honeybees on flowers', help='flickr search term')
    # parser.add_argument('--search', type=str, default='honeybees on flowers', help='flickr search term')
    parser.add_argument('--n', type=int, default=10, help='number of images')
    parser.add_argument('--download', action='store_true', help='download images')
    opt = parser.parse_args()


    print(f'nargs {opt.search}')
    # Check key
    help_url = 'https://www.flickr.com/services/apps/create/apply'
    assert key and secret, f'Flickr API key required in flickr_scraper.py L11-12. To apply visit {help_url}'

    for search in opt.search:
        get_urls(search=search,  # search term
                 n=opt.n,  # max number of images
                 download=opt.download)  # download images
