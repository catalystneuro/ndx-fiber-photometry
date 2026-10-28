import json

import h5py
import numpy as np
import pytest
from pynwb import NWBHDF5IO
from pynwb.testing.mock.file import mock_NWBFile

from ndx_fiber_photometry import FiberPhotometryResponseSeries

PROCESSING_PARAMETERS = json.dumps({"bandpass_filter": {"freq_min": 0.2, "freq_max": 5.0}, "zscore": {"seed": 0}})


@pytest.fixture
def processed_series():
    return FiberPhotometryResponseSeries(
        name="processed_series",
        description="Band-pass filtered and z-scored 465 nm channel.",
        data=np.arange(20.0).reshape(10, 2),
        unit="n.a.",
        rate=30.0,
        processing_parameters=PROCESSING_PARAMETERS,
        processing_software="fiber-mosaic",
        processing_software_version="0.1.0",
    )


@pytest.fixture
def nwbfile_path(tmp_path, processed_series):
    nwbfile = mock_NWBFile()
    ophys_module = nwbfile.create_processing_module(name="ophys", description="Processed fiber photometry.")
    ophys_module.add(processed_series)
    path = tmp_path / "processed.nwb"
    with NWBHDF5IO(path, mode="w") as io:
        io.write(nwbfile)
    return path


class TestFiberPhotometryResponseSeries:
    def test_roundtrip_processing_parameters(self, nwbfile_path):
        with NWBHDF5IO(nwbfile_path, mode="r") as io:
            read_series = io.read().processing["ophys"]["processed_series"]
            assert read_series.processing_parameters == PROCESSING_PARAMETERS
            assert read_series.processing_software == "fiber-mosaic"
            assert read_series.processing_software_version == "0.1.0"

    def test_processing_software_is_stored_on_the_parameters_dataset(self, nwbfile_path):
        with h5py.File(nwbfile_path, mode="r") as file:
            parameters_dataset = file["processing/ophys/processed_series/processing_parameters"]
            assert parameters_dataset.attrs["processing_software"] == "fiber-mosaic"
            assert parameters_dataset.attrs["processing_software_version"] == "0.1.0"

    def test_processing_parameters_default_to_none(self):
        series = FiberPhotometryResponseSeries(
            name="raw_series",
            description="Demodulated photoreceiver output of the 465 nm channel.",
            data=np.zeros((10, 1)),
            unit="V",
            rate=30.0,
        )
        assert series.processing_parameters is None
        assert series.processing_software is None
        assert series.processing_software_version is None

    def test_processing_parameters_require_software_and_version(self):
        with pytest.raises(ValueError, match="must be given together"):
            FiberPhotometryResponseSeries(
                name="processed_series",
                description="Band-pass filtered 465 nm channel.",
                data=np.zeros((10, 1)),
                unit="n.a.",
                rate=30.0,
                processing_parameters=PROCESSING_PARAMETERS,
                processing_software="fiber-mosaic",
            )

    def test_processing_parameters_must_be_json(self):
        with pytest.raises(json.JSONDecodeError):
            FiberPhotometryResponseSeries(
                name="processed_series",
                description="Band-pass filtered 465 nm channel.",
                data=np.zeros((10, 1)),
                unit="n.a.",
                rate=30.0,
                processing_parameters="freq_min=0.2",
                processing_software="fiber-mosaic",
                processing_software_version="0.1.0",
            )

    def test_reading_malformed_processing_parameters_warns(self, nwbfile_path):
        # another writer, such as MatNWB, could store text that is not JSON
        with h5py.File(nwbfile_path, mode="r+") as file:
            file["processing/ophys/processed_series/processing_parameters"][()] = "freq_min=0.2"

        with NWBHDF5IO(nwbfile_path, mode="r") as io:
            with pytest.warns(UserWarning, match="processing_parameters of 'processed_series' is not valid JSON"):
                read_series = io.read().processing["ophys"]["processed_series"]
            assert read_series.processing_parameters == "freq_min=0.2"
