"""
Tools for creating Pandana networks from General Transit Feed Service (what a name)

I get my gtfs files from here: http://www.gtfs-data-exchange.com/
"""

import zipfile
import pandas as pd

class GTFS:

    def __init__(self, zipfile_or_filename):
        if isinstance(zipfile_or_filename, str):
            self.zipfile = zipfile.ZipFile(zipfile_or_filename)
        else:
            self.zipfile = zipfile_or_filename
        self.read()

    def read(self):
        z = self.zipfile
        print "here"
        self.agencies_df = pd.read_csv(z.open('agency.txt'))
        self.routes_df = pd.read_csv(z.open('routes.txt'))
        self.calendar_df = pd.read_csv(z.open('calendar.txt'))
        self.stops_df = pd.read_csv(z.open('stops.txt'))
        self.trips_df = pd.read_csv(z.open('trips.txt'))
        self.shapes_df = pd.read_csv(z.open('shapes.txt'))
        self.stop_times_df = pd.read_csv(z.open('stop_times.txt'))
        self.calendar_dates_df = pd.read_csv(z.open('calendar_dates.txt'))
