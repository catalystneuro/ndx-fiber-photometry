import numpy as np
from pynwb import get_type_map

from ndx_fiber_photometry import FiberPhotometryResponseSeries


def get_spec(neurodata_type):
    return get_type_map().namespace_catalog.get_spec("ndx-fiber-photometry", neurodata_type)


def test_response_series_table_region_is_optional():
    # extensions such as ndx-guppy create response series without a table region
    series = FiberPhotometryResponseSeries(
        name="fiber_photometry_response_series",
        description="response series without a table region",
        data=np.zeros((10, 1)),
        unit="V",
        rate=30.0,
    )
    assert series.fiber_photometry_table_region is None


def test_dims_are_declared():
    response_data = get_spec("FiberPhotometryResponseSeries").get_dataset("data")
    assert response_data.dims == [["num_times"], ["num_times", "num_fibers"]]

    commanded_data = get_spec("CommandedVoltageSeries").get_dataset("data")
    assert commanded_data.dims == ["num_times"]

    table = get_spec("FiberPhotometryTable")
    # skip the unnamed VectorData spec inherited from DynamicTable
    for column in table.datasets:
        if column.name is not None:
            assert column.dims is not None, column.name
    assert table.get_dataset("coordinates").dims == ["num_rows", "x,y,z"]
