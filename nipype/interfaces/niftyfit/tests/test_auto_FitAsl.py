# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..asl import FitAsl


def test_FitAsl_inputs():
    input_map = dict(IRoutput=dict(argstr='-IRoutput %s',
    ),
    IRvolume=dict(argstr='-IRvolume %s',
    ),
    L=dict(argstr='-L %f',
    ),
    LDD=dict(argstr='-LDD %f',
    ),
    PLD=dict(argstr='-PLD %f',
    ),
    T1a=dict(argstr='-T1a %f',
    ),
    Tinv1=dict(argstr='-Tinv1 %f',
    ),
    Tinv2=dict(argstr='-Tinv2 %f',
    ),
    args=dict(argstr='%s',
    ),
    cbf_file=dict(argstr='-cbf %s',
    genfile=True,
    ),
    dPLD=dict(argstr='-dPLD %f',
    ),
    dTinv2=dict(argstr='-dTinv2 %f',
    ),
    eff=dict(argstr='-eff %f',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    error_file=dict(argstr='-error %s',
    genfile=True,
    ),
    gmL=dict(argstr='-gmL %f',
    ),
    gmT1=dict(argstr='-gmT1 %f',
    ),
    gmTTT=dict(argstr='-gmTTT %f',
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    m0map=dict(argstr='-m0map %s',
    ),
    m0mape=dict(argstr='-m0mape %s',
    ),
    mask=dict(argstr='-mask %s',
    position=2,
    ),
    mul=dict(argstr='-mul %f',
    ),
    mulgm=dict(argstr='-sig',
    ),
    out=dict(argstr='-out %f',
    ),
    pasl=dict(argstr='-pasl',
    ),
    pcasl=dict(argstr='-pcasl',
    ),
    pv0=dict(argstr='-pv0 %d',
    ),
    pv2=dict(argstr='-pv2 %d',
    ),
    pv3=dict(argstr='-pv3 %d %d %d',
    ),
    pvthreshold=dict(argstr='-pvthreshold',
    ),
    seg=dict(argstr='-seg %s',
    ),
    segstyle=dict(argstr='-segstyle',
    ),
    sig=dict(argstr='-sig',
    ),
    source_file=dict(argstr='-source %s',
    mandatory=True,
    position=1,
    ),
    syn_file=dict(argstr='-syn %s',
    genfile=True,
    ),
    t1map=dict(argstr='-t1map %s',
    ),
    terminal_output=dict(nohash=True,
    ),
    wmL=dict(argstr='-wmL %f',
    ),
    wmT1=dict(argstr='-wmT1 %f',
    ),
    wmTTT=dict(argstr='-wmTTT %f',
    ),
    )
    inputs = FitAsl.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_FitAsl_outputs():
    output_map = dict(cbf_file=dict(),
    error_file=dict(),
    syn_file=dict(),
    )
    outputs = FitAsl.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value