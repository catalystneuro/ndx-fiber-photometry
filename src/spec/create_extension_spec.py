# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBDatasetSpec, NWBRefSpec, NWBAttributeSpec
from ndx_ophys_devices import (
    Indicator,
    OpticalFiber,
    ExcitationSource,
    Photodetector,
    DichroicMirror,
    BandOpticalFilter,
    EdgeOpticalFilter,
)


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-fiber-photometry""",
        version="""0.1.1""",
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
    ns_builder.include_namespace("ndx-ophys-devices")
    ns_builder.include_type("TimeSeries", namespace="core")
    ns_builder.include_type("Device", namespace="core")
    ns_builder.include_type("LabMetaData", namespace="core")
    ns_builder.include_type("DynamicTable", namespace="hdmf-common")
    ns_builder.include_type("DynamicTableRegion", namespace="hdmf-common")
    ns_builder.include_type("VectorData", namespace="hdmf-common")

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
                doc="Fiber placement in stereotactic coordinates (AP, ML, DV) mm relative to Bregma.",
                dtype="float",
                shape=(None, 3),
                neurodata_type_inc="VectorData",
                quantity="?",
                attributes=[NWBAttributeSpec(name="unit", doc="coordinates unit", value="millimeters", dtype="text")],
            ),
            NWBDatasetSpec(
                name="indicator",
                doc="Link to the indicator object.",
                dtype=NWBRefSpec(target_type="Device", reftype="object"),
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
                name="commanded_voltage_series",
                doc="Link to the commanded voltage series.",
                dtype=NWBRefSpec(target_type="TimeSeries", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
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
            NWBDatasetSpec(
                name="emission_filter",
                doc="Link to the emission filter device.",
                dtype=NWBRefSpec(target_type="Device", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="excitation_filter",
                doc="Link to the excitation filter device.",
                dtype=NWBRefSpec(target_type="Device", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
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
