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
# ndx-fiber-photometry depends on ndx-ophys-devices,
# so importing it here prevents namespace errors when users import this package directly
import ndx_ophys_devices  # noqa: F401

load_namespaces(str(__spec_path))

# TODO: Define your classes here to make them accessible at the package level.
# Either have PyNWB generate a class from the spec using `get_class` as shown
# below or write a custom class and register it using the class decorator
# `@register_class("TetrodeSeries", "ndx-fiber-photometry")`
FiberPhotometryViruses = get_class("FiberPhotometryViruses", "ndx-fiber-photometry")
FiberPhotometryVirusInjections = get_class("FiberPhotometryVirusInjections", "ndx-fiber-photometry")
FiberPhotometryIndicators = get_class("FiberPhotometryIndicators", "ndx-fiber-photometry")
FiberPhotometry = get_class("FiberPhotometry", "ndx-fiber-photometry")
from .fiber_photometry import FiberPhotometryTable

FiberPhotometryResponseSeries = get_class("FiberPhotometryResponseSeries", "ndx-fiber-photometry")
CommandedVoltageSeries = get_class("CommandedVoltageSeries", "ndx-fiber-photometry")

# Remove these functions from the package
del load_namespaces, get_class
