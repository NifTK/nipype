# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from ..utils import Slicer


def test_Slicer_inputs():
    input_map = dict(all_axial=dict(argstr='-A',
    position=10,
    requires=[u'image_width'],
    xor=(u'single_slice', u'middle_slices', u'all_axial', u'sample_axial'),
    ),
    args=dict(argstr='%s',
    ),
    colour_map=dict(argstr='-l %s',
    position=4,
    ),
    dither_edges=dict(argstr='-t',
    position=7,
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    image_edges=dict(argstr='%s',
    position=2,
    ),
    image_width=dict(argstr='%d',
    position=-2,
    ),
    in_file=dict(argstr='%s',
    mandatory=True,
    position=1,
    ),
    intensity_range=dict(argstr='-i %.3f %.3f',
    position=5,
    ),
    label_slices=dict(argstr='-L',
    position=3,
    usedefault=True,
    ),
    middle_slices=dict(argstr='-a',
    position=10,
    xor=(u'single_slice', u'middle_slices', u'all_axial', u'sample_axial'),
    ),
    nearest_neighbour=dict(argstr='-n',
    position=8,
    ),
    out_file=dict(argstr='%s',
    genfile=True,
    hash_files=False,
    position=-1,
    ),
    output_type=dict(),
    sample_axial=dict(argstr='-S %d',
    position=10,
    requires=[u'image_width'],
    xor=(u'single_slice', u'middle_slices', u'all_axial', u'sample_axial'),
    ),
    scaling=dict(argstr='-s %f',
    position=0,
    ),
    show_orientation=dict(argstr='%s',
    position=9,
    usedefault=True,
    ),
    single_slice=dict(argstr='-%s',
    position=10,
    requires=[u'slice_number'],
    xor=(u'single_slice', u'middle_slices', u'all_axial', u'sample_axial'),
    ),
    slice_number=dict(argstr='-%d',
    position=11,
    ),
    terminal_output=dict(nohash=True,
    ),
    threshold_edges=dict(argstr='-e %.3f',
    position=6,
    ),
    )
    inputs = Slicer.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_Slicer_outputs():
    output_map = dict(out_file=dict(),
    )
    outputs = Slicer.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
