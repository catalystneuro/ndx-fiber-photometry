from hdmf.common import DynamicTableRegion
from hdmf.utils import docval, get_docval, popargs
from pynwb import TimeSeries, get_class, register_class, register_map
from pynwb.io.base import TimeSeriesMap

FiberPhotometryTable = get_class("FiberPhotometryTable", "ndx-fiber-photometry")


@docval(
    {"name": "region", "type": list, "doc": "the indices of the FiberPhotometryTable"},
    {"name": "description", "type": str, "doc": "a brief description of what these table entries represent"},
)
def create_fiber_photometry_table_region(self, **kwargs):
    region, description = popargs("region", "description", kwargs)
    name = "fiber_photometry_table_region"
    return super(FiberPhotometryTable, self).create_region(name=name, region=region, description=description)


FiberPhotometryTable.create_fiber_photometry_table_region = create_fiber_photometry_table_region


@register_class("FiberPhotometryResponseSeries", "ndx-fiber-photometry")
class FiberPhotometryResponseSeries(TimeSeries):
    """Extends TimeSeries to hold Fiber Photometry data."""

    __nwbfields__ = (
        {"name": "fiber_photometry_table_region", "child": True},
        "processing_parameters",
        "processing_software",
        "processing_software_version",
    )

    @docval(
        *get_docval(TimeSeries.__init__),
        {
            "name": "fiber_photometry_table_region",
            "type": DynamicTableRegion,
            "doc": (
                "References the row(s) of FiberPhotometryTable that the data come from, one row per column of " "data."
            ),
            "default": None,
        },
        {
            "name": "processing_parameters",
            "type": str,
            "doc": (
                "JSON-encoded parameters of the processing that produced the data, in the vocabulary of "
                "processing_software. Requires processing_software and processing_software_version."
            ),
            "default": None,
        },
        {
            "name": "processing_software",
            "type": str,
            "doc": "Name of the software that produced the data.",
            "default": None,
        },
        {
            "name": "processing_software_version",
            "type": str,
            "doc": "Version of the software that produced the data.",
            "default": None,
        },
    )
    def __init__(self, **kwargs):
        (
            fiber_photometry_table_region,
            processing_parameters,
            processing_software,
            processing_software_version,
        ) = popargs(
            "fiber_photometry_table_region",
            "processing_parameters",
            "processing_software",
            "processing_software_version",
            kwargs,
        )
        processing_fields = (processing_parameters, processing_software, processing_software_version)
        if any(field is not None for field in processing_fields) and any(field is None for field in processing_fields):
            raise ValueError(
                "processing_parameters, processing_software and processing_software_version must be given together."
            )
        super().__init__(**kwargs)
        self.fiber_photometry_table_region = fiber_photometry_table_region
        self.processing_parameters = processing_parameters
        self.processing_software = processing_software
        self.processing_software_version = processing_software_version


@register_map(FiberPhotometryResponseSeries)
class FiberPhotometryResponseSeriesMap(TimeSeriesMap):
    def __init__(self, spec):
        super().__init__(spec)
        processing_parameters_spec = self.spec.get_dataset("processing_parameters")
        self.map_spec("processing_software", processing_parameters_spec.get_attribute("processing_software"))
        self.map_spec(
            "processing_software_version", processing_parameters_spec.get_attribute("processing_software_version")
        )
