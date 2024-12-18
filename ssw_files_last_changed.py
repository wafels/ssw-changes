import os
import time
from astropy.time import Time
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
 
def list_files_recursive(path, extension='.pro'):
    """Recursively lists files and their modification times in a directory."""
    # Extension
    len_extension = len(extension)

    # Storage for the times
    mtimes = []

    # Walk the path get each file, and get its last modifcation date
    for root, dirs, files in os.walk(path):
        for f in files:
            filepath = os.path.join(root, f)
            # Make sure we are only considering actual files that have the correct extension
            if os.path.isfile(filepath) and filepath[-len_extension:] == extension:
                try:
                    mtime = os.path.getmtime(filepath)
                except:
                    print('A problem')
                mtimes.append(mtime)

    # Return the modification times for all the appropriate files.
    return Time(np.asarray(mtimes), format='unix')

class Mission:
    def __init__(self, name, launch=None, end=None, note=None, nicknames=None):
        self.name = name
        self.launch = parse_time(launch)
        if self.end is not None:
            self.end = parse_time(end)
            if self.launch > self.end:
                raise Exception('Launch date is after end date.')
        self.note = note
        self.nicknames = [self.name]
        if nicknames is not None:
            for nickname in nicknames:
                self.nicknames.append(nickname)

    def is_operational_now(self):
        if self.end is None:
            return True
        return False

    def nominally_operational(self, date):
        t = parse_time(date)
        if (self.end is None) and (t >= self.launch):
            return True
        else:
            return (self.launch <= t) and (t <= self.end)

iris = Mission('IRIS', launch='2013-06-07')
stereo = Mission('STEREO', launch='2006-10-25', note='STEREO-A is operational. STEREO-B not operational since 2014 October 01.')
rhessi = Mission('RHESSI', launch='2002-02-05', end='2018-08-16', nicknames=['HESSI'])
trace = Mission('TRACE', launch='1998-04-01', end='2010-06-21', note='Instrument is no longer operational and the last science image taken on 2010 June 21.')
hinode = Mission('Hinode', launch='2006-09-22', note='All instruments are operational except SOT-FG (ceased operations 2016 February 25).')
so = Mission('Solar Orbiter', launch='2020-02-10', nicknames=['so', 'solo'])


missions = [iris, stereo, rhessi, trace, hinode, so]

# TODO
# Add up total number of files changed in all the subdirectories
# Calculate fractional changes for each subdirectory
# Calculate fractional changes for all the subdirectories
# Rank by percentage changes in the past N years?

basepath = os.path.expanduser('~/ssw/')

# These are the specific parts of SSW that we are looking to measure changes
paths = ['gen','goesn','goesr','hessi','hinode','iris','offline','proba2','radio',
             'sdo','site','so','soho','stereo','trace','vobs','yohkoh','packages/azam',
             'packages/binaries','packages/chianti','packages/mjastereo','packages/nrl',
             'packages/s3drs','packages/sbrowser','packages/spex','packages/sunspice',
             'packages/xray']

# Number of places we are looking for changes
n = len(paths)

#
output = os.path.expanduser('~/sdac_code/ssw_changes/output/')

for i, p in enumerate(paths):
    fullpath = os.path.join(basepath, p)
    file_times = list_files_recursive(fullpath)
    nfiles = len(file_times)
    difference = ((Time.now() - file_times).to(u.year)).to_value()
    
    plt.hist(difference, bins=np.linspace(0,40,81))
    plt.xlabel('Years since last mod')
    plt.ylabel('# files')
    plt.grid(linestyle=':')
    plt.title(p + ' ('+str(nfiles)+' files in subdirectory)')
    plt.xlim([0,5])

    filename = p.replace('/', '_')
    filepath = output + filename
    plt.savefig(filepath + '.png')
    plt.close('all')
    
stop


# Number of rows in the output figure
nrows = int(n / 4) +1

# Set up the figure
plt.figure(1,figsize=(16,9))
plt.subplots_adjust(left=0.05,right=0.98,top=0.95,bottom=0.05,hspace=0.6,wspace=0.25)
plt.tight_layout()


for i, p in enumerate(paths):
    fullpath = os.path.join(basepath,p)
    difference = ((Time.now() - list_files_recursive(fullpath)).to(u.year)).to_value()
    total_files = len(list_files_recursive(fullpath))                
    
    #fig, ax = plt.subplot(4,nrows,i+1)
    plt.subplot(nrows,4,i+1)
 #   ax.hist(difference, bins=100)
    plt.hist(difference, bins=np.linspace(0,40,81))
    plt.xlabel('Years since last mod')
    plt.ylabel('# files')
    plt.grid(':')
    plt.title(p,y=1.0,pad=-12,color='red')
    plt.xlim([0,5])

plt.savefig('ssw_time_since_file_updated_all.png')
plt.show()

munit = u.year
munit_string = str(munit)

fig, ax = plt.subplots(nrows,4,i+1)

for i, p in enumerate(paths):

    difference = ((Time.now() - list_files_recursive(path)).to(munit)).to_value()

    nfiles = len(difference)

    ax.hist(difference, bins=500, density=False)
    ax.set_xlabel('time since last modification (' + munit_string + ')')
    ax.set_ylabel('number of file objects')
    ax.set_yscale('log')
    ax.set_title(path + ' [#files = '+str(nfiles)+']')
    ax.grid(linestyle=':')

    plt.show()

