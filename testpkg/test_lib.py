#!/usr/bin/env python


import os.path as op

from . import lib


def test_thing():

    with lib.testdir() as testdir:

        dims = [(10, 10, 10),
                (15, 15, 15),
                (20, 20, 20)]

        fname = op.join(testdir, 'tensor_image.nii')

        for d in dims:
            lib.make_random_image(fname, dims=d)
