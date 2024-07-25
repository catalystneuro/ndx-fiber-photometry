from pynwb import NWBHDF5IO


def test_readme(tmp_path):
    """Test the first python code block in the README by simply executing it."""
    with open("README.md") as f:
        lines = f.readlines()
    start_line = None
    for i, line in enumerate(lines):
        if line == "```python\n":
            start_line = i
        elif line == "```\n" and start_line is not None:
            end_line = i
            break
    code_lines = lines[start_line + 1 : end_line]
    code_block = "".join(code_lines)
    readme_outputs = {}
    exec(code_block, globals(), readme_outputs)
    nwbfile = readme_outputs["nwbfile"]
    nwbfile_path = tmp_path / "test_ndx_fiber_photometry.nwb"
    with NWBHDF5IO(nwbfile_path, mode="w") as io:
        io.write(nwbfile)
