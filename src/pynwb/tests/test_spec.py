import numpy as np
import pytest

from pynwb import get_type_map

from ndx_fiber_photometry import FiberPhotometryResponseSeries


def get_spec(neurodata_type):
    return get_type_map().namespace_catalog.get_spec("ndx-fiber-photometry", neurodata_type)


def test_response_series_requires_table_region():
    with pytest.raises(TypeError, match="fiber_photometry_table_region"):
        FiberPhotometryResponseSeries(
            name="fiber_photometry_response_series",
            description="response series without a table region",
            data=np.zeros((10, 1)),
            unit="V",
            rate=30.0,
        )


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
