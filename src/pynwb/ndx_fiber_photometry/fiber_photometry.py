from hdmf.common import DynamicTableRegion
from hdmf.utils import docval, get_docval, popargs
from pynwb import get_class, register_class

FiberPhotometryTable = get_class("FiberPhotometryTable", "ndx-fiber-photometry")
FiberPhotometryResponseSeries = get_class("FiberPhotometryResponseSeries", "ndx-fiber-photometry")


@docval(
    {"name": "region", "type": list, "doc": "the indices of the FiberPhotometryTable"},
    {"name": "description", "type": str, "doc": "a brief description of what these table entries represent"},
)
def create_fiber_photometry_table_region(self, **kwargs):
    region, description = popargs("region", "description", kwargs)
    name = "fiber_photometry_table_region"
    return super(FiberPhotometryTable, self).create_region(name=name, region=region, description=description)


FiberPhotometryTable.create_fiber_photometry_table_region = create_fiber_photometry_table_region

# the signal and control regions are both required, so they follow the required arguments of TimeSeries
_series_with_control_docval = (
    *get_docval(FiberPhotometryResponseSeries.__init__, "name", "data", "unit"),
    {
        "name": "fiber_photometry_table_region",
        "type": DynamicTableRegion,
        "doc": "References the row(s) of FiberPhotometryTable of the signal, one row per column of data.",
    },
    {
        "name": "control_fiber_photometry_table_region",
        "type": DynamicTableRegion,
        "doc": "References the row(s) of FiberPhotometryTable of the control, one row per column of data.",
    },
    *get_docval(
        FiberPhotometryResponseSeries.__init__,
        "resolution",
        "conversion",
        "offset",
        "timestamps",
        "starting_time",
        "rate",
        "comments",
        "description",
        "control",
        "control_description",
        "continuity",
    ),
)


@register_class("ModulatedResponseSeries", "ndx-fiber-photometry")
class ModulatedResponseSeries(FiberPhotometryResponseSeries):
    """Fiber photometry signal recorded while the signal and control excitation were on at the same time."""

    __nwbfields__ = ({"name": "control_fiber_photometry_table_region", "child": True},)

    @docval(*_series_with_control_docval)
    def __init__(self, **kwargs):
        control_fiber_photometry_table_region = popargs("control_fiber_photometry_table_region", kwargs)
        super().__init__(**kwargs)
        self.control_fiber_photometry_table_region = control_fiber_photometry_table_region


@register_class("DeltaFOverFResponseSeries", "ndx-fiber-photometry")
class DeltaFOverFResponseSeries(FiberPhotometryResponseSeries):
    """Change in fluorescence of the signal relative to a baseline computed from the control (dF/F)."""

    __nwbfields__ = ({"name": "control_fiber_photometry_table_region", "child": True},)

    @docval(*_series_with_control_docval)
    def __init__(self, **kwargs):
        control_fiber_photometry_table_region = popargs("control_fiber_photometry_table_region", kwargs)
        super().__init__(**kwargs)
        self.control_fiber_photometry_table_region = control_fiber_photometry_table_region
