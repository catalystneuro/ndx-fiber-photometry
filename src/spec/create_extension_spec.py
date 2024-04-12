# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBDatasetSpec, NWBRefSpec, NWBAttributeSpec

# TODO: import other spec classes as needed
# from pynwb.spec import NWBLinkSpec, NWBDtypeSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-fiber-photometry""",
        version="""0.1.0""",
        doc="""This is an NWB extension for storing fiber photometry recordings and associated metadata.""",
        author=[
            "Alessandra Trapani",
            "Luiz Tauffer",
            "Paul Adkisson",
            "Szonja Weigl",
        ],
        contact=[
            "alessandra.trapani@catlystneuro.com",
            "luiz.tauffer@catlystneuro.com",
            "paul.adkisson@catlystneuro.com",
            "szonja.weigl@catlystneuro.com",
        ],
    )
    ns_builder.include_namespace("core")
    ns_builder.include_type("TimeSeries", namespace="core")
    ns_builder.include_type("Device", namespace="core")
    ns_builder.include_type("DynamicTable", namespace="hdmf-common")
    ns_builder.include_type("DynamicTableRegion", namespace="hdmf-common")
    ns_builder.include_type("VectorData", namespace="hdmf-common")

    # Define new data types
    # see https://pynwb.readthedocs.io/en/stable/tutorials/general/extensions.html
    # for more information
    optical_fiber = NWBGroupSpec(
        neurodata_type_def="OpticalFiber",
        neurodata_type_inc="Device",
        name="fiber",
        doc="Extends Device to hold metadata on the Optica Fiber.",
        attributes=[
            NWBAttributeSpec(
                name="model",
                doc="Model of optical fiber.",
                dtype="text",
                required=False,
            ),
            NWBAttributeSpec(
                name="numerical_aperture",
                doc="Numerical aperture, e.g., 0.39 NA.",
                dtype="float",
                required=False,
            ),
        ],
    )

    excitation_source = NWBGroupSpec(
        neurodata_type_def="ExcitationSource",
        neurodata_type_inc="Device",
        name="excitation_source",
        doc="Extends Device to hold metadata on the Excitation Source.",
        attributes=[
            NWBAttributeSpec(
                name="model",
                doc="Model of excitation source device.",
                dtype="text",
                required=False,
            ),
            NWBAttributeSpec(
                name="illumination_type",
                doc="Illumination type, e.g., laser ot LED.",
                dtype="text",
            ),
            NWBAttributeSpec(
                name="excitation_wavelength_in_nm",
                doc="Excitation wavelength of the stimulation light (nanometers).",
                dtype="float",
            ),
        ],
    )

    photodetector = NWBGroupSpec(
        neurodata_type_def="Photodetector",
        neurodata_type_inc="Device",
        name="excitation_source",
        doc="Extends Device to hold metadata on the Excitation Source.",
        attributes=[
            NWBAttributeSpec(
                name="model",
                doc="Model of excitation source device.",
                dtype="text",
                required=False,
            ),
            NWBAttributeSpec(
                name="detector_type",
                doc="Technology used to detect the light, e.g., PMT or photodiode.",
                dtype="text",
            ),
            NWBAttributeSpec(
                name="detected_wavelength_in_nm",
                doc="Wavelength detected by photodetector.",
                dtype="float",
            ),
            NWBAttributeSpec(
                name="gain",
                doc="Gain on the photodetector.",
                dtype="float",
            ),
        ],
    )

    dichroic_mirror = NWBGroupSpec(
        neurodata_type_def="DichroicMirror",
        neurodata_type_inc="Device",
        doc="Extends Device to hold a Dichroic Mirror.",
        attributes=[
            NWBAttributeSpec(
                name="cut_on_wavelength_in_nm",
                doc="Wavelength at which the mirror starts to transmit light more than reflect.",
                dtype="float",
            ),
            NWBAttributeSpec(
                name="cut_off_wavelength_in_nm",
                doc="Wavelength at which transmission shifts back to reflection, for mirrors with complex transmission spectra.",
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="reflection_bandwidth_in_nm",
                doc="The range of wavelengths that are primarily reflected. The start and end wavelengths needs to be specified.",
                dtype="float",
                required=False,
                shape=(2,),
            ),
            NWBAttributeSpec(
                name="transmission_bandwidth_in_nm",
                doc="The range of wavelengths that are primarily transmitted. The start and end wavelengths needs to be specified.",
                dtype="float",
                required=False,
                shape=(2,),
            ),
            NWBAttributeSpec(
                name="angle_of_incidence_in_degrees",
                doc="Intended angle at which light strikes the mirror.",
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="model",
                doc="Model of the dichroic mirror.",
                dtype="text",
                required=False,
            ),
        ],
    )

    optical_filter = NWBGroupSpec(
        neurodata_type_def="OpticalFilter",
        neurodata_type_inc="Device",
        doc="Extends Device to hold a Optical Filter.",
        attributes=[
            NWBAttributeSpec(
                name="peak_wavelength_in_nm",
                doc="Wavelength that the filter is designed to pass or reflect.",
                dtype="float",
            ),
            NWBAttributeSpec(
                name="bandwidth_in_nm",
                doc="Width of the wavelength range that the filter allows to pass through or blocks.",
                dtype="float",
            ),
            NWBAttributeSpec(
                name="filter_type",
                doc="Type of filter (e.g., 'Excitation', 'Emission', 'Bandpass', 'Longpass', 'Shortpass').",
                dtype="text",
            ),
            NWBAttributeSpec(
                name="model",
                doc="Model of the optical filter.",
                dtype="text",
                required=False,
            ),
        ],
    )

    fiber_photometry_table = NWBGroupSpec(
        neurodata_type_def="FiberPhotometryTable",
        neurodata_type_inc="DynamicTable",
        name="fiber_photometry_table",
        doc="Extends DynamicTable to hold metadata on the Fiber Photometry system.",
        datasets=[
            NWBDatasetSpec(
                name="location",
                doc="Location of fiber.",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="coordinates",
                doc="Fiber placement in stereotactic coordinates (AP, ML, DV) mm relative to Bregma.",
                dtype="float",
                shape=(None, 3),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="indicator",
                doc="Indicator notation.",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="notes",
                doc="Description of system.",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="fiber",
                doc="Link to the fiber device.",
                dtype=NWBRefSpec(target_type="Device", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="excitation_source",
                doc="Link to the excitation source device.",
                dtype=NWBRefSpec(target_type="Device", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="photodetector",
                doc="Link to the photodetector device.",
                dtype=NWBRefSpec(target_type="Device", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="dichroic_mirror",
                doc="Link to the dichroic mirror device.",
                dtype=NWBRefSpec(target_type="Device", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
        ],
    )

    fiberphotometryresponse_series = NWBGroupSpec(
        neurodata_type_def="FiberPhotometryResponseSeries",
        neurodata_type_inc="TimeSeries",
        doc="Extends TimeSeries to hold Fiber Photometry data.",
        datasets=[
            NWBDatasetSpec(
                name="data",
                doc="The data values. May be 1D or 2D. The first dimension must be time. The optional second dimension referes to the fiber that record the series.",
                shape=(None, None),
            ),
            NWBDatasetSpec(
                name="fiber_photometry_table",
                doc="References row(s) of FiberPhotometryTable.",
                neurodata_type_inc="DynamicTableRegion",
                quantity="?",
            ),
        ],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [
        optical_fiber,
        excitation_source,
        photodetector,
        dichroic_mirror,
        optical_filter,
        fiber_photometry_table,
        fiberphotometryresponse_series,
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
