import datetime
import numpy as np

from pynwb import NWBHDF5IO, NWBFile
from pynwb.core import DynamicTableRegion
from pynwb.testing import TestCase, remove_test_file

from ndx_fiber_photometry import (
    Indicator,
    OpticalFiber,
    ExcitationSource,
    Photodetector,
    DichroicMirror,
    OpticalFilter,
    FiberPhotometryTable,
    FiberPhotometryResponseSeries,
    CommandedVoltageSeries,
    MultiCommandedVoltage,
)


def set_up_nwbfile():
    nwbfile = NWBFile(
        session_description="session_description",
        identifier="identifier",
        session_start_time=datetime.datetime.now(datetime.timezone.utc),
    )
    return nwbfile


class TestIntegrationRoundtrip(TestCase):
    """
    Full Roundtrip Integration Test
    Creates, writes, and reads instances of:
        Indicator,
        OpticalFiber,
        ExcitationSource,
        Photodetector,
        DichroicMirror,
        OpticalFilter,
        FiberPhotometryTable,
        FiberPhotometryResponseSeries,
        CommandedVoltageSeries,
        MultiCommandedVoltage,
    """

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):

        indicator_green = Indicator(
            name="Green Indicator",
            description="indicator",
            label="GCamp6f",
            injection_location="VTA",
            injection_coordinates_in_mm=(3.0, 2.0, 1.0),
        )
        indicator_red = Indicator(
            name="Red Indicator",
            description="indicator",
            label="Tdtomato",
            injection_location="VTA",
            injection_coordinates_in_mm=(3.0, 2.0, 1.0),
        )

        optical_fiber_1 = OpticalFiber(
            name="optical_fiber_1",
            model="fiber_model",
            numerical_aperture=0.2,
        )
        optical_fiber_2 = OpticalFiber(
            name="optical_fiber_2",
            model="fiber_model",
            numerical_aperture=0.2,
        )

        excitation_source_1 = ExcitationSource(
            name="excitation_source_1",
            description="excitation sources for green indicator",
            model="laser model",
            illumination_type="laser",
            excitation_wavelength_in_nm=470.0,
        )
        excitation_source_2 = ExcitationSource(
            name="excitation_source_2",
            description="excitation sources for red indicator",
            model="laser model",
            illumination_type="laser",
            excitation_wavelength_in_nm=525.0,
        )

        photodetector_1 = Photodetector(
            name="photodetector_1",
            description="photodetector for green emission",
            detector_type="PMT",
            detected_wavelength_in_nm=520.0,
            gain=100.0,
        )
        photodetector_2 = Photodetector(
            name="photodetector_2",
            description="photodetector for red emission",
            detector_type="PMT",
            detected_wavelength_in_nm=585.0,
            gain=100.0,
        )

        dichroic_mirror_1 = DichroicMirror(
            name="dichroic_mirror_1",
            description="Dichroic mirror for green indicator",
            model="dicdichroic mirror model",
            cut_on_wavelength_in_nm=470.0,
            transmission_bandwidth_in_nm=(460.0, 480.0),
            cut_off_wavelength_in_nm=500.0,
            reflection_bandwidth_in_nm=(490.0, 520.0),
            angle_of_incidence_in_degrees=45.0,
        )

        dichroic_mirror_2 = DichroicMirror(
            name="dichroic_mirror_2",
            description="Dichroic mirror for red indicator",
            model="dicdichroic mirror model",
            cut_on_wavelength_in_nm=525.0,
            transmission_bandwidth_in_nm=(515.0, 535.0),
            cut_off_wavelength_in_nm=585.0,
            reflection_bandwidth_in_nm=(575.0, 595.0),
            angle_of_incidence_in_degrees=45.0,
        )

        optical_filter_1 = OpticalFilter(
            name="optical_filter_1",
            description="emission filter for green indicator",
            model="emission filter model",
            peak_wavelength_in_nm=500.0,
            bandwidth_in_nm=(490.0, 520.0),
            filter_type="emission filter",
        )
        optical_filter_2 = OpticalFilter(
            name="optical_filter_2",
            description="emission filter for red indicator",
            model="emission filter model",
            peak_wavelength_in_nm=585.0,
            bandwidth_in_nm=(575.0, 595.0),
            filter_type="emission filter",
        )

        multi_commanded_voltage = MultiCommandedVoltage()

        commandedvoltage_series_1 = multi_commanded_voltage.create_commanded_voltage_series(
            name="commandedvoltage_series_1", data=[1.0, 2.0, 3.0], frequency=30.0, rate=30.0, unit="volts"
        )
        commandedvoltage_series_2 = multi_commanded_voltage.create_commanded_voltage_series(
            name="commandedvoltage_series_2",
            data=[4.0, 5.0, 6.0],
            rate=30.0,
            unit="volts",
        )

        fiber_photometry_table = FiberPhotometryTable(
            name="fiber_photometry_table",
            description="fiber photometry table",
        )
        fiber_photometry_table.add_row(
            location="VTA",
            coordinates=(3.0, 2.0, 1.0),
            indicator=indicator_green,
            optical_fiber=optical_fiber_1,
            excitation_source=excitation_source_1,
            commandedvoltage_series=commandedvoltage_series_1,
            photodetector=photodetector_1,
            dichroic_mirror=dichroic_mirror_1,
            emission_filter=optical_filter_1,
        )
        fiber_photometry_table.add_row(
            location="VTA",
            coordinates=(3.0, 2.0, 1.0),
            indicator=indicator_red,
            optical_fiber=optical_fiber_2,
            excitation_source=excitation_source_2,
            commandedvoltage_series=commandedvoltage_series_2,
            photodetector=photodetector_2,
            dichroic_mirror=dichroic_mirror_2,
            emission_filter=optical_filter_2,
        )

        fiber_photometry_table_region = DynamicTableRegion(
            name="fiber_photometry_table_region", data=[0], description="source fibers", table=fiber_photometry_table
        )

        fiber_photometry_response_series = FiberPhotometryResponseSeries(
            name="fiber_photometry_response_series",
            description="my roi response series",
            data=np.random.randn(100, 1),
            unit="F",
            rate=30.0,
            fiber_photometry_table_region=fiber_photometry_table_region,
        )

        self.nwbfile.add_device(indicator_green)
        self.nwbfile.add_device(indicator_red)
        self.nwbfile.add_device(optical_fiber_1)
        self.nwbfile.add_device(optical_fiber_2)
        self.nwbfile.add_device(excitation_source_1)
        self.nwbfile.add_device(excitation_source_2)
        self.nwbfile.add_device(photodetector_1)
        self.nwbfile.add_device(photodetector_2)
        self.nwbfile.add_device(dichroic_mirror_1)
        self.nwbfile.add_device(dichroic_mirror_2)
        self.nwbfile.add_device(optical_filter_1)
        self.nwbfile.add_device(optical_filter_2)

        self.nwbfile.add_acquisition(multi_commanded_voltage)
        self.nwbfile.add_acquisition(fiber_photometry_table)
        self.nwbfile.add_acquisition(fiber_photometry_response_series)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(
                self.nwbfile.acquisition["fiber_photometry_table"], read_nwbfile.acquisition["fiber_photometry_table"]
            )
            self.assertContainerEqual(
                fiber_photometry_response_series, read_nwbfile.acquisition["fiber_photometry_response_series"]
            )