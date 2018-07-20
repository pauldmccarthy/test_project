#!/usr/bin/env python
#

import os
import shutil
import tempfile
import os.path as op

import nibabel as nib
import numpy as np


def make_dummy_file(path, contents=None):
    """Makes a plain text file. Returns a hash of the file contents. """
    dirname = op.dirname(path)

    if not op.exists(dirname):
        os.makedirs(dirname)

    if contents is None:
        contents = '{}\n'.format(op.basename(path))
    with open(path, 'wt') as f:
        f.write(contents)

    return hash(contents)


def make_dummy_files(paths):
    """Creates dummy files for all of the given paths. """
    for p in paths:
        make_dummy_file(p)


def testdir(contents=None, suffix=""):
    """Returnsa context manager which creates, changes to, and returns a
    temporary directory, and then deletes it on exit.
    """

    if contents is not None:
        contents = [op.join(*c.split('/')) for c in contents]

    class ctx(object):

        def __init__(self, contents):
            self.contents = contents

        def __enter__(self):

            self.testdir = tempfile.mkdtemp(suffix=suffix)
            self.prevdir = os.getcwd()

            os.chdir(self.testdir)

            if self.contents is not None:
                contents = [op.join(self.testdir, c) for c in self.contents]
                make_dummy_files(contents)

            return self.testdir

        def __exit__(self, *a, **kwa):
            os.chdir(self.prevdir)
            shutil.rmtree(self.testdir)

    return ctx(contents)


def make_random_image(filename=None,
                      dims=(10, 10, 10),
                      xform=None,
                      imgtype=1,
                      pixdims=None,
                      dtype=np.float32):
    """Convenience function which makes an image containing random data.
    Saves and returns the nibabel object.

    imgtype == 0: ANALYZE
    imgtype == 1: NIFTI1
    imgtype == 2: NIFTI2
    """

    if   imgtype == 0: hdr = nib.AnalyzeHeader()
    elif imgtype == 1: hdr = nib.Nifti1Header()
    elif imgtype == 2: hdr = nib.Nifti2Header()

    if pixdims is None:
        pixdims = [1] * len(dims)

    pixdims = pixdims[:len(dims)]
    zooms   = [abs(p) for p in pixdims]

    hdr.set_data_dtype(dtype)
    hdr.set_data_shape(dims)
    hdr.set_zooms(zooms)

    if xform is None:
        xform = np.eye(4)
        for i, p in enumerate(pixdims[:3]):
            xform[i, i] = p

    data  = np.array(np.random.random(dims) * 100, dtype=dtype)

    if   imgtype == 0: img = nib.AnalyzeImage(data, xform, hdr)
    elif imgtype == 1: img = nib.Nifti1Image( data, xform, hdr)
    elif imgtype == 2: img = nib.Nifti2Image( data, xform, hdr)

    if filename is not None:

        if op.splitext(filename)[1] == '':
            if imgtype == 0: filename = '{}.img'.format(filename)
            else:            filename = '{}.nii'.format(filename)

        nib.save(img, filename)

    return img
