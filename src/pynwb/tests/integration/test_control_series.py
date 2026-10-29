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

from ndx_fiber_photometry import (
    DeltaFOverFResponseSeries,
    FiberPhotometry,
    FiberPhotometryIndicators,
    FiberPhotometryResponseSeries,
    FiberPhotometryTable,
    ModulatedResponseSeries,
)


@pytest.fixture
def nwbfile():
    nwbfile = mock_NWBFile()
    indicator = mock_Indicator(name="indicator_green", viral_vector_injection=None)
    optical_fiber = mock_OpticalFiber(name="optical_fiber")
    excitation_source_465 = mock_ExcitationSource(name="excitation_source_465")
    excitation_source_405 = mock_ExcitationSource(name="excitation_source_405")
    photodetector = mock_Photodetector(name="photodetector")
    for device in (optical_fiber, excitation_source_465, excitation_source_405, photodetector):
        nwbfile.add_device_model(device.model)
        nwbfile.add_device(device)

    fiber_photometry_table = FiberPhotometryTable(name="fiber_photometry_table", description="fiber photometry table")
    for excitation_wavelength_in_nm, excitation_source in (
        (465.0, excitation_source_465),
        (405.0, excitation_source_405),
    ):
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


@pytest.fixture
def fiber_photometry_table(nwbfile):
    return nwbfile.lab_meta_data["fiber_photometry"].fiber_photometry_table


@pytest.fixture
def modulated_series(fiber_photometry_table):
    return ModulatedResponseSeries(
        name="modulated_series",
        description="Photoreceiver output with the 465 nm and 405 nm LEDs modulated at different frequencies.",
        data=np.arange(10.0),
        unit="V",
        rate=1000.0,
        fiber_photometry_table_region=fiber_photometry_table.create_fiber_photometry_table_region(
            region=[0], description="signal excitation"
        ),
        control_fiber_photometry_table_region=fiber_photometry_table.create_region(
            name="control_fiber_photometry_table_region", region=[1], description="control excitation"
        ),
    )


@pytest.fixture
def delta_f_over_f_series(fiber_photometry_table):
    return DeltaFOverFResponseSeries(
        name="delta_f_over_f_series",
        description="dF/F of the 465 nm signal, with the fitted 405 nm control as baseline.",
        data=np.arange(10.0) / 100,
        unit="n.a.",
        rate=30.0,
        fiber_photometry_table_region=fiber_photometry_table.create_fiber_photometry_table_region(
            region=[0], description="signal"
        ),
        control_fiber_photometry_table_region=fiber_photometry_table.create_region(
            name="control_fiber_photometry_table_region", region=[1], description="control"
        ),
    )


@pytest.fixture
def nwbfile_path(tmp_path, nwbfile, modulated_series, delta_f_over_f_series):
    nwbfile.add_acquisition(modulated_series)
    ophys_module = nwbfile.create_processing_module(name="ophys", description="Processed fiber photometry.")
    ophys_module.add(delta_f_over_f_series)
    path = tmp_path / "control_series.nwb"
    with NWBHDF5IO(path, mode="w") as io:
        io.write(nwbfile)
    return path


class TestModulatedResponseSeries:
    def test_is_a_fiber_photometry_response_series(self, modulated_series):
        assert isinstance(modulated_series, FiberPhotometryResponseSeries)

    def test_roundtrip(self, nwbfile_path):
        with NWBHDF5IO(nwbfile_path, mode="r") as io:
            read_series = io.read().acquisition["modulated_series"]
            assert isinstance(read_series, ModulatedResponseSeries)
            signal_rows = read_series.fiber_photometry_table_region[:]
            control_rows = read_series.control_fiber_photometry_table_region[:]
            assert signal_rows["excitation_wavelength_in_nm"].tolist() == [465.0]
            assert control_rows["excitation_wavelength_in_nm"].tolist() == [405.0]

    def test_control_region_is_required(self, fiber_photometry_table):
        with pytest.raises(TypeError, match="missing argument 'control_fiber_photometry_table_region'"):
            ModulatedResponseSeries(
                name="modulated_series",
                description="Photoreceiver output with the 465 nm and 405 nm LEDs modulated.",
                data=np.arange(10.0),
                unit="V",
                rate=1000.0,
                fiber_photometry_table_region=fiber_photometry_table.create_fiber_photometry_table_region(
                    region=[0], description="signal excitation"
                ),
            )

    def test_signal_region_is_required(self, fiber_photometry_table):
        with pytest.raises(TypeError, match="missing argument 'fiber_photometry_table_region'"):
            ModulatedResponseSeries(
                name="modulated_series",
                description="Photoreceiver output with the 465 nm and 405 nm LEDs modulated.",
                data=np.arange(10.0),
                unit="V",
                rate=1000.0,
                control_fiber_photometry_table_region=fiber_photometry_table.create_region(
                    name="control_fiber_photometry_table_region", region=[1], description="control excitation"
                ),
            )


class TestDeltaFOverFResponseSeries:
    def test_is_a_fiber_photometry_response_series(self, delta_f_over_f_series):
        assert isinstance(delta_f_over_f_series, FiberPhotometryResponseSeries)

    def test_roundtrip(self, nwbfile_path):
        with NWBHDF5IO(nwbfile_path, mode="r") as io:
            read_series = io.read().processing["ophys"]["delta_f_over_f_series"]
            assert isinstance(read_series, DeltaFOverFResponseSeries)
            np.testing.assert_array_equal(read_series.data[:], np.arange(10.0) / 100)
            signal_rows = read_series.fiber_photometry_table_region[:]
            control_rows = read_series.control_fiber_photometry_table_region[:]
            assert signal_rows["excitation_wavelength_in_nm"].tolist() == [465.0]
            assert control_rows["excitation_wavelength_in_nm"].tolist() == [405.0]

    def test_control_region_is_required(self, fiber_photometry_table):
        with pytest.raises(TypeError, match="missing argument 'control_fiber_photometry_table_region'"):
            DeltaFOverFResponseSeries(
                name="delta_f_over_f_series",
                description="dF/F of the 465 nm signal.",
                data=np.arange(10.0) / 100,
                unit="n.a.",
                rate=30.0,
                fiber_photometry_table_region=fiber_photometry_table.create_fiber_photometry_table_region(
                    region=[0], description="signal"
                ),
            )

    def test_signal_region_is_required(self, fiber_photometry_table):
        with pytest.raises(TypeError, match="missing argument 'fiber_photometry_table_region'"):
            DeltaFOverFResponseSeries(
                name="delta_f_over_f_series",
                description="dF/F of the 465 nm signal.",
                data=np.arange(10.0) / 100,
                unit="n.a.",
                rate=30.0,
                control_fiber_photometry_table_region=fiber_photometry_table.create_region(
                    name="control_fiber_photometry_table_region", region=[1], description="control"
                ),
            )
