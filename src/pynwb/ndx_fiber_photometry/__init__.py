import os
from pynwb import load_namespaces, get_class

try:
    from importlib.resources import files
except ImportError:
    # TODO: Remove when python 3.9 becomes the new minimum
    from importlib_resources import files

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / "ndx-fiber-photometry.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not os.path.exists(__spec_path):
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / "ndx-fiber-photometry.namespace.yaml"

# Load the namespace
load_namespaces(str(__spec_path))

# TODO: Define your classes here to make them accessible at the package level.
# Either have PyNWB generate a class from the spec using `get_class` as shown
# below or write a custom class and register it using the class decorator
# `@register_class("TetrodeSeries", "ndx-fiber-photometry")`
Indicator = get_class("Indicator", "ndx-fiber-photometry")
OpticalFiber = get_class("OpticalFiber", "ndx-fiber-photometry")
ExcitationSource = get_class("ExcitationSource", "ndx-fiber-photometry")
Photodetector = get_class("Photodetector", "ndx-fiber-photometry")
DichroicMirror = get_class("DichroicMirror", "ndx-fiber-photometry")
BandOpticalFilter = get_class("BandOpticalFilter", "ndx-fiber-photometry")
EdgeOpticalFilter = get_class("EdgeOpticalFilter", "ndx-fiber-photometry")
FiberPhotometry = get_class("FiberPhotometry", "ndx-fiber-photometry")
from .fiber_photometry import FiberPhotometryTable
FiberPhotometryResponseSeries = get_class("FiberPhotometryResponseSeries", "ndx-fiber-photometry")
CommandedVoltageSeries = get_class("CommandedVoltageSeries", "ndx-fiber-photometry")


# NOTE: `widgets/tetrode_series_widget.py` adds a "widget"
# attribute to the TetrodeSeries class. This attribute is used by NWBWidgets.
# Delete the `widgets` subpackage or the `tetrode_series_widget.py` module
# if you do not want to define a custom widget for your extension neurodata
# type.

# Remove these functions from the package
del load_namespaces, get_class
