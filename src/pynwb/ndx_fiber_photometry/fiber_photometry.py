from hdmf.utils import docval, popargs
from pynwb import get_class

FiberPhotometryTable = get_class("FiberPhotometryTable", "ndx-fiber-photometry")

@docval(
    {'name': 'region', 'type': list, 'doc': 'the indices of the FiberPhotometryTable'},
    {'name': 'description', 'type': str, 'doc': 'a brief description of what these table entries represent'},
)
def create_fiber_photometry_table_region(self, **kwargs):
    region, description = popargs('region', 'description', kwargs)
    name = 'fiber_photometry_table_region'
    return super(FiberPhotometryTable, self).create_region(name=name, region=region, description=description)

FiberPhotometryTable.create_fiber_photometry_table_region = create_fiber_photometry_table_region