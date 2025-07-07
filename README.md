# ndx-fiber-photometry Extension for NWB

This is an NWB extension for storing fiber photometry recordings and associated metadata.
It replaces the deprecated [ndx-photometry](https://github.com/catalystneuro/ndx-photometry) extension.

This extension consists of 11 new neurodata types:
- `Indicator` extends `Device` to hold metadata on the fluorescent indicator (ex. label=GCaMP6).
- `OpticalFiber` extends `Device` to hold metadata on the optical fiber (ex. numerical_aperture=0.39).
- `ExcitationSource` extends `Device` to hold metadata on the excitation source (ex. excitation_wavelength_in_nm=470.0).
- `Photodetector` extends `Device` to hold metadata on the photodetector (ex. detected_wavelength_in_nm=520.0).
- `DichroicMirror` extends `Device` to hold metadata on the dichroic mirror (ex. cut_on_wavelength_in_nm=470.0).
- `BandOpticalFilter` extends `Device` to hold metadata on any bandpass or bandstop optical filters (ex. center_wavelength_in_nm=505.0).
- `EdgeOpticalFilter` extends `Device` to hold metadata on any edge optical filters (ex. cut_wavelength_in_nm=585.0).
- `FiberPhotometryResponseSeries` extends `TimeSeries` to hold the recorded fiber photometry responses.
- `CommandedVoltageSeries` extends `TimeSeries` to hold the commanded voltage values for a single fiber photometry trace.
- `FiberPhotometryTable` extends `DynamicTable` to hold information on the fiber photometry setup.
    Each row of the table reference a combination of the devices and a commanded voltage series that correspond to a single fiber photometry trace.
- `FiberPhotometry` extends `LabMetaData` to hold the `FiberPhotometryTable`.

## Installation

To install the latest stable release through PyPI,
```bash
pip install ndx-fiber-photometry
```

## Usage

```python
import datetime
import numpy as np
from pynwb import NWBFile, NWBHDF5IO
from ndx_ophys_devices import (
    ViralVector,
    ViralVectorInjection,
    Indicator,
    OpticalFiberModel,
    FiberInsertion,
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

nwbfile = NWBFile(
    session_description='session_description',
    identifier='identifier',
    session_start_time=datetime.datetime.now(datetime.timezone.utc)
)

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
    construct_name="AAV-CaMKII-Tdtomato",
    manufacturer="Vector Manufacturer",
    titer_in_vg_per_ml=1.0e12,
)
viruses = FiberPhotometryViruses(viral_vectors=[viral_vector_green, viral_vector_red])

viral_vector_injection_green = ViralVectorInjection(
    name="viral_vector_injection_green",
    description="Viral vector injection for fiber photometry.",
    location="Ventral Tegmental Area (VTA)",
    hemisphere="right",
    reference="Bregma at the cortical surface",
    ap_in_mm=3.0,
    ml_in_mm=2.0,
    dv_in_mm=1.0,
    pitch_in_deg=0.0,
    yaw_in_deg=0.0,
    roll_in_deg=0.0,
    stereotactic_rotation_in_deg=0.0,
    stereotactic_tilt_in_deg=0.0,
    volume_in_uL=0.45,
    injection_date="1970-01-01T00:00:00+00:00",
    viral_vector=viral_vector_green,
)

viral_vector_injection_red = ViralVectorInjection(
    name="viral_vector_injection_red",
    description="Viral vector injection for fiber photometry.",
    location="Ventral Tegmental Area (VTA)",
    hemisphere="right",
    reference="Bregma at the cortical surface",
    ap_in_mm=3.0,
    ml_in_mm=2.0,
    dv_in_mm=1.0,
    pitch_in_deg=0.0,
    yaw_in_deg=0.0,
    roll_in_deg=0.0,
    stereotactic_rotation_in_deg=0.0,
    stereotactic_tilt_in_deg=0.0,
    volume_in_uL=0.45,
    injection_date="1970-01-01T00:00:00+00:00",
    viral_vector=viral_vector_red,
)

virus_injections = FiberPhotometryVirusInjections(
    viral_vector_injections=[viral_vector_injection_green, viral_vector_injection_red]
)


indicator_green = Indicator(
    name="indicator_1",
    description="Green indicator",
    label="GCamp6f",
    viral_vector_injection=viral_vector_injection_green,
)
indicator_red = Indicator(
    name="indicator_2",
    description="Red indicator",
    label="Tdtomato",
    viral_vector_injection=viral_vector_injection_red,
)

indicators = FiberPhotometryIndicators(indicators=[indicator_green, indicator_red])

optical_fiber_model = OpticalFiberModel(
    name="optical_fiber_model",
    manufacturer="Fiber Manufacturer",
    model_number="OF-123",
    description="Optical fiber model for optogenetics",
    numerical_aperture=0.2,
    core_diameter_in_um=400.0,
    active_length_in_mm=2.0,
    ferrule_name="cFCF - ∅2.5mm Ceramic Ferrule",
    ferrule_model="SM-SC-CF-10-FM",
    ferrule_diameter_in_mm=2.5,
)

fiber_insertion_1 = FiberInsertion(
    name="fiber_insertion",
    depth_in_mm=3.5,
    insertion_position_ap_in_mm=3.0,
    insertion_position_ml_in_mm=2.0,
    insertion_position_dv_in_mm=1.0,
    position_reference="bregma",
    hemisphere="right",
    insertion_angle_pitch_in_deg=10.0,
)

fiber_insertion_2 = FiberInsertion(
    name="fiber_insertion",
    depth_in_mm=3.5,
    insertion_position_ap_in_mm=3.0,
    insertion_position_ml_in_mm=-2.0,
    insertion_position_dv_in_mm=1.0,
    position_reference="bregma",
    hemisphere="left",
    insertion_angle_pitch_in_deg=10.0,
)

optical_fiber_1 = OpticalFiber(
    name="optical_fiber_1",
    description="Optical fiber for fiber photometry.",
    serial_number="OF-SN-123456",
    model=optical_fiber_model,
    fiber_insertion=fiber_insertion_1,
)
optical_fiber_2 = OpticalFiber(
    name="optical_fiber_2",
    description="Optical fiber for fiber photometry.",
    serial_number="OF-SN-654321",
    model=optical_fiber_model,
    fiber_insertion=fiber_insertion_2,
)

excitation_source_model = ExcitationSourceModel(
    name="excitation_source_model",
    manufacturer="Laser Manufacturer",
    model_number="ES-123",
    description="Excitation source model for fiber photometry.",
    source_type="laser",
    excitation_mode="one-photon",
    wavelength_range_in_nm=[400.0, 800.0],
)
excitation_source_1 = ExcitationSource(
    name="excitation_source_1",
    description="Excitation source for green indicator",
    serial_number="ES-SN-123456",
    model=excitation_source_model,
    power_in_W=0.7,
    intensity_in_W_per_m2=0.005,
    exposure_time_in_s=2.51e-13,
)
excitation_source_2 = ExcitationSource(
    name="excitation_source_2",
    description="Excitation source for red indicator",
    serial_number="ES-SN-654321",
    model=excitation_source_model,
    power_in_W=0.7,
    intensity_in_W_per_m2=0.005,
    exposure_time_in_s=2.51e-13,
)

photodetector_model = PhotodetectorModel(
    name="photodetector_model",
    manufacturer="Detector Manufacturer",
    model_number="PD-123",
    description="Photodetector model for fiber photometry.",
    detector_type="PMT",
    wavelength_range_in_nm=[400.0, 800.0],
    gain=100.0,
    gain_unit="A/W",
)
photodetector_1 = Photodetector(
    name="photodetector_1",
    description="Photodetector for green emission.",
    serial_number="PD-SN-123456",
    model=photodetector_model,
)
photodetector_2 = Photodetector(
    name="photodetector_2",
    description="Photodetector for red emission.",
    serial_number="PD-SN-654321",
    model=photodetector_model,
)

dichroic_mirror_model_1 = DichroicMirrorModel(
    name="dichroic_mirror_model_1",
    manufacturer="Mirror Manufacturer",
    model_number="DM-123",
    description="Dichroic mirror model for green indicator.",
    cut_on_wavelength_in_nm=470.0,
    cut_off_wavelength_in_nm=500.0,
    reflection_band_in_nm=[490.0, 520.0],
    transmission_band_in_nm=[460.0, 480.0],
    angle_of_incidence_in_degrees=45.0,
)
dichroic_mirror_model_2 = DichroicMirrorModel(
    name="dichroic_mirror_model_2",
    manufacturer="Mirror Manufacturer",
    model_number="DM-456",
    description="Dichroic mirror model for red indicator.",
    cut_on_wavelength_in_nm=525.0,
    cut_off_wavelength_in_nm=585.0,
    reflection_band_in_nm=[575.0, 595.0],
    transmission_band_in_nm=[515.0, 535.0],
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
    center_wavelength_in_nm=505.0,
    bandwidth_in_nm=30.0,  # 505±15nm
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

commanded_voltage_series_1 = CommandedVoltageSeries(
    name="commanded_voltage_series_1", data=[1.0, 2.0, 3.0], frequency=30.0, rate=30.0, unit="volts"
)
commanded_voltage_series_2 = CommandedVoltageSeries(
    name="commanded_voltage_series_2",
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
    indicator=indicator_green,
    optical_fiber=optical_fiber_1,
    excitation_source=excitation_source_1,
    commanded_voltage_series=commanded_voltage_series_1,
    photodetector=photodetector_1,
    dichroic_mirror=dichroic_mirror_1,
    emission_filter=band_optical_filter,
)
fiber_photometry_table.add_row(
    location="VTA",
    indicator=indicator_red,
    optical_fiber=optical_fiber_2,
    excitation_source=excitation_source_2,
    commanded_voltage_series=commanded_voltage_series_2,
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

fiber_photometry_response_series = FiberPhotometryResponseSeries(
    name="fiber_photometry_response_series",
    description="my roi response series",
    data=np.random.randn(100, 1),
    unit="n.a.",
    rate=30.0,
    fiber_photometry_table_region=fiber_photometry_table_region,
)

nwbfile.add_device(optical_fiber_model)
nwbfile.add_device(optical_fiber_1)
nwbfile.add_device(optical_fiber_2)
nwbfile.add_device(excitation_source_model)
nwbfile.add_device(excitation_source_1)
nwbfile.add_device(excitation_source_2)
nwbfile.add_device(photodetector_model)
nwbfile.add_device(photodetector_1)
nwbfile.add_device(photodetector_2)
nwbfile.add_device(dichroic_mirror_model_1)
nwbfile.add_device(dichroic_mirror_1)
nwbfile.add_device(dichroic_mirror_model_2)
nwbfile.add_device(dichroic_mirror_2)
nwbfile.add_device(band_optical_filter_model)
nwbfile.add_device(band_optical_filter)
nwbfile.add_device(edge_optical_filter_model)
nwbfile.add_device(edge_optical_filter)

nwbfile.add_acquisition(commanded_voltage_series_1)
nwbfile.add_acquisition(commanded_voltage_series_2)
nwbfile.add_lab_meta_data(fiber_photometry_lab_meta_data)
nwbfile.add_acquisition(fiber_photometry_response_series)
```

## Extension Diagram
```mermaid
%%{
    init: {
        'theme': 'base',
        'themeVariables': {
            'primaryColor': '#ffffff',
            "primaryBorderColor': '#144E73',
            'lineColor': '#D96F32'
        }
    }
}%%


classDiagram
    direction BT

    class TimeSeries {
        attributes
        --------------------------------------
        name : str
        description : str
        rate : float
        starting_time: float
        timestamps : array-like
        unit : str
        offset : float, optional
        conversion : float, optional
    }

    class DynamicTable{
        attributes
        --------------------------------------
        name : str
        description : str
    }

    class Device{
        attributes
        --------------------------------------
        name : str
        description : str
        manufacturer : str
    }

    class FiberPhotometryResponseSeries {
        datasets
        --------------------------------------
        data [ntime, nfibers] : array-like

        links
        --------------------------------------
        fiber_photometry_table_region : DynamicTableRegion
    }

    class CommandedVoltageSeries {
        datasets
        --------------------------------------
        data [ntime] : array-like

        attributes
        --------------------------------------
        frequency : float
    }

    class FiberPhotometryTable {
        VectorData Columns
        --------------------------------------
        location : str
        coordinates [x, y, z] : [float, float, float]
        notes : str
        commanded_voltage_series : CommandedVoltageSeries
        optical_fiber : OpticalFiber
        photodetector : Photodetector
        indicator : Indicator
        excitation_source : ExcitationSource
        dichroic_mirror : DichroicMirror
        emission_filter : BandOpticalFilter | EdgeOpticalFilter
        excitation_filter : BandOpticalFilter | EdgeOpticalFilter
    }

    class OpticalFiber{
        attributes
        --------------------------------------
        model : str
        numerical_aperture : float
        core_diameter_in_um : float
    }

    class ExcitationSource{
        attributes
        --------------------------------------
        model : str
        illumination_type : str
        excitation_wavelength_in_nm : float
    }

    class Photodetector{
        attributes
        --------------------------------------
        model : str
        detector_type : str
        detected_wavelength_in_nm : float
        gain : float
    }

    class BandOpticalFilter{
        attributes
        --------------------------------------
        model : str
        center_wavelength_in_nm : float
        bandwidth_in_nm : float
        filter_type : str
    }

    class EdgeOpticalFilter{
        attributes
        --------------------------------------
        model : str
        cut_wavelength_in_nm : float
        slope_in_percent_cut_wavelength : float
        slope_starting_transmission_in_percent : float
        slope_ending_transmission_in_percent : float
        filter_type : str
    }

    class DichroicMirror{
        attributes
        --------------------------------------
        model : str
        cut_on_wavelength_in_nm : float
        cut_off_wavelength_in_nm : float
        reflection_band_in_nm : float
        angle_of_incidence_in_degrees : float
    }

    class Indicator{
        attributes
        --------------------------------------
        label : str, optional
        injection_location : str
        injection_coordinates_in_mm [AP, ML, DV] : [float, float, float]
    }

    TimeSeries <|-- FiberPhotometryResponseSeries : extends
    TimeSeries <|-- CommandedVoltageSeries : extends
    DynamicTable <|-- FiberPhotometryTable : extends
    Device <|-- OpticalFiber : extends
    Device <|-- ExcitationSource : extends
    Device <|-- Photodetector : extends
    Device <|-- BandOpticalFilter : extends
    Device <|-- EdgeOpticalFilter : extends
    Device <|-- DichroicMirror : extends
    Device <|-- Indicator : extends

    CommandedVoltageSeries o-- FiberPhotometryTable : aggregates
    OpticalFiber o-- FiberPhotometryTable : aggregates
    ExcitationSource o-- FiberPhotometryTable : aggregates
    Photodetector o-- FiberPhotometryTable : aggregates
    BandOpticalFilter o-- FiberPhotometryTable : aggregates
    EdgeOpticalFilter o-- FiberPhotometryTable : aggregates
    DichroicMirror o-- FiberPhotometryTable : aggregates
    Indicator o-- FiberPhotometryTable : aggregates

    FiberPhotometryTable -- FiberPhotometryResponseSeries : links

    style Device stroke:blue,stroke-width:5px
    style TimeSeries stroke:blue,stroke-width:5px
    style DynamicTable stroke:blue,stroke-width:5px
    style FiberPhotometryResponseSeries stroke:green,stroke-width:5px
    style CommandedVoltageSeries stroke:green,stroke-width:5px
    style FiberPhotometryTable stroke:green,stroke-width:5px
    style OpticalFiber stroke:green,stroke-width:5px
    style ExcitationSource stroke:green,stroke-width:5px
    style Photodetector stroke:green,stroke-width:5px
    style BandOpticalFilter stroke:green,stroke-width:5px
    style EdgeOpticalFilter stroke:green,stroke-width:5px
    style DichroicMirror stroke:green,stroke-width:5px
    style Indicator stroke:green,stroke-width:5px
```
---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
