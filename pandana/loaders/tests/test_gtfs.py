import pytest
import requests
import zipfile
import StringIO

import pandana
from pandana.loaders.gtfs import GTFS
from pandana.testing import skipiftravis

gtfs_file = "http://www.gtfs-data-exchange.com/agency/alamedaoakland-ferry/latest.zip"

def test_gtfs():
    r = requests.get(gtfs_file)
    z = zipfile.ZipFile(StringIO.StringIO(r.content))
    gtfs = GTFS(z)

    assert gtfs.agencies_df is not None
    assert len(gtfs.agencies_df) == 4
    assert gtfs.routes_df is not None
    assert gtfs.stops_df is not None

    print gtfs.agencies_df
