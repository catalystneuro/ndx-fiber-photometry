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


@docval(
    {"name": "region", "type": list, "doc": "the indices of the FiberPhotometryTable"},
    {"name": "description", "type": str, "doc": "a brief description of what these table entries represent"},
)
def create_control_fiber_photometry_table_region(self, **kwargs):
    region, description = popargs("region", "description", kwargs)
    name = "control_fiber_photometry_table_region"
    return super(FiberPhotometryTable, self).create_region(name=name, region=region, description=description)


FiberPhotometryTable.create_control_fiber_photometry_table_region = create_control_fiber_photometry_table_region

# the signal and control regions are both required, so they follow the required arguments of TimeSeries
_series_with_control_docval = (
    *get_docval(FiberPhotometryResponseSeries.__init__, "name", "data", "unit"),
    {
        "name": "fiber_photometry_table_region",
        "type": DynamicTableRegion,
        "doc": (
            "References the row(s) of FiberPhotometryTable for the signal channel, one row per column of data, "
            "in the same order."
        ),
    },
    {
        "name": "control_fiber_photometry_table_region",
        "type": DynamicTableRegion,
        "doc": (
            "References the row(s) of FiberPhotometryTable for the control channel, such as the isosbestic "
            "excitation, one row per column of data, in the same order. Row i shares its optical fiber and "
            "photodetector with row i of fiber_photometry_table_region."
        ),
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


def _check_control_region(control_region, signal_region):
    if control_region.name != "control_fiber_photometry_table_region":
        raise ValueError(
            "The control region must be named 'control_fiber_photometry_table_region', "
            f"got '{control_region.name}'. Use FiberPhotometryTable.create_control_fiber_photometry_table_region."
        )
    if len(control_region.data) != len(signal_region.data):
        raise ValueError(
            "fiber_photometry_table_region and control_fiber_photometry_table_region must have the same number of "
            f"rows, got {len(signal_region.data)} and {len(control_region.data)}."
        )


@register_class("ModulatedResponseSeries", "ndx-fiber-photometry")
class ModulatedResponseSeries(FiberPhotometryResponseSeries):
    """Raw photodetector output that mixes the fluorescence from the signal and control excitation, before it is
    separated into one series per excitation.
    """

    __nwbfields__ = ({"name": "control_fiber_photometry_table_region", "child": True},)

    @docval(*_series_with_control_docval)
    def __init__(self, **kwargs):
        control_fiber_photometry_table_region = popargs("control_fiber_photometry_table_region", kwargs)
        _check_control_region(control_fiber_photometry_table_region, kwargs["fiber_photometry_table_region"])
        super().__init__(**kwargs)
        self.control_fiber_photometry_table_region = control_fiber_photometry_table_region


# the control region is optional for dF/F, since the baseline can come from the signal channel alone
_delta_f_over_f_docval = tuple(
    (
        {
            **argument,
            "default": None,
            "doc": argument["doc"] + " Omit it when the baseline comes from the signal channel alone.",
        }
        if argument["name"] == "control_fiber_photometry_table_region"
        else argument
    )
    for argument in _series_with_control_docval
)


@register_class("DeltaFOverFResponseSeries", "ndx-fiber-photometry")
class DeltaFOverFResponseSeries(FiberPhotometryResponseSeries):
    """Change in fluorescence of the signal relative to a baseline (dF/F), estimated from a control channel or
    from the signal channel alone.
    """

    __nwbfields__ = ({"name": "control_fiber_photometry_table_region", "child": True},)

    @docval(*_delta_f_over_f_docval)
    def __init__(self, **kwargs):
        control_fiber_photometry_table_region = popargs("control_fiber_photometry_table_region", kwargs)
        if control_fiber_photometry_table_region is not None:
            _check_control_region(control_fiber_photometry_table_region, kwargs["fiber_photometry_table_region"])
        super().__init__(**kwargs)
        self.control_fiber_photometry_table_region = control_fiber_photometry_table_region
