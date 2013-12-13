#!/usr/bin/env python
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import ConfigParser
import urllib
from tempfile import mktemp
import gzip
from numbers import Number
import os


config = ConfigParser.RawConfigParser()
config.read(os.path.realpath(__file__)[:-2] + 'cfg')
osmgr = OpenSubtitles()
osmgr.login(config.get('Login', 'user'), config.get('Login', 'pass'))


def find_subtitles(path, langid='all'):
    ''' Get a list of subtitles for a given file '''
    f = File(path)
    hash = f.get_hash()
    assert type(hash) == str
    size = f.size
    assert isinstance(size, Number)
    data = osmgr.search_subtitles([{'sublanguageid': langid,
                                   'moviehash': hash,
                                   'moviebytesize': size}])
    assert type(data) == list
    return data


def download_subtitle(subtitle):
    print 'Downloading %s...' % subtitle['SubFileName']
    tempfile = mktemp()
    urllib.urlretrieve(subtitle['SubDownloadLink'], tempfile)
    with gzip.open(tempfile, 'rb') as gz, open(subtitle['SubFileName'], 'wb') as f:
        f.write(gz.read())
    os.remove(tempfile)


def usage():
    import sys
    print "%s <filename> [<langid>]" % sys.argv[0]


def main():
    import sys
    if len(sys.argv) < 2:
        usage()
        return
    langid = config.get('Language', 'langid')
    if len(sys.argv) >= 3:
        langid = sys.argv[2]
    subtitles = find_subtitles(sys.argv[1], langid)
    download_subtitle(subtitles[0])


if __name__ == '__main__':
    main()
