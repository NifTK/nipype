# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from ..utils import SigLoss


def test_SigLoss_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    echo_time=dict(argstr='--te=%f',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    in_file=dict(argstr='-i %s',
    mandatory=True,
    ),
    mask_file=dict(argstr='-m %s',
    ),
    out_file=dict(argstr='-s %s',
    genfile=True,
    ),
    output_type=dict(),
    slice_direction=dict(argstr='-d %s',
    ),
    terminal_output=dict(nohash=True,
    ),
    )
    inputs = SigLoss.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_SigLoss_outputs():
    output_map = dict(out_file=dict(),
    )
    outputs = SigLoss.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
