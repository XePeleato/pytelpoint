# Licensed under a 3-clause BSD style license - see LICENSE.rst

import gzip
import pkg_resources
import pickle
import os

from matplotlib.testing.decorators import cleanup

import astropy.units as u
from astropy.coordinates import Angle, AltAz, SkyCoord
from astropy.time import Time

from tpoint.constants import MMT_LOCATION
from tpoint.transform import tpoint
from tpoint.visualization import pointing_histogram, pointing_azel_resid, pointing_residuals, \
    pointing_sky, plot_corner, plot_posterior

OBSTIME = Time("2021-08-21T06:00:00", format='isot')
AA_FRAME = AltAz(obstime=OBSTIME, location=MMT_LOCATION)
AZ_REF = Angle([0, 45, 90, 135, 180, 225, 270, 315, 360], unit=u.degree).wrap_at(360 * u.deg)
EL_REF = Angle([15, 20, 30, 45, 50, 60, 65, 75, 85], unit=u.degree).wrap_at(360 * u.deg)
COO_REF = SkyCoord(AZ_REF, EL_REF, frame=AA_FRAME)
COO_MOD = tpoint(COO_REF, ia=1.)

TEST_FILE = pkg_resources.resource_filename("tpoint", os.path.join("test_data", "k_and_e.pkl.gz"))
with gzip.GzipFile(TEST_FILE, 'rb') as fp:
    pkl = pickle.Unpickler(fp)
    TEST_DATA = pkl.load()


@cleanup
def test_pointing_histogram():
    f = pointing_histogram(COO_REF, COO_MOD)
    assert(f is not None)


@cleanup
def test_azel_resid():
    f = pointing_azel_resid(COO_REF, COO_MOD)
    assert(f is not None)


@cleanup
def test_pointing_resid():
    f = pointing_residuals(COO_REF, COO_MOD)
    assert(f is not None)


@cleanup
def test_pointing_sky():
    f = pointing_sky(COO_REF, COO_MOD)
    assert(f is not None)


@cleanup
def test_posterior_plot():
    f = plot_posterior(TEST_DATA)
    assert(f is not None)


@cleanup
def test_corner_plot():
    f = plot_corner(TEST_DATA)
    assert(f is not None)
