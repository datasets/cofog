'''Extract COFOG codes into usable (csv) form.


TODO: do other languages (French, Spanish, Russian)
TODO: footnotes about CS and IS ...
'''
import csv
import os
import zipfile
import commands
from StringIO import StringIO

from swiss.cache import Cache

cache_path = os.path.join(os.path.dirname(__file__), 'cache')
cache = Cache(cache_path)

access_db_zip_url = 'http://unstats.un.org/unsd/cr/registry/regdntransfer.asp?f=186'
details_table_name = 'tblTitles_English_COFOG'
db_filename = 'COFOG_english.mdb'
db_filepath = cache.cache_path(db_filename)

def retrieve():
    '''Retrieve remove files into local cache.
    '''
    fp = cache.retrieve(access_db_zip_url)
    zipfo = zipfile.ZipFile(fp)
    # extract is in 2.6
    # zipfo.extract('COFOG_english.mdb', cache.path)
    out = zipfo.read(db_filename)
    open(db_filepath, 'w').write(out)
    assert os.path.exists(db_filepath), '%s does not exist' % db_filepath

def show_schema(): 
    '''Show the COFOG access db schema'''
    # mdb-schema COFOG_english.mdb 
    # mdb-export COFOG_english.mdb tblTitles_English_COFOG
    infocmd = 'mdb-schema %s' % db_filepath
    status, output = commands.getstatusoutput(infocmd)
    assert not status, 'FAILED: %s\n%s' % (infocmd, output)
    # check they have kept with known table structure
    assert 'tblStructure_COFOG' in output
    assert details_table_name in output

def export_to_csv():
    '''Export from access db to csv'''
    exportcmd = 'mdb-export %s %s' % (db_filepath, details_table_name)
    status, output = commands.getstatusoutput(exportcmd)
    assert not status, 'FAILED: %s\n%s' % (exportcmd, output)

    def read_csv():
        fo = StringIO(output)
        reader = csv.reader(fo)
        # Code,Description,ExplanatoryNote,Change_date
        headings = reader.next()
        for idx,(code,description,details,change_date) in enumerate(reader):
            pass
    open('cofog.csv', 'w').write(output) 


from swiss.clitools import *
if __name__ == '__main__':
    _main(locals())


