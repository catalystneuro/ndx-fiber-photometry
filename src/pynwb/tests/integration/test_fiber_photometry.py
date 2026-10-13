import numpy as np
import pytest

from pynwb import NWBHDF5IO
from pynwb.testing import TestCase
from pynwb.testing.mock.file import mock_NWBFile

from ndx_ophys_devices import (
    ViralVector,
    ViralVectorInjection,
    Indicator,
    StereotacticPosition,
    OpticalFiberModel,
    OpticalFiber,
    ExcitationSourceModel,
    ExcitationSource,
    PhotodetectorModel,
    Photodetector,
    DichroicMirrorModel,
    DichroicMirror,
    BandOpticalFilterModel,
    BandOpticalFilter,
    EdgeOpticalFilterModel,
    EdgeOpticalFilter,
)
from ndx_fiber_photometry import (
    FiberPhotometryViruses,
    FiberPhotometryVirusInjections,
    FiberPhotometryIndicators,
    FiberPhotometry,
    FiberPhotometryTable,
    FiberPhotometryResponseSeries,
    CommandedVoltageSeries,
)


class TestIntegrationRoundtrip(TestCase):
    """
    Full Roundtrip Integration Test
    Creates, writes, and reads instances of:
        ViralVector,
        ViralVectorInjection,
        FiberPhotometryViruses,
        FiberPhotometryVirusInjections,
        FiberPhotometryIndicators,
        Indicator,
        StereotacticPosition,
        OpticalFiberModel,
        OpticalFiber,
        ExcitationSourceModel,
        ExcitationSource,
        PhotodetectorModel,
        Photodetector,
        DichroicMirrorModel,
        DichroicMirror,
        BandOpticalFilterModel,
        BandOpticalFilter,
        EdgeOpticalFilterModel,
        EdgeOpticalFilter,
        FiberPhotometry,
        FiberPhotometryTable,
        FiberPhotometryResponseSeries,
        CommandedVoltageSeries,
    """

    @pytest.fixture(autouse=True)
    def set_path(self, tmp_path):
        self.path = tmp_path / "test.nwb"

    def setUp(self):
        self.nwbfile = mock_NWBFile()

    def test_roundtrip(self):
        viral_vector_green = ViralVector(
            name="viral_vector_green",
            description="AAV viral vector for the green indicator.",
            construct_name="AAV-CaMKII-GCaMP6f",
            manufacturer="Vector Manufacturer",
            titer_in_vg_per_ml=1.0e12,
        )

        viral_vector_red = ViralVector(
            name="viral_vector_red",
            description="AAV viral vector for the red indicator.",
            construct_name="AAV-CaMKII-jRGECO1a",
            manufacturer="Vector Manufacturer",
            titer_in_vg_per_ml=1.0e12,
        )
        viruses = FiberPhotometryViruses(viral_vectors=[viral_vector_green, viral_vector_red])

        # Coordinates use the RAS orientation relative to bregma: x is mediolateral (right is positive),
        # y is anteroposterior (anterior is positive) and z is dorsoventral (dorsal is positive).
        viral_vector_injection_green = ViralVectorInjection(
            name="viral_vector_injection_green",
            description="Viral vector injection for fiber photometry.",
            viral_injection_coordinates=StereotacticPosition(
                name="viral_injection_coordinates",
                anatomical_target="Ventral Tegmental Area (VTA)",
                origin="bregma",
                orientation="RAS",
                x_in_mm=0.5,
                y_in_mm=-3.3,
                z_in_mm=-4.4,
            ),
            volume_in_uL=0.45,
            injection_date="1970-01-01T00:00:00+00:00",
            viral_vector=viral_vector_green,
        )

        viral_vector_injection_red = ViralVectorInjection(
            name="viral_vector_injection_red",
            description="Viral vector injection for fiber photometry.",
            viral_injection_coordinates=StereotacticPosition(
                name="viral_injection_coordinates",
                anatomical_target="Ventral Tegmental Area (VTA)",
                origin="bregma",
                orientation="RAS",
                x_in_mm=-0.5,
                y_in_mm=-3.3,
                z_in_mm=-4.4,
            ),
            volume_in_uL=0.45,
            injection_date="1970-01-01T00:00:00+00:00",
            viral_vector=viral_vector_red,
        )

        virus_injections = FiberPhotometryVirusInjections(
            viral_vector_injections=[viral_vector_injection_green, viral_vector_injection_red]
        )

        indicator_green = Indicator(
            name="indicator_1",
            description="Green calcium indicator",
            label="GCaMP6f",
            viral_vector_injection=viral_vector_injection_green,
        )
        indicator_red = Indicator(
            name="indicator_2",
            description="Red calcium indicator",
            label="jRGECO1a",
            viral_vector_injection=viral_vector_injection_red,
        )

        indicators = FiberPhotometryIndicators(indicators=[indicator_green, indicator_red])

        optical_fiber_model = OpticalFiberModel(
            name="optical_fiber_model",
            manufacturer="Fiber Manufacturer",
            model_number="OF-123",
            description="Flat-tip fiber optic cannula for fiber photometry",
            numerical_aperture=0.48,
            core_diameter_in_um=400.0,
            ferrule_name="cFCF - ∅2.5mm Ceramic Ferrule",
            ferrule_model="SM-SC-CF-10-FM",
            ferrule_diameter_in_mm=2.5,
        )

        # The fiber tips are 0.2 mm above the injection sites.
        optical_fiber_1 = OpticalFiber(
            name="optical_fiber_1",
            description="Optical fiber for fiber photometry in the right VTA.",
            serial_number="OF-SN-123456",
            model=optical_fiber_model,
            fiber_insertion=StereotacticPosition(
                name="fiber_insertion",
                anatomical_target="Ventral Tegmental Area (VTA)",
                origin="bregma",
                orientation="RAS",
                x_in_mm=0.5,
                y_in_mm=-3.3,
                z_in_mm=-4.2,
            ),
        )
        optical_fiber_2 = OpticalFiber(
            name="optical_fiber_2",
            description="Optical fiber for fiber photometry in the left VTA.",
            serial_number="OF-SN-654321",
            model=optical_fiber_model,
            fiber_insertion=StereotacticPosition(
                name="fiber_insertion",
                anatomical_target="Ventral Tegmental Area (VTA)",
                origin="bregma",
                orientation="RAS",
                x_in_mm=-0.5,
                y_in_mm=-3.3,
                z_in_mm=-4.2,
            ),
        )

        excitation_source_model_465 = ExcitationSourceModel(
            name="excitation_source_model_465",
            manufacturer="LED Manufacturer",
            model_number="LED-465",
            description="465 nm LED for exciting green indicators.",
            source_type="LED",
            excitation_mode="one-photon",
            wavelength_range_in_nm=[455.0, 475.0],
        )
        excitation_source_model_405 = ExcitationSourceModel(
            name="excitation_source_model_405",
            manufacturer="LED Manufacturer",
            model_number="LED-405",
            description="405 nm LED for isosbestic excitation.",
            source_type="LED",
            excitation_mode="one-photon",
            wavelength_range_in_nm=[400.0, 410.0],
        )
        excitation_source_model_560 = ExcitationSourceModel(
            name="excitation_source_model_560",
            manufacturer="LED Manufacturer",
            model_number="LED-560",
            description="560 nm LED for exciting red indicators.",
            source_type="LED",
            excitation_mode="one-photon",
            wavelength_range_in_nm=[545.0, 575.0],
        )
        # Power is measured at the fiber tip; intensity is that power divided by the area of the 400 um core.
        excitation_source_465 = ExcitationSource(
            name="excitation_source_465",
            description="465 nm excitation of the green indicator (calcium-dependent signal).",
            serial_number="ES-SN-123456",
            model=excitation_source_model_465,
            power_in_W=30e-6,
            intensity_in_W_per_m2=240.0,
        )
        excitation_source_405 = ExcitationSource(
            name="excitation_source_405",
            description="405 nm excitation of the green indicator (isosbestic control).",
            serial_number="ES-SN-234567",
            model=excitation_source_model_405,
            power_in_W=15e-6,
            intensity_in_W_per_m2=120.0,
        )
        excitation_source_560 = ExcitationSource(
            name="excitation_source_560",
            description="560 nm excitation of the red indicator.",
            serial_number="ES-SN-654321",
            model=excitation_source_model_560,
            power_in_W=30e-6,
            intensity_in_W_per_m2=240.0,
        )

        photodetector_model = PhotodetectorModel(
            name="photodetector_model",
            manufacturer="Detector Manufacturer",
            model_number="PD-123",
            description="Femtowatt silicon photoreceiver for fiber photometry.",
            detector_type="Photodiode",
            wavelength_range_in_nm=[300.0, 1100.0],
        )
        photodetector_1 = Photodetector(
            name="photodetector_1",
            description="Photoreceiver for green emission.",
            serial_number="PD-SN-123456",
            model=photodetector_model,
            gain=1.0e10,
            gain_unit="V/W",
        )
        photodetector_2 = Photodetector(
            name="photodetector_2",
            description="Photoreceiver for red emission.",
            serial_number="PD-SN-654321",
            model=photodetector_model,
            gain=1.0e10,
            gain_unit="V/W",
        )

        dichroic_mirror_model_1 = DichroicMirrorModel(
            name="dichroic_mirror_model_1",
            manufacturer="Mirror Manufacturer",
            model_number="DM-123",
            description="Dichroic mirror model for the green indicator: reflects 405 and 465 nm, transmits emission.",
            cut_on_wavelength_in_nm=495.0,
            reflection_band_in_nm=[400.0, 488.0],
            transmission_band_in_nm=[502.0, 700.0],
            angle_of_incidence_in_degrees=45.0,
        )
        dichroic_mirror_model_2 = DichroicMirrorModel(
            name="dichroic_mirror_model_2",
            manufacturer="Mirror Manufacturer",
            model_number="DM-456",
            description="Dichroic mirror model for the red indicator: reflects 560 nm, transmits emission.",
            cut_on_wavelength_in_nm=580.0,
            reflection_band_in_nm=[530.0, 570.0],
            transmission_band_in_nm=[590.0, 700.0],
            angle_of_incidence_in_degrees=45.0,
        )
        dichroic_mirror_1 = DichroicMirror(
            name="dichroic_mirror_1",
            description="Dichroic mirror for green indicator",
            serial_number="DM-SN-123456",
            model=dichroic_mirror_model_1,
        )
        dichroic_mirror_2 = DichroicMirror(
            name="dichroic_mirror_2",
            description="Dichroic mirror for red indicator",
            serial_number="DM-SN-654321",
            model=dichroic_mirror_model_2,
        )

        band_optical_filter_model = BandOpticalFilterModel(
            name="band_optical_filter_model",
            manufacturer="Filter Manufacturer",
            model_number="BOF-123",
            description="Band optical filter model for green indicator",
            filter_type="Bandpass",
            center_wavelength_in_nm=525.0,
            bandwidth_in_nm=50.0,  # 525±25nm
        )
        band_optical_filter = BandOpticalFilter(
            name="band_optical_filter",
            description="Band optical filter for green indicator",
            serial_number="BOF-SN-123456",
            model=band_optical_filter_model,
        )
        edge_optical_filter_model = EdgeOpticalFilterModel(
            name="edge_optical_filter_model",
            manufacturer="Filter Manufacturer",
            model_number="EOF-123",
            description="Edge optical filter model for red indicator",
            filter_type="Longpass",
            cut_wavelength_in_nm=585.0,
            slope_in_percent_cut_wavelength=1.0,
            slope_starting_transmission_in_percent=10.0,
            slope_ending_transmission_in_percent=80.0,
        )
        edge_optical_filter = EdgeOpticalFilter(
            name="edge_optical_filter",
            description="Edge optical filter for red indicator",
            serial_number="EOF-SN-123456",
            model=edge_optical_filter_model,
        )

        # Each LED is driven by a sinusoid at its own carrier frequency so that a lock-in amplifier can separate
        # channels that share a photoreceiver. The commands are sampled at 10 kHz.
        command_rate = 10000.0
        command_times = np.arange(int(command_rate)) / command_rate
        commanded_voltage_series_465 = CommandedVoltageSeries(
            name="commanded_voltage_series_465",
            description="Commanded voltage of the 465 nm LED.",
            data=0.5 + 0.5 * np.sin(2 * np.pi * 211.0 * command_times),
            frequency=211.0,
            rate=command_rate,
            unit="volts",
        )
        commanded_voltage_series_405 = CommandedVoltageSeries(
            name="commanded_voltage_series_405",
            description="Commanded voltage of the 405 nm LED.",
            data=0.25 + 0.25 * np.sin(2 * np.pi * 531.0 * command_times),
            frequency=531.0,
            rate=command_rate,
            unit="volts",
        )
        commanded_voltage_series_560 = CommandedVoltageSeries(
            name="commanded_voltage_series_560",
            description="Commanded voltage of the 560 nm LED.",
            data=0.5 + 0.5 * np.sin(2 * np.pi * 330.0 * command_times),
            frequency=330.0,
            rate=command_rate,
            unit="volts",
        )

        fiber_photometry_table = FiberPhotometryTable(
            name="fiber_photometry_table",
            description="fiber photometry table",
        )
        fiber_photometry_table.add_row(
            location="VTA",
            excitation_wavelength_in_nm=465.0,
            emission_wavelength_in_nm=525.0,
            indicator=indicator_green,
            optical_fiber=optical_fiber_1,
            excitation_source=excitation_source_465,
            commanded_voltage_series=commanded_voltage_series_465,
            photodetector=photodetector_1,
            dichroic_mirror=dichroic_mirror_1,
            emission_filter=band_optical_filter,
        )
        # The isosbestic control shares the fiber, indicator and detection path of the green channel.
        fiber_photometry_table.add_row(
            location="VTA",
            excitation_wavelength_in_nm=405.0,
            emission_wavelength_in_nm=525.0,
            indicator=indicator_green,
            optical_fiber=optical_fiber_1,
            excitation_source=excitation_source_405,
            commanded_voltage_series=commanded_voltage_series_405,
            photodetector=photodetector_1,
            dichroic_mirror=dichroic_mirror_1,
            emission_filter=band_optical_filter,
        )
        fiber_photometry_table.add_row(
            location="VTA",
            excitation_wavelength_in_nm=560.0,
            emission_wavelength_in_nm=600.0,
            indicator=indicator_red,
            optical_fiber=optical_fiber_2,
            excitation_source=excitation_source_560,
            commanded_voltage_series=commanded_voltage_series_560,
            photodetector=photodetector_2,
            dichroic_mirror=dichroic_mirror_2,
            emission_filter=edge_optical_filter,
        )

        fiber_photometry_table_region = fiber_photometry_table.create_fiber_photometry_table_region(
            region=[0], description="source fibers"
        )

        fiber_photometry_lab_meta_data = FiberPhotometry(
            name="fiber_photometry",
            fiber_photometry_table=fiber_photometry_table,
            fiber_photometry_viruses=viruses,
            fiber_photometry_virus_injections=virus_injections,
            fiber_photometry_indicators=indicators,
        )

        rng = np.random.default_rng(seed=0)
        fiber_photometry_response_series = FiberPhotometryResponseSeries(
            name="fiber_photometry_response_series",
            description="Demodulated photoreceiver output of the 465 nm channel.",
            data=rng.standard_normal((100, 1)),
            unit="V",
            rate=30.0,
            fiber_photometry_table_region=fiber_photometry_table_region,
        )

        self.nwbfile.add_device_model(optical_fiber_model)
        self.nwbfile.add_device(optical_fiber_1)
        self.nwbfile.add_device(optical_fiber_2)
        self.nwbfile.add_device_model(excitation_source_model_465)
        self.nwbfile.add_device(excitation_source_465)
        self.nwbfile.add_device_model(excitation_source_model_405)
        self.nwbfile.add_device(excitation_source_405)
        self.nwbfile.add_device_model(excitation_source_model_560)
        self.nwbfile.add_device(excitation_source_560)
        self.nwbfile.add_device_model(photodetector_model)
        self.nwbfile.add_device(photodetector_1)
        self.nwbfile.add_device(photodetector_2)
        self.nwbfile.add_device_model(dichroic_mirror_model_1)
        self.nwbfile.add_device(dichroic_mirror_1)
        self.nwbfile.add_device_model(dichroic_mirror_model_2)
        self.nwbfile.add_device(dichroic_mirror_2)
        self.nwbfile.add_device_model(band_optical_filter_model)
        self.nwbfile.add_device(band_optical_filter)
        self.nwbfile.add_device_model(edge_optical_filter_model)
        self.nwbfile.add_device(edge_optical_filter)

        self.nwbfile.add_acquisition(commanded_voltage_series_465)
        self.nwbfile.add_acquisition(commanded_voltage_series_405)
        self.nwbfile.add_acquisition(commanded_voltage_series_560)
        self.nwbfile.add_lab_meta_data(fiber_photometry_lab_meta_data)
        self.nwbfile.add_acquisition(fiber_photometry_response_series)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(
                self.nwbfile.lab_meta_data["fiber_photometry"], read_nwbfile.lab_meta_data["fiber_photometry"]
            )
            self.assertContainerEqual(
                fiber_photometry_response_series, read_nwbfile.acquisition["fiber_photometry_response_series"]
            )
