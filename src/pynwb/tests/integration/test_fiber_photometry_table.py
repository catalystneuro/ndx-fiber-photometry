import numpy as np
import pytest
from pynwb import NWBHDF5IO
from pynwb.testing.mock.file import mock_NWBFile
from ndx_ophys_devices.testing import (
    mock_ExcitationSource,
    mock_Indicator,
    mock_OpticalFiber,
    mock_Photodetector,
)

from ndx_fiber_photometry import FiberPhotometry, FiberPhotometryIndicators, FiberPhotometryTable


@pytest.fixture
def nwbfile():
    nwbfile = mock_NWBFile()
    indicator = mock_Indicator(name="indicator_green", viral_vector_injection=None)
    optical_fiber = mock_OpticalFiber(name="optical_fiber")
    excitation_source = mock_ExcitationSource(name="excitation_source_470")
    photodetector = mock_Photodetector(name="photodetector")
    for device in (optical_fiber, excitation_source, photodetector):
        nwbfile.add_device_model(device.model)
        nwbfile.add_device(device)

    fiber_photometry_table = FiberPhotometryTable(name="fiber_photometry_table", description="fiber photometry table")
    # a pulsed recording reads each sample once with the LED on and once with it off
    for excitation_wavelength_in_nm in (470.0, np.nan):
        fiber_photometry_table.add_row(
            location="VTA",
            excitation_wavelength_in_nm=excitation_wavelength_in_nm,
            emission_wavelength_in_nm=525.0,
            indicator=indicator,
            optical_fiber=optical_fiber,
            excitation_source=excitation_source,
            photodetector=photodetector,
        )
    nwbfile.add_lab_meta_data(
        FiberPhotometry(
            name="fiber_photometry",
            fiber_photometry_table=fiber_photometry_table,
            fiber_photometry_indicators=FiberPhotometryIndicators(indicators=[indicator]),
        )
    )
    return nwbfile


class TestFiberPhotometryTable:
    def test_roundtrip_row_without_excitation(self, tmp_path, nwbfile):
        path = tmp_path / "dark_row.nwb"
        with NWBHDF5IO(path, mode="w") as io:
            io.write(nwbfile)

        with NWBHDF5IO(path, mode="r") as io:
            read_table = io.read().lab_meta_data["fiber_photometry"].fiber_photometry_table
            np.testing.assert_array_equal(read_table["excitation_wavelength_in_nm"][:], [470.0, np.nan])
