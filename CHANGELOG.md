# v0.2.3 (Upcoming)

* Made `dichroic_mirror` optional in the `FiberPhotometryTable` [PR #50](https://github.com/catalystneuro/ndx-fiber-photometry/pull/50).

# v0.2.2 (September 23rd, 2025)

* Updated the `FiberPhotometryViruses` and `FiberPhotometryVirusInjections` groups to be optional in the `FiberPhotometry` container [PR #47](https://github.com/catalystneuro/ndx-fiber-photometry/pull/47).

# v0.2.1 (September 22nd, 2025)

* Updated the auto-publish workflow to use attestation, which is the new standard on PyPI [PR #41](https://github.com/catalystneuro/ndx-fiber-photometry/pull/41).
* Updated requirements to depend on ndx-ophys-devices>=0.3.1 [PR #40](https://github.com/catalystneuro/ndx-fiber-photometry/pull/40)

# v0.2.0 (September 18th, 2025)

* Refactored the extension to depend on ndx-ophys-devices for device and biological component specification, replacing its previous standalone device types [PR #37](https://github.com/catalystneuro/ndx-fiber-photometry/pull/37).

# v0.1.0

### Features
Initial release of 11 new neurodata types:
* `Indicator` extends `Device` to hold metadata on the fluorescent indicator (ex. label=GCaMP6).
* `OpticalFiber` extends `Device` to hold metadata on the optical fiber (ex. numerical_aperture=0.39).
* `ExcitationSource` extends `Device` to hold metadata on the excitation source (ex. excitation_wavelength_in_nm=470.0).
* `Photodetector` extends `Device` to hold metadata on the photodetector (ex. detected_wavelength_in_nm=520.0).
* `DichroicMirror` extends `Device` to hold metadata on the dichroic mirror (ex. cut_on_wavelength_in_nm=470.0).
* `BandOpticalFilter` extends `Device` to hold metadata on any bandpass or bandstop optical filters (ex. center_wavelength_in_nm=505.0).
* `EdgeOpticalFilter` extends `Device` to hold metadata on any edge optical filters (ex. cut_wavelength_in_nm=585.0).
* `FiberPhotometryResponseSeries` extends `TimeSeries` to hold the recorded fiber photometry responses.
* `CommandedVoltageSeries` extends `TimeSeries` to hold the commanded voltage values for a single fiber photometry trace.
* `FiberPhotometryTable` extends `DynamicTable` to hold information on the fiber photometry setup.
    Each row of the table reference a combination of the devices and a commanded voltage series that correspond to a single fiber photometry trace.
* `FiberPhotometry` extends `LabMetaData` to hold the `FiberPhotometryTable`.

### Fixes
* Replaces old ndx-photometry extension: https://github.com/catalystneuro/ndx-photometry
