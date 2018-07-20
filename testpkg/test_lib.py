#!/usr/bin/env python


import os.path as op

from . import lib


def test_thing():

    with lib.testdir() as testdir:

        fname = op.join(testdir, 'tensor_image.nii')

        lib.make_random_image(fname, dims=(10, 10, 10))
