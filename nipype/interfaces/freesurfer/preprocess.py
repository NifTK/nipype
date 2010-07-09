# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Provides interfaces to various commands provided by freeusrfer

"""
__docformat__ = 'restructuredtext'

import os
from glob import glob
import numpy as np

from nipype.externals.pynifti import load
from nipype.utils.filemanip import fname_presuffix
from nipype.interfaces.io import FreeSurferSource

from nipype.interfaces.freesurfer.base import FSCommand, FSTraitedSpec
from nipype.interfaces.base import (TraitedSpec, File, traits,
                                    Directory, InputMultiPath)
from nipype.utils.misc import isdefined


class ParseDICOMDirInputSpec(FSTraitedSpec):
    dicom_dir = Directory(exists=True, argstr='--d %s', mandatory=True,
                         desc='path to siemens dicom directory')
    dicom_info_file = File('dicominfo.txt', argstr='--o %s', usedefault=True,
                           desc='file to which results are written')
    sortbyrun = traits.Bool(argstr='--sortbyrun', desc='assign run numbers')
    summarize = traits.Bool(argstr='--summarize',
                            desc='only print out info for run leaders')

class ParseDICOMDirOutputSpec(TraitedSpec):
    dicom_info_file = File(exists=True,
                           desc='text file containing dicom information')

class ParseDICOMDir(FSCommand):
    """Uses mri_parse_sdcmdir to get information from dicom directories
    
    Examples
    --------

    >>> from nipype.interfaces.freesurfer import ParseDICOMDir
    >>> dcminfo = ParseDICOMDir()
    >>> dcminfo.inputs.dicom_dir = '.'
    >>> dcminfo.inputs.sortbyrun = True
    >>> dcminfo.inputs.summarize = True
    >>> dcminfo.cmdline
    'mri_parse_sdcmdir --d . --o dicominfo.txt --sortbyrun --summarize'
    
   """

    _cmd = 'mri_parse_sdcmdir'
    input_spec = ParseDICOMDirInputSpec
    output_spec = ParseDICOMDirOutputSpec
    
    def _list_outputs(self):
        outputs = self.output_spec().get()
        if isdefined(self.inputs.dicom_info_file):
            outputs['dicom_info_file'] = os.path.join(os.getcwd(),self.inputs.dicom_info_file)
        return outputs

class UnpackSDICOMDirInputSpec(FSTraitedSpec):
    source_dir = Directory(exists=True, argstr='-src %s',
                           mandatory=True,
                           desc='directory with the DICOM files')
    output_dir = Directory(argstr='-targ %s',
                           desc='top directory into which the files will be unpacked')
    run_info = traits.Tuple(traits.Int, traits.Str, traits.Str, traits.Str,
                           mandatory=True,
                           argstr='-run %d %s %s %s',
                           xor = ('run_info', 'config', 'seq_config'),
        desc='runno subdir format name : spec unpacking rules on cmdline')
    config = File(exists=True, argstr='-cfg %s',
                  mandatory=True,
                  xor = ('run_info', 'config', 'seq_config'),
                  desc='specify unpacking rules in file')
    seq_config = File(exists=True, argstr='-seqcfg %s',
                     mandatory=True,
                     xor = ('run_info', 'config', 'seq_config'),
                     desc='specify unpacking rules based on sequence')
    dir_structure = traits.Enum('fsfast', 'generic', argstr='-%s',
                                desc='unpack to specified directory structures')
    no_info_dump = traits.Bool(argstr='-noinfodump',
                             desc='do not create infodump file')
    scan_only = File(exists=True, argstr='-scanonly %s',
                    desc='only scan the directory and put result in file')
    log_file = File(exists=True, argstr='-log %s',
                   desc='explicilty set log file')
    spm_zeropad = traits.Int(argstr='-nspmzeropad %d',
                            desc='set frame number zero padding width for SPM')
    no_unpack_err = traits.Bool(argstr='-no-unpackerr',
                              desc='do not try to unpack runs with errors')

class UnpackSDICOMDir(FSCommand):
    """Use unpacksdcmdir to convert dicom files

    Call unpacksdcmdir -help from the command line to see more information on
    using this command.

    Examples
    --------

    >>> from nipype.interfaces.freesurfer import UnpackSDICOMDir
    >>> unpack = UnpackSDICOMDir()
    >>> unpack.inputs.source_dir = '.'
    >>> unpack.inputs.output_dir = '.'
    >>> unpack.inputs.run_info = (5, 'mprage', 'nii', 'struct')
    >>> unpack.inputs.dir_structure = 'generic'
    >>> unpack.cmdline
    'unpacksdcmdir -generic -targ . -run 5 mprage nii struct -src .'
    """
    _cmd = 'unpacksdcmdir'
    input_spec = UnpackSDICOMDirInputSpec


class MRIConvertInputSpec(FSTraitedSpec):
    read_only = traits.Bool(argstr='--read_only',
                            desc='read the input volume')
    no_write = traits.Bool(argstr='--no_write',
                           desc='do not write output')
    in_info = traits.Bool(argstr='--in_info',
                         desc='display input info')
    out_info = traits.Bool(argstr='--out_info',
                          desc='display output info')
    in_stats = traits.Bool(argstr='--in_stats',
                          desc='display input stats')
    out_stats = traits.Bool(argstr='--out_stats',
                           desc='display output stats')
    in_matrix = traits.Bool(argstr='--in_matrix',
                           desc='display input matrix')
    out_matrix = traits.Bool(argstr='--out_matrix',
                            desc='display output matrix')
    in_i_size = traits.Int(argstr='--in_i_size %d',
                           desc='input i size')
    in_j_size = traits.Int(argstr='--in_j_size %d',
                           desc='input j size')
    in_k_size = traits.Int(argstr='--in_k_size %d',
                           desc='input k size')
    force_ras = traits.Bool(argstr='--force_ras_good',
                           desc='use default when orientation info absent')
    in_i_dir = traits.Tuple(traits.Float, traits.Float,traits.Float,
                           argstr='--in_i_direction %f %f %f',
                           desc='<R direction> <A direction> <S direction>')
    in_j_dir = traits.Tuple(traits.Float, traits.Float,traits.Float,
                           argstr='--in_j_direction %f %f %f',
                           desc='<R direction> <A direction> <S direction>')
    in_k_dir = traits.Tuple(traits.Float, traits.Float,traits.Float,
                           argstr='--in_k_direction %f %f %f',
                           desc='<R direction> <A direction> <S direction>')
    #[''.join([i['x'],i['y'],i['z']]) for i in \
    #    walk(dict(x=lambda:['L','R'],y=lambda:['A','P'],z=lambda:['I','S']).items())]
    _orientations = ['LAI', 'LAS', 'RAI', 'RAS', 'LPI', 'LPS', 'RPI', 'RPS']
    in_orientation = traits.Enum(_orientations,
                                argstr='--in_orientation %s',
                                desc='specify the input orientation')
    in_center = traits.List(traits.Float, maxlen=3,
                           argstr='--in_center %s',
                           desc='<R coordinate> <A coordinate> <S coordinate>')
    sphinx = traits.Bool(argstr='--sphinx',
                         desc='change orientation info to sphinx')
    out_i_count = traits.Int(argstr='--out_i_count %d',
                             desc='some count ?? in i direction')
    out_j_count = traits.Int(argstr='--out_j_count %d',
                             desc='some count ?? in j direction')
    out_k_count = traits.Int(argstr='--out_k_count %d',
                             desc='some count ?? in k direction')
    vox_size = traits.Tuple(traits.Float, traits.Float,traits.Float,
                           argstr='--voxsize %f %f %f',
                           desc='<size_x> <size_y> <size_z> specify the size (mm) - useful for upsampling or downsampling')
    out_i_size = traits.Int(argstr='--out_i_size %d',
                            desc='output i size')
    out_j_size = traits.Int(argstr='--out_j_size %d',
                            desc='output j size')
    out_k_size = traits.Int(argstr='--out_k_size %d',
                            desc='output k size')
    out_i_dir = traits.Tuple(traits.Float, traits.Float,traits.Float,
                           argstr='--out_i_direction %f %f %f',
                           desc='<R direction> <A direction> <S direction>')
    out_j_dir = traits.Tuple(traits.Float, traits.Float,traits.Float,
                           argstr='--out_j_direction %f %f %f',
                           desc='<R direction> <A direction> <S direction>')
    out_k_dir = traits.Tuple(traits.Float, traits.Float,traits.Float,
                             argstr='--out_k_direction %f %f %f',
                             desc='<R direction> <A direction> <S direction>')
    out_orientation = traits.Enum(_orientations,
                                argstr='--out_orientation %s',
                                desc='specify the output orientation')
    out_center = traits.Tuple(traits.Float, traits.Float,traits.Float,
                           argstr='--out_center %f %f %f',
                           desc='<R coordinate> <A coordinate> <S coordinate>')
    out_datatype = traits.Enum('uchar', 'short', 'int', 'float',
                              argstr='--out_data_type %s',
                              descr='output data type <uchar|short|int|float>')
    resample_type = traits.Enum('interpolate', 'weighted', 'nearest', 'sinc', 'cubic',
                               argstr='--resample_type %s',
                               desc='<interpolate|weighted|nearest|sinc|cubic> (default is interpolate)')
    no_scale = traits.Bool(argstr='--no_scale 1',
                          desc='dont rescale values for COR')
    no_change = traits.Bool(argstr='--nochange',
                           desc="don't change type of input to that of template")
    autoalign_matrix = File(exists=True, argstr='--autoalign %s',
                        desc='text file with autoalign matrix')
    unwarp_gradient = traits.Bool(argstr='--unwarp_gradient_nonlinearity',
                                 desc='unwarp gradient nonlinearity')
    apply_transform = File(exists=True, argstr='--apply_transform %s',
                    desc='apply xfm file')
    apply_inv_transform = File(exists=True, argstr='--apply_inverse_transform %s',
                       desc='apply inverse transformation xfm file')
    devolve_transform = traits.Str(argstr='--devolvexfm %s',
                            desc='subject id')
    crop_center = traits.Tuple(traits.Int, traits.Int, traits.Int,
                              argstr='--crop %d %d %d',
                              desc='<x> <y> <z> crop to 256 around center (x,y,z)')
    crop_size = traits.Tuple(traits.Int, traits.Int, traits.Int,
                            argstr='--cropsize %d %d %d',
                            desc='<dx> <dy> <dz> crop to size <dx, dy, dz>')
    cut_ends = traits.Int(argstr='--cutends %d',
                         desc='remove ncut slices from the ends')
    slice_crop = traits.Tuple(traits.Int, traits.Int,
                             argstr='--slice-crop %d %d',
                             desc='s_start s_end : keep slices s_start to s_end')
    slice_reverse = traits.Bool(argstr='--slice-reverse',
                               desc='reverse order of slices, update vox2ras')
    slice_bias = traits.Float(argstr='--slice-bias %f',
                             desc='apply half-cosine bias field')
    fwhm = traits.Float(argstr='--fwhm %f',
                        desc='smooth input volume by fwhm mm')
    _filetypes = ['cor', 'mgh', 'mgz', 'minc', 'analyze',
                  'analyze4d', 'spm', 'afni', 'brik', 'bshort',
                  'bfloat', 'sdt', 'outline', 'otl', 'gdf',
                  'nifti1', 'nii', 'niigz']
    _infiletypes = ['ge', 'gelx', 'lx','ximg', 'siemens', 'dicom', 'siemens+dicom']
    in_type = traits.Enum(_filetypes + _infiletypes, argstr='--in_type %s',
                        desc='input file type')
    out_type = traits.Enum(_filetypes, argstr='--out_type %s',
                        desc='output file type')
    ascii = traits.Bool(argstr='--ascii',
                        desc='save output as ascii col>row>slice>frame')
    reorder = traits.Tuple(traits.Int, traits.Int, traits.Int,
                           argstr='--reorder %d %d %d',
                           desc='olddim1 olddim2 olddim3')
    invert_contrast = traits.Float(argstr='--invert_contrast %f',
                                  desc='threshold for inversting contrast')
    in_file = File(exists=True, mandatory=True,
                  position=-2,
                  argstr='--input_volume %s',
                  desc='File to read/convert')
    out_file = File(argstr='--output_volume %s', 
                   position=-1, genfile=True,
                   desc='output filename or True to generate one')
    conform = traits.Bool(argstr='--conform',
                          desc='conform to 256^3')
    conform_min = traits.Bool(argstr='--conform_min',
                             desc='conform to smallest size')
    conform_size = traits.Float(argstr='--conform_size %s',
                               desc='conform to size_in_mm')
    parse_only = traits.Bool(argstr='--parse_only',
                            desc='parse input only')
    subject_name = traits.Str(argstr='--subject_name %s',
                             desc = 'subject name ???')
    reslice_like = File(exists=True, argstr='--reslice_like %s',
                       desc='reslice output to match file')
    template_type = traits.Enum(_filetypes + _infiletypes,
                               argstr='--template_type %s',
                               desc='template file type')
    split = traits.Bool(argstr='--split',
                        desc='split output frames into separate output files.')
    frame = traits.Int(argstr='--frame %d',
                       desc='keep only 0-based frame number')
    midframe = traits.Bool(argstr='--mid-frame',
                           desc='keep only the middle frame')
    skip_n = traits.Int(argstr='--nskip %d',
                       desc='skip the first n frames')
    drop_n = traits.Int(argstr='--ndrop %d',
                       desc='drop the last n frames')
    frame_subsample = traits.Tuple(traits.Int, traits.Int, traits.Int,
                                  argstr='--fsubsample %d %d %d',
                                  desc='start delta end : frame subsampling (end = -1 for end)')
    in_scale = traits.Float(argstr='--scale %f',
                         desc='input intensity scale factor')
    out_scale = traits.Float(argstr='--out-scale %d',
                            desc='output intensity scale factor')
    in_like = File(exists=True, argstr='--in_like %s',
                  desc='input looks like')
    fill_parcellation = traits.Bool(argstr='--fill_parcellation',
                                   desc='fill parcellation')
    smooth_parcellation = traits.Bool(argstr='--smooth_parcellation',
                                     desc='smooth parcellation')
    zero_outlines = traits.Bool(argstr='--zero_outlines',
                               desc='zero outlines')
    color_file = File(exists=True, argstr='--color_file %s',
                     desc='color file')
    no_translate = traits.Bool(argstr='--no_translate',
                              desc='???')
    status_file = File(argstr='--status %s',
                      desc='status file for DICOM conversion')
    sdcm_list = File(exists=True, argstr='--sdcmlist %s',
                    desc='list of DICOM files for conversion')
    template_info = traits.Bool('--template_info',
                               desc='dump info about template')
    crop_gdf = traits.Bool(argstr='--crop_gdf',
                           desc='apply GDF cropping')
    zero_ge_z_offset = traits.Bool(argstr='--zero_ge_z_offset',
                               desc='zero ge z offset ???')

class MRIConvertOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc='converted output file')

class MRIConvert(FSCommand):
    """use fs mri_convert to manipulate files

    .. note::
       Adds niigz as an output type option

    Examples
    --------

    >>> os.chdir( os.path.dirname( os.path.realpath( __file__ ) ) )
    >>> mc = MRIConvert()
    >>> mc.inputs.in_file = '../../emptydata/structural.nii'
    >>> mc.inputs.out_file = 'outfile.mgz'
    >>> mc.inputs.out_type = 'mgz'
    >>> mc.cmdline
    'mri_convert --out_type mgz --input_volume ../../emptydata/structural.nii --output_volume outfile.mgz'
    
    """
    _cmd = 'mri_convert'
    input_spec = MRIConvertInputSpec
    output_spec = MRIConvertOutputSpec

    filemap = dict(cor='cor', mgh='mgh', mgz='mgz', minc='mnc',
                   afni='brik', brik='brik', bshort='bshort',
                   spm='img', analyze='img', analyze4d='img',
                   bfloat='bfloat', nifti1='img', nii='nii',
                   niigz='nii.gz')

    def _format_arg(self, name, spec, value):
        if name in ['in_type', 'out_type', 'template_type']:
            if value == 'niigz':
                return spec.argstr % 'nii'
        return super(MRIConvert, self)._format_arg(name, spec, value)
    
    def _get_outfilename(self):
        outfile = self.inputs.out_file
        if not isdefined(outfile):
            if isdefined(self.inputs.out_type):
                suffix = '_out.' + self.filemap[self.inputs.out_type]
            else:
                suffix = '_out.nii.gz'
            outfile = fname_presuffix(self.inputs.in_file,
                                      newpath=os.getcwd(),
                                      suffix=suffix,
                                      use_ext=False)
        return outfile
        
    def _list_outputs(self):
        outputs = self.output_spec().get()
        outfile = self._get_outfilename()
        if isdefined(self.inputs.out_type):
            if self.inputs.out_type in ['spm', 'analyze']:
                # generate all outputs
                size = load(self.inputs.in_file).get_shape()
                if len(size)==3:
                    tp = 1
                else:
                    tp = size[-1]
                    # have to take care of all the frame manipulations
                    raise Exception('Not taking frame manipulations into account- please warn the developers')
                outfiles = []
                for i in range(tp):
                    outfiles.append(fname_presuffix(outfile,
                                                    suffix='%03d'%(i+1)))
                outfile = outfiles
        outputs['out_file'] = outfile
        return outputs

    def _gen_filename(self, name):
        if name == 'out_file':
            return self._get_outfilename()
        return None    

class DICOMConvertInputSpec(FSTraitedSpec):
    dicom_dir = Directory(exists=True, mandatory=True,
                         desc='dicom directory from which to convert dicom files')
    base_output_dir = Directory(mandatory=True,
            desc='directory in which subject directories are created')
    subject_dir_template = traits.Str('S.%04d', usedefault=True,
                          desc='template for subject directory name')
    subject_id = traits.Any(desc = 'subject identifier to insert into template')
    file_mapping = traits.List(traits.Tuple(traits.Str, traits.Str),
               desc='defines the output fields of interface')
    out_type = traits.Enum('niigz', MRIConvertInputSpec._filetypes,
                           usedefault=True,
               desc='defines the type of output file produced')
    dicom_info = File(exists=True,
               desc='File containing summary information from mri_parse_sdcmdir')
    seq_list = traits.List(traits.Str,
                           requires=['dicom_info'],
               desc='list of pulse sequence names to be converted.')
    ignore_single_slice = traits.Bool(requires=['dicom_info'],
               desc='ignore volumes containing a single slice')

class DICOMConvert(FSCommand):
    """use fs mri_convert to convert dicom files

    Examples
    --------

    >>> os.chdir( os.path.dirname( os.path.realpath( __file__ ) ) )
    >>> from nipype.interfaces.freesurfer import DICOMConvert
    >>> cvt = DICOMConvert()
    >>> cvt.inputs.dicom_dir = '../../emptydata/dicomdir'
    >>> cvt.inputs.file_mapping = [('nifti','*.nii'),('info','dicom*.txt'),('dti','*dti.bv*')]

    """
    _cmd = 'mri_convert'
    input_spec = DICOMConvertInputSpec

    def _get_dicomfiles(self):
        """validate fsl bet options
        if set to None ignore
        """
        return glob(os.path.abspath(os.path.join(self.inputs.dicom_dir,
                                                 '*-1.dcm')))

    def _get_outdir(self):
        """returns output directory"""
        subjid = self.inputs.subject_id
        if not isdefined(subjid):
            path,fname = os.path.split(self._get_dicomfiles()[0])
            subjid = int(fname.split('-')[0])
        if isdefined(self.inputs.subject_dir_template):
            subjid  = self.inputs.subject_dir_template % subjid
        basedir=self.inputs.base_output_dir
        if not isdefined(basedir):
            basedir = os.path.abspath('.')
        outdir = os.path.abspath(os.path.join(basedir,subjid))
        return outdir

    def _get_runs(self):
        """Returns list of dicom series that should be converted.

        Requires a dicom info summary file generated by ``DicomDirInfo``

        """
        seq = np.genfromtxt(self.inputs.dicom_info, dtype=object)
        runs = []
        for s in seq:
            if self.inputs.seq_list:
                if self.inputs.ignore_single_slice:
                    if (int(s[8]) > 1) and any([s[12].startswith(sn) for sn in self.inputs.seq_list]):
                        runs.append(int(s[2]))
                else:
                    if any([s[12].startswith(sn) for sn in self.inputs.seq_list]):
                        runs.append(int(s[2]))
            else:
                runs.append(int(s[2]))
        return runs

    def _get_filelist(self, outdir):
        """Returns list of files to be converted"""
        filemap = {}
        for f in self._get_dicomfiles():
            head,fname = os.path.split(f)
            fname,ext = os.path.splitext(fname)
            fileparts = fname.split('-')
            runno = int(fileparts[1])
            out_type = MRIConvert.filemap[self.inputs.out_type]
            outfile = os.path.join(outdir,'.'.join(('%s-%02d'% (fileparts[0],
                                                                runno),
                                                    out_type)))
            filemap[runno] = (f,outfile)
        if self.inputs.dicom_info:
            files = [filemap[r] for r in self._get_runs()]
        else:
            files = [filemap[r] for r in filemap.keys()]
        return files

    @property
    def cmdline(self):
        """ `command` plus any arguments (args)
        validates arguments and generates command line"""
        self._check_mandatory_inputs()
        outdir = self._get_outdir()
        cmd = []
        if not os.path.exists(outdir):
            cmdstr = 'python -c "import os; os.makedirs(\'%s\')"' % outdir
            cmd.extend([cmdstr])
        infofile = os.path.join(outdir, 'shortinfo.txt')
        if not os.path.exists(infofile):
            cmdstr = 'dcmdir-info-mgh %s > %s' % (self.inputs.dicom_dir,
                                                  infofile)
            cmd.extend([cmdstr])
        files = self._get_filelist(outdir)
        for infile,outfile in files:
            if not os.path.exists(outfile):
                single_cmd = '%s %s %s' % (self.cmd, infile,
                                           os.path.join(outdir, outfile))
                cmd.extend([single_cmd])
        return  '; '.join(cmd)

class ResampleInputSpec(FSTraitedSpec):
    in_file = File(exists=True, argstr='-i %s', mandatory=True,
                  desc='file to resample', position=-2)
    resampled_file = File(argstr='-o %s', desc='output filename', genfile=True,
                          position=-1)
    voxel_size = traits.Tuple(traits.Float, traits.Float, traits.Float,
                       argstr='-vs %.2f %.2f %.2f', desc='triplet of output voxel sizes',
                              mandatory=True)
        
class ResampleOutputSpec(TraitedSpec):
    resampled_file = File(exists=True,
                   desc='output filename')
    
class Resample(FSCommand):
    """Use FreeSurfer mri_convert to up or down-sample image files

    Examples
    --------
    
    >>> os.chdir( os.path.dirname( os.path.realpath( __file__ ) ) )
    >>> from nipype.interfaces import freesurfer
    >>> resampler = freesurfer.Resample()
    >>> resampler.inputs.in_file = '../../emptydata/structural.nii'
    >>> resampler.inputs.resampled_file = 'resampled.nii'
    >>> resampler.inputs.voxel_size = (2.1, 2.1, 2.1)
    >>> resampler.cmdline
    'mri_convert -vs 2.10 2.10 2.10 -i ../../emptydata/structural.nii -o resampled.nii'
    
    """

    _cmd = 'mri_convert'
    input_spec = ResampleInputSpec
    output_spec = ResampleOutputSpec

    def _get_outfilename(self):
        if isdefined(self.inputs.resampled_file):
            outfile = self.inputs.resampled_file
        else:
            outfile = fname_presuffix(self.inputs.in_file,
                                      newpath = os.getcwd(),
                                      suffix='_resample')
        return outfile
            
        
    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['resampled_file'] = self._get_outfilename()
        return outputs
    
    def _gen_filename(self, name):
        if name == 'resampled_file':
            return self._get_outfilename()
        return None

class ReconAllInputSpec(FSTraitedSpec):
    subject_id = traits.Str(argstr='-subjid %s', desc='subject name',
                            mandatory=True)
    directive = traits.Enum('all', 'autorecon1', 'autorecon2', 'autorecon2-cp',
                            'autorecon2-wm', 'autorecon2-inflate1', 'autorecon2-perhemi',
                            'autorecon3', argstr='-%s', desc='process directive',
                            mandatory=True)
    hemi = traits.Enum('lh', 'rh', desc='hemisphere to process')
    T1_files = InputMultiPath(File(exists=True), argstr='-i %s...',
                              desc='name of T1 file to process')
    subjects_dir = Directory(exists=True, argstr='-sd %s',
                             desc='path to subjects directory')
    flags = traits.Str(argstr='%s', desc='additional parameters')

class ReconAll(FSCommand):
    """Uses recon-all to generate surfaces and parcellations of structural data
    from anatomical images of a subject. 

    Examples
    --------
    
    >>> os.chdir( os.path.dirname( os.path.realpath( __file__ ) ) )
    >>> from nipype.interfaces.freesurfer import ReconAll
    >>> reconall = ReconAll()
    >>> reconall.inputs.subject_id = 'foo'
    >>> reconall.inputs.directive = 'all'
    >>> reconall.inputs.subjects_dir = '.'
    >>> reconall.inputs.T1_files = '../../emptydata/structural.nii'
    >>> reconall.cmdline
    'recon-all -i ../../emptydata/structural.nii -all -subjid foo -sd .'
    
    """

    _cmd = 'recon-all'
    input_spec = ReconAllInputSpec
    output_spec = FreeSurferSource.output_spec

    def _list_outputs(self):
        """
        See io.FreeSurferSource.outputs for the list of outputs returned
        """
        FreeSurferSource(subject_id=self.inputs.subject_id,
                         subjects_dir=self.inputs.subjects_dir)._outputs().get()

class BBRegisterInputSpec(FSTraitedSpec):
    subject_id = traits.Str(argstr='--s %s', desc='freesurfer subject id',
                            mandatory=True)
    source_file = File(argstr='--mov %s', desc='source file to be registered',
                      mandatory=True, copyfile=False)
    init = traits.Enum('spm', 'fsl', 'header', argstr='--init-%s',
                       xor=['init_reg_file'],
                       desc='initialize registration spm, fsl, header')
    init_reg_file = File(exists=True, desc='existing registration file',
                         xor=['init'],
                         mandatory=True)
    contrast_type = traits.Enum('t1', 't2', argstr='--%s',
                                desc='contrast type of image', mandatory=True)
    out_reg_file = File(argstr='--reg %s', desc='output registration file',
                      genfile=True)
    registered_file = traits.Either(traits.Bool, File, argstr='--o %s',
                            desc='output warped sourcefile either True or filename')

class BBRegisterOutputSpec(TraitedSpec):
    out_reg_file = File(exists=True, desc='Output registration file')
    registered_file = File(desc='Registered and resampled source file')

class BBRegister(FSCommand):
    """Use FreeSurfer bbregister to register a volume two a surface mesh

    This program performs within-subject, cross-modal registration using a
    boundary-based cost function. The registration is constrained to be 6
    DOF (rigid). It is required that you have an anatomical scan of the
    subject that has already been recon-all-ed using freesurfer.

    Examples
    --------
    
    >>> os.chdir( os.path.dirname( os.path.realpath( __file__ ) ) )
    >>> from nipype.interfaces.freesurfer import BBRegister
    >>> bbreg = BBRegister(subject_id='me', source_file='../../emptydata/structural.nii', init='header', contrast_type='t2')
    >>> bbreg.cmdline
    'bbregister --t2 --init-header --reg ../../emptydata/structural_bbreg_me.dat --mov ../../emptydata/structural.nii --s me'

    """

    _cmd = 'bbregister'
    input_spec = BBRegisterInputSpec
    output_spec =  BBRegisterOutputSpec
    
    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_reg_file'] = self.inputs.out_reg_file
        if not isdefined(self.inputs.out_reg_file) and self.inputs.source_file:
            outputs['out_reg_file'] = fname_presuffix(self.inputs.source_file,
                                         suffix='_bbreg_%s.dat'%self.inputs.subject_id,
                                         use_ext=False)
        if isdefined(self.inputs.registered_file):
            outputs['registered_file'] = self.inputs.registered_file
            if isinstance(self.inputs.registered_file, bool):
                outputs['registered_file'] = fname_presuffix(self.inputs.source_file,suffix='_bbreg')
        return outputs

    def _format_arg(self, name, spec, value):
        if name == 'registered_file':
            if isinstance(value, bool):
                fname = self._list_outputs()[name]
            else:
                fname = value
            return spec.argstr % fname
        return super(BBRegister, self)._format_arg(name, spec, value)
    
    def _gen_filename(self, name):
        if name == 'out_reg_file':
            return self._list_outputs()[name]
        return None    

class ApplyVolTransformInputSpec(FSTraitedSpec):
    source_file = File(exists = True, argstr = '--mov %s',
                      copyfile=False, mandatory = True,
                      desc = 'Input volume you wish to transform')
    transformed_file = File(desc = 'Output volume', argstr='--o %s', genfile=True)
    _targ_xor = ('target_file', 'tal', 'fs_target')
    target_file = File(exists = True, argstr = '--targ %s', xor=_targ_xor,
                      desc = 'Output template volume', mandatory=True)
    tal = traits.Bool(argstr='--tal', xor=_targ_xor, mandatory=True,
                      desc='map to a sub FOV of MNI305 (with --reg only)')
    fs_target = traits.Bool(argstr='--fstarg',xor=_targ_xor, mandatory=True,
                         requires=['reg_file'],
                         desc='use orig.mgz from subject in regfile as target')
    _reg_xor = ('reg_file', 'fsl_reg_file', 'xfm_reg_file', 'reg_header', 'subject')
    reg_file = File(exists=True, xor=_reg_xor, argstr='--reg %s',
                   mandatory=True,
                   desc= 'tkRAS-to-tkRAS matrix   (tkregister2 format)')
    fsl_reg_file = File(exists=True, xor=_reg_xor, argstr='--fsl %s',
                   mandatory=True,
                   desc= 'fslRAS-to-fslRAS matrix (FSL format)')
    xfm_reg_file = File(exists=True, xor=_reg_xor, argstr='--xfm %s',
                   mandatory=True,
                   desc= 'ScannerRAS-to-ScannerRAS matrix (MNI format)')
    reg_header = traits.Bool(xor=_reg_xor, argstr='--regheader',
                   mandatory=True,
                   desc= 'ScannerRAS-to-ScannerRAS matrix = identity')
    subject = traits.Str(xor=_reg_xor, argstr='--s %s',
                   mandatory=True,
                   desc= 'set matrix = identity and use subject for any templates')
    inverse = traits.Bool(desc = 'sample from target to source',
                          argstr = '--inv')
    interp = traits.Enum('trilin', 'nearest', argstr = '--interp %s',
                         desc = 'Interpolation method (<trilin> or nearest)')
    no_resample = traits.Bool(desc = 'Do not resample; just change vox2ras matrix',
                             argstr = '--no-resample')

class ApplyVolTransformOutputSpec(TraitedSpec):
    transformed_file = File(exists=True, desc = 'Path to output file if used normally')

class ApplyVolTransform(FSCommand):
    """Use FreeSurfer mri_vol2vol to apply a transform.

    Examples
    --------
    
    >>> os.chdir( os.path.dirname( os.path.realpath( __file__ ) ) )
    >>> from nipype.interfaces.freesurfer import ApplyVolTransform
    >>> applyreg = ApplyVolTransform()
    >>> applyreg.inputs.source_file = '../../emptydata/structural.nii'
    >>> applyreg.inputs.reg_file = '../../emptydata/register.dat'
    >>> applyreg.inputs.transformed_file = 'struct_warped.nii'
    >>> applyreg.inputs.fs_target = True
    >>> applyreg.cmdline
    'mri_vol2vol --fstarg --reg ../../emptydata/register.dat --mov ../../emptydata/structural.nii --o struct_warped.nii'

    """

    _cmd = 'mri_vol2vol'
    input_spec = ApplyVolTransformInputSpec
    output_spec = ApplyVolTransformOutputSpec

    def _get_outfile(self):
        outfile = self.inputs.transformed_file
        if not isdefined(outfile):
            if self.inputs.inverse == True:
                if self.inputs.fs_target == True:
                    src = 'orig.mgz'
                else:
                    src = self.inputs.target_file
            else:
                src = self.inputs.source_file
            outfile = fname_presuffix(src,
                                      newpath=os.getcwd(),
                                      suffix='_warped')
        return outfile

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['transformed_file'] = self._get_outfile()
        return outputs
    
    def _gen_filename(self, name):
        if name == 'transformed_file':
            return self._get_outfile()
        return None    

class SmoothInputSpec(FSTraitedSpec):
    in_file= File(exists=True, desc='source volume',
                     argstr='--i %s', mandatory=True)
    reg_file = File(desc='registers volume to surface anatomical ',
                   argstr='--reg %s', mandatory=True,
                   exists=True)
    smoothed_file = File(desc='output volume', argstr='--o %s', genfile=True)
    proj_frac_avg=traits.Tuple(traits.Float,traits.Float,traits.Float,
                               xor=['proj_frac'],
                              desc='average a long normal min max delta',
                              argstr='--projfrac-avg %.2f %.2f %.2f')
    proj_frac = traits.Float(desc='project frac of thickness a long surface normal',
                             xor=['proj_frac_avg'],
                             argstr='--projfrac %s')
    surface_fwhm = traits.Float(min=0, requires=['reg_file'],
                                mandatory=True, xor=['num_iters'],
                                desc='surface FWHM in mm', argstr='--fwhm %d')
    num_iters = traits.Int(min=1, xor=['surface_fwhm'],
                           mandatory=True,
                           desc='number of iterations instead of fwhm')
    vol_fwhm = traits.Float(min=0, argstr= '--vol-fwhm %d',
                            desc='volumesmoothing outside of surface')

class SmoothOutputSpec(FSTraitedSpec):
    smoothed_file= File(exist=True,desc='smoothed input volume')	
         
class Smooth(FSCommand):
    """Use FreeSurfer mris_volsmooth to smooth a volume

    This function smoothes cortical regions on a surface and non-cortical
    regions in volume.

    .. note::
       Cortical voxels are mapped to the surface (3D->2D) and then the
       smoothed values from the surface are put back into the volume to fill
       the cortical ribbon. If data is smoothed with this algorithm, one has to
       be careful about how further processing is interpreted.

    Examples
    --------

    >>> os.chdir( os.path.dirname( os.path.realpath( __file__ ) ) )
    >>> from nipype.interfaces.freesurfer import Smooth
    >>> smoothvol = Smooth(in_file='../../emptydata/functional.nii', smoothed_file = 'foo_out.nii', reg_file='../../emptydata/register.dat', surface_fwhm=10, vol_fwhm=6)
    >>> smoothvol.cmdline
    'mris_volsmooth --i ../../emptydata/functional.nii --reg ../../emptydata/register.dat --o foo_out.nii --fwhm 10 --vol-fwhm 6'
    
    """

    _cmd = 'mris_volsmooth'
    input_spec = SmoothInputSpec
    output_spec = SmoothOutputSpec

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outfile= self.inputs.smoothed_file
        if not isdefined(outfile):
            outfile = self._gen_fname(self.inputs.in_file,
                                      suffix = '_smooth')
        outputs['smoothed_file'] = outfile
        return outputs

    def _gen_filename(self, name):
        if name == 'smoothed_file':
            return self._list_outputs()[name]
        return None


"""
interfaces to do:

mri_vol2surf
mri_surf2vol
mri_surf2surf
mri_robust_register
mri_ms_fitparams
"""

