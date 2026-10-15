# v0.3.0 (October 15th, 2026)

## Breaking changes

* Requires ndx-ophys-devices 0.4.0 (`ndx_ophys_devices>=0.4.0,<0.5`), which changes several types used by this extension:
  * `FiberInsertion` is removed. `OpticalFiber.fiber_insertion` is now an optional `StereotacticPosition` named "fiber_insertion", with `anatomical_target`, `origin`, `orientation`, `x_in_mm`, `y_in_mm`, `z_in_mm` and the optional angles `pitch_in_deg`, `yaw_in_deg` and `roll_in_deg`. The coordinates give the position of the fiber tip, so the old `depth_in_mm` is folded into the dorsoventral coordinate.
  * `ViralVectorInjection` no longer has `location`, `hemisphere`, `reference`, `ap_in_mm`, `ml_in_mm`, `dv_in_mm`, `pitch_in_deg`, `yaw_in_deg`, `roll_in_deg`, `stereotactic_rotation_in_deg` or `stereotactic_tilt_in_deg`. The injection site goes in the optional `viral_injection_coordinates`, a `StereotacticPosition` named "viral_injection_coordinates".
  * `gain` and `gain_unit` moved from `PhotodetectorModel` to `Photodetector`.
* Requires Python 3.10 or later.

## Reading files written with earlier versions

Files written with ndx-fiber-photometry 0.2.x and ndx-ophys-devices 0.3.x fail to read with `No specification for 'FiberInsertion'` in a Python session that has imported ndx-fiber-photometry 0.3.0 or ndx-ophys-devices 0.4.0, because the installed namespaces take precedence over the ones cached in the file. To read such files, open them in a session that does not import these packages; pynwb then loads the cached namespaces.

## Installing with NeuroConv

NeuroConv 0.10.2 and earlier import `FiberInsertion` in the TDT fiber photometry interface and allow ndx-fiber-photometry 0.3.0, which then fails on import. Until a NeuroConv release caps it ([PR #2102](https://github.com/catalystneuro/neuroconv/pull/2102)), run `pip install "ndx-fiber-photometry<0.3"` alongside NeuroConv.

## Other changes

* Fixed the contact email addresses in the namespace.
* Declared explicit `dims` for all datasets with a shape, so that regenerating the spec gives the same result with pynwb 3.x and 4.x.
* Clarified the docs of the `notes` column and of `FiberPhotometryResponseSeries.data`, and listed `NWBContainer` in place of the unused `Device` in the namespace.
* Updated the example in the README and the tests with realistic values: VTA coordinates, LED excitation at 465 nm with a 405 nm isosbestic control row, jRGECO1a as the red indicator, a photoreceiver with its gain, and lock-in carrier frequencies for the commanded voltages.
* `test_readme.py` now finds `README.md` relative to the test file and reads it as UTF-8, and the roundtrip test writes to a temporary directory.
* `requirements-min.txt` now pins the minimum supported versions.
* Bumped `gh-action-pypi-publish` to v1.14.2 in the publish workflow, so that wheels with Metadata-Version 2.5 can be uploaded.

# v0.2.4 (October 14th, 2026)

* Capped the ndx-ophys-devices dependency at `<0.4`. ndx-ophys-devices 0.4.0 removes `FiberInsertion`, which this release uses. ndx-fiber-photometry 0.3.0 will adopt ndx-ophys-devices 0.4.0. If you have pinned `ndx-fiber-photometry==0.2.3` and a fresh install fails with `cannot import name 'FiberInsertion'`, run `pip install "ndx-ophys-devices<0.4"`.

# v0.2.3 (January 23rd, 2026)

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
