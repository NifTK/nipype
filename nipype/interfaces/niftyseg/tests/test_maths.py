# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from nipype.interfaces.niftyseg import (no_niftyseg, get_custom_path,
                                        UnaryMaths, BinaryMaths,
                                        BinaryMathsInteger, TupleMaths,
                                        Merge)
from nipype.testing import example_data
import os
import pytest


@pytest.mark.skipif(no_niftyseg(cmd='seg_maths'),
                    reason="niftyseg is not installed")
def test_unary_maths():

    # Create a node object
    unarym = UnaryMaths()

    # Check if the command is properly defined
    assert unarym.cmd == get_custom_path('seg_maths')

    # test raising error with mandatory args absent
    with pytest.raises(ValueError):
        unarym.run()

    # Assign some input data
    in_file = example_data('im1.nii')
    unarym.inputs.in_file = in_file
    unarym.inputs.operation = 'otsu'
    unarym.inputs.output_datatype = 'float'

    expected_cmd = '{cmd} {in_file} -otsu -odt float {out_file}'.format(
        cmd=get_custom_path('seg_maths'),
        in_file=in_file,
        out_file=os.path.join(os.getcwd(), 'im1_otsu.nii'))

    assert unarym.cmdline == expected_cmd


@pytest.mark.skipif(no_niftyseg(cmd='seg_maths'),
                    reason="niftyseg is not installed")
def test_binary_maths():

    # Create a node object
    binarym = BinaryMaths()

    # Check if the command is properly defined
    assert binarym.cmd == get_custom_path('seg_maths')

    # test raising error with mandatory args absent
    with pytest.raises(ValueError):
        binarym.run()

    # Assign some input data
    in_file = example_data('im1.nii')
    binarym.inputs.in_file = in_file
    binarym.inputs.operand_value = 2.0
    binarym.inputs.operation = 'sub'
    binarym.inputs.output_datatype = 'float'

    cmd_tmp = '{cmd} {in_file} -sub 2.00000000 -odt float {out_file}'
    expected_cmd = cmd_tmp.format(
        cmd=get_custom_path('seg_maths'),
        in_file=in_file,
        out_file=os.path.join(os.getcwd(), 'im1_sub.nii'))

    assert binarym.cmdline == expected_cmd


@pytest.mark.skipif(no_niftyseg(cmd='seg_maths'),
                    reason="niftyseg is not installed")
def test_int_binary_maths():

    # Create a node object
    ibinarym = BinaryMathsInteger()

    # Check if the command is properly defined
    assert ibinarym.cmd == get_custom_path('seg_maths')

    # test raising error with mandatory args absent
    with pytest.raises(ValueError):
        ibinarym.run()

    # Assign some input data
    in_file = example_data('im1.nii')
    ibinarym.inputs.in_file = in_file
    ibinarym.inputs.operand_value = 2
    ibinarym.inputs.operation = 'dil'
    ibinarym.inputs.output_datatype = 'float'

    expected_cmd = '{cmd} {in_file} -dil 2 -odt float {out_file}'.format(
        cmd=get_custom_path('seg_maths'),
        in_file=in_file,
        out_file=os.path.join(os.getcwd(), 'im1_dil.nii'))

    assert ibinarym.cmdline == expected_cmd


@pytest.mark.skipif(no_niftyseg(cmd='seg_maths'),
                    reason="niftyseg is not installed")
def test_tuple_maths():

    # Create a node object
    tuplem = TupleMaths()

    # Check if the command is properly defined
    assert tuplem.cmd == get_custom_path('seg_maths')

    # test raising error with mandatory args absent
    with pytest.raises(ValueError):
        tuplem.run()

    # Assign some input data
    in_file = example_data('im1.nii')
    op_file = example_data('im2.nii')
    tuplem.inputs.in_file = in_file
    tuplem.inputs.operation = 'lncc'
    tuplem.inputs.operand_file1 = op_file
    tuplem.inputs.operand_value2 = 2.0
    tuplem.inputs.output_datatype = 'float'

    cmd_tmp = '{cmd} {in_file} -lncc {op} 2.00000000 -odt float {out_file}'
    expected_cmd = cmd_tmp.format(
        cmd=get_custom_path('seg_maths'),
        in_file=in_file,
        op=op_file,
        out_file=os.path.join(os.getcwd(), 'im1_lncc.nii'))

    assert tuplem.cmdline == expected_cmd


@pytest.mark.skipif(no_niftyseg(cmd='seg_maths'),
                    reason="niftyseg is not installed")
def test_merge():

    # Create a node object
    merge = Merge()

    # Check if the command is properly defined
    assert merge.cmd == get_custom_path('seg_maths')

    # test raising error with mandatory args absent
    with pytest.raises(ValueError):
        merge.run()

    # Assign some input data
    in_file = example_data('im1.nii')
    file1 = example_data('im2.nii')
    file2 = example_data('im3.nii')
    merge.inputs.in_file = in_file
    merge.inputs.merge_files = [file1, file2]
    merge.inputs.dimension = 2
    merge.inputs.output_datatype = 'float'

    cmd_tmp = '{cmd} {in_file} -merge 2 2 {f1} {f2} -odt float {out_file}'
    expected_cmd = cmd_tmp.format(
        cmd=get_custom_path('seg_maths'),
        in_file=in_file,
        f1=file1,
        f2=file2,
        out_file=os.path.join(os.getcwd(), 'im1_merged.nii'))

    assert merge.cmdline == expected_cmd