# -*- coding: utf-8 -*-
import os.path
from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBDatasetSpec, NWBRefSpec, NWBAttributeSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-fiber-photometry""",
        version="""0.2.3""",
        doc="""This is an NWB extension for storing fiber photometry recordings and associated metadata.""",
        author=[
            "Alessandra Trapani",
            "Luiz Tauffer",
            "Paul Adkisson-Floro",
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
    ns_builder.include_type("LabMetaData", namespace="core")

    ns_builder.include_namespace("hdmf-common")
    ns_builder.include_type("DynamicTable", namespace="hdmf-common")
    ns_builder.include_type("DynamicTableRegion", namespace="hdmf-common")
    ns_builder.include_type("VectorData", namespace="hdmf-common")

    ns_builder.include_namespace("ndx-ophys-devices")
    ns_builder.include_type("Indicator", namespace="ndx-ophys-devices")
    ns_builder.include_type("ViralVector", namespace="ndx-ophys-devices")
    ns_builder.include_type("ViralVectorInjection", namespace="ndx-ophys-devices")
    ns_builder.include_type("OpticalFiber", namespace="ndx-ophys-devices")
    ns_builder.include_type("ExcitationSource", namespace="ndx-ophys-devices")
    ns_builder.include_type("Photodetector", namespace="ndx-ophys-devices")
    ns_builder.include_type("DichroicMirror", namespace="ndx-ophys-devices")
    ns_builder.include_type("BandOpticalFilter", namespace="ndx-ophys-devices")
    ns_builder.include_type("EdgeOpticalFilter", namespace="ndx-ophys-devices")
    ns_builder.include_type("OpticalFilter", namespace="ndx-ophys-devices")

    # Define new data types
    # see https://pynwb.readthedocs.io/en/stable/tutorials/general/extensions.html
    # for more information
    fiber_photometry_table = NWBGroupSpec(
        neurodata_type_def="FiberPhotometryTable",
        neurodata_type_inc="DynamicTable",
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
                doc="Relative coordinates of fiber in multi-fiber array. If single fiber, use None.",
                dtype="float",
                shape=(None, 3),
                neurodata_type_inc="VectorData",
                quantity="?",
                attributes=[NWBAttributeSpec(name="unit", doc="coordinates unit", value="millimeters", dtype="text")],
            ),
            NWBDatasetSpec(
                name="excitation_wavelength_in_nm",
                doc="Wavelength of excitation light in nanometers.",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="emission_wavelength_in_nm",
                doc="Wavelength of emission light in nanometers.",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="indicator",
                doc="Link to the indicator object.",
                dtype=NWBRefSpec(target_type="Indicator", reftype="object"),
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
                name="optical_fiber",
                doc="Link to the optical fiber device.",
                dtype=NWBRefSpec(target_type="OpticalFiber", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="excitation_source",
                doc="Link to the excitation source device.",
                dtype=NWBRefSpec(target_type="ExcitationSource", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="commanded_voltage_series",
                doc="Link to the commanded voltage series.",
                dtype=NWBRefSpec(target_type="CommandedVoltageSeries", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="photodetector",
                doc="Link to the photodetector device.",
                dtype=NWBRefSpec(target_type="Photodetector", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="dichroic_mirror",
                doc="Link to the dichroic mirror device.",
                dtype=NWBRefSpec(target_type="DichroicMirror", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="emission_filter",
                doc="Link to the emission filter device.",
                dtype=NWBRefSpec(target_type="OpticalFilter", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="excitation_filter",
                doc="Link to the excitation filter device.",
                dtype=NWBRefSpec(target_type="OpticalFilter", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
        ],
    )

    fiber_photometry_indicators = NWBGroupSpec(
        name="fiber_photometry_indicators",  # use fixed name, for use in FiberPhotometry
        neurodata_type_def="FiberPhotometryIndicators",
        neurodata_type_inc="NWBContainer",
        doc="Group containing one or more Indicator objects, to be used within an FiberPhotometry object.",
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="Indicator",
                doc="Indicator object(s).",
                quantity="+",
            ),
        ],
    )
    fiber_photometry_viruses = NWBGroupSpec(
        name="fiber_photometry_viruses",  # use fixed name, for use in FiberPhotometry
        neurodata_type_def="FiberPhotometryViruses",
        neurodata_type_inc="NWBContainer",
        doc="Group containing one or more ViralVector objects, to be used within an FiberPhotometry object.",
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="ViralVector",
                doc="ViralVector object(s).",
                quantity="+",
            ),
        ],
    )
    fiber_photometry_virus_injections = NWBGroupSpec(
        name="fiber_photometry_virus_injections",  # use fixed name, for use in FiberPhotometry
        neurodata_type_def="FiberPhotometryVirusInjections",
        neurodata_type_inc="NWBContainer",
        doc="Group containing one or more ViralVectorInjection objects, to be used within an FiberPhotometry object.",
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="ViralVectorInjection",
                doc="ViralVectorInjection object(s).",
                quantity="+",
            ),
        ],
    )

    fiber_photometry_lab_meta_data = NWBGroupSpec(
        neurodata_type_def="FiberPhotometry",
        neurodata_type_inc="LabMetaData",
        doc="Extends LabMetaData to hold all Fiber Photometry metadata.",
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="FiberPhotometryTable",
                doc="The table containing the metadata on the Fiber Photometry system.",
            ),
            NWBGroupSpec(
                neurodata_type_inc="FiberPhotometryIndicators",
                doc="The group containing the Indicator objects.",
            ),
            NWBGroupSpec(
                neurodata_type_inc="FiberPhotometryViruses",
                doc="The group containing the ViralVector objects.",
                quantity="?",
            ),
            NWBGroupSpec(
                neurodata_type_inc="FiberPhotometryVirusInjections",
                doc="The group containing the ViralVectorInjection objects.",
                quantity="?",
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
                doc="The data values. May be 1D or 2D. The first dimension must be time."
                "The optional second dimension refers to the fiber that record the series.",
                shape=((None,), (None, None)),
            ),
            NWBDatasetSpec(
                name="fiber_photometry_table_region",
                doc="References row(s) of FiberPhotometryTable.",
                neurodata_type_inc="DynamicTableRegion",
                quantity="?",
            ),
        ],
    )

    commandedvoltage_series = NWBGroupSpec(
        neurodata_type_def="CommandedVoltageSeries",
        neurodata_type_inc="TimeSeries",
        doc="Extends TimeSeries to hold a Commanded Voltage",
        datasets=[
            NWBDatasetSpec(
                name="data",
                doc="Voltages (length number timesteps) in unit volts.",
                dtype="float",
                shape=(None,),
            ),
            NWBDatasetSpec(
                name="frequency",
                doc="Voltage frequency in unit hertz.",
                dtype="float",
                attributes=[NWBAttributeSpec(name="unit", doc="frequency unit", value="hertz", dtype="text")],
                quantity="?",
            ),
        ],
    )

    new_data_types = [
        fiber_photometry_viruses,
        fiber_photometry_virus_injections,
        fiber_photometry_indicators,
        fiber_photometry_table,
        fiber_photometry_lab_meta_data,
        fiberphotometryresponse_series,
        commandedvoltage_series,
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
