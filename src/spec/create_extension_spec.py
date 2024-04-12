# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec

# TODO: import other spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


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
    
    # TODO: if your extension builds on another extension, include the namespace
    # of the other extension below
    # ns_builder.include_namespace("ndx-other-extension")

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/stable/tutorials/general/extensions.html
    # for more information
    tetrode_series = NWBGroupSpec(
        neurodata_type_def="TetrodeSeries",
        neurodata_type_inc="ElectricalSeries",
        doc="An extension of ElectricalSeries to include the tetrode ID for each time series.",
        attributes=[NWBAttributeSpec(name="trode_id", doc="The tetrode ID.", dtype="int32")],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [tetrode_series]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
