#OsDown

A script that downloads subtitles from opensubtitles automatically for a given language

#Requirements
The script requires the python-opensubtitles module which can be found at: https://github.com/agonzalezro/python-opensubtitles

#Usage
First, edit the osdown.cfg file and add your username and password in the Login section.
You can also select your default language id (currently set to heb - for hebrew)
When running 'python osdown.py <filepath>' the script will download the subtitle, if few were found it will display a menu allowing the user to choose which subtitle he wish to download.

#Configuration

##General
* rename - When set to true, the script will rename the subtitles file to the name of the movie (only will change the extension), otherwise the original subtitles name will remain.
* download_first - When downloading subtitles for a single file, should the script automatically download the first subtitle or query the user when several option available?
* download_first_on_multiple - When downloading subtitles for multiple files, should the script automatically download the first subtitle or query the user when several options available?

##Login
* user - The username for opensubtitles.org
* pass - The password for opensubtitles.org

##Language
* langid - The default language identifier.
