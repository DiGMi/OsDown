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


def download_subtitle(subtitle, file_name=None):
    print 'Downloading %s...' % subtitle['SubFileName']
    tempfile = mktemp()
    urllib.urlretrieve(subtitle['SubDownloadLink'], tempfile)
    if file_name is None:
        file_name = subtitle['SubFileName']
    with gzip.open(tempfile, 'rb') as gz, open(file_name, 'wb') as f:
        f.write(gz.read())
    os.remove(tempfile)


def choose_subtitles(subtitles):
    while True:
        i = 0
        print 'There are several subtitles available:'
        for s in subtitles:
            i += 1
            print '%d:\t%s' % (i, s['SubFileName'])
        print 'Enter your choice:',
        c = raw_input()
        if not c.isdigit():
            print 'Invalid input!'
            continue
        c = int(c)
        if c < 1 or c > i:
            print 'Invalid option!'
            continue
        return subtitles[c-1]


def usage():
    import sys
    print "%s <filename> [<langid>]" % sys.argv[0]


def main():
    import sys
    if len(sys.argv) < 2:
        usage()
        return
    langid = config.get('Language', 'langid')
    rename = config.get('General', 'rename')
    if len(sys.argv) >= 3:
        langid = sys.argv[2]
    subtitles = find_subtitles(sys.argv[1], langid)

    if len(subtitles) == 0:
        print "No subtitles found!"
        return

    to_download = subtitles[0]
    if len(subtitles) > 1:
        to_download = choose_subtitles(subtitles)

    file_name = None
    if rename:
        file_name = '%s%s' % (os.path.splitext(sys.argv[1])[0],
                               os.path.splitext(to_download['SubFileName'])[1])

    download_subtitle(to_download, file_name)


if __name__ == '__main__':
    main()
