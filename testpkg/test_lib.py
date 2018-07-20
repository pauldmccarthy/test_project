#!/usr/bin/env python


import os
import os.path as op

from . import lib

import fsl.data.image as fslimage


def _test_thing():

    with lib.testdir() as testdir:

        dims = [(10, 10, 10),
                (15, 15, 15),
                (20, 20, 20)]

        fname = op.join(testdir, 'tensor_image.nii')

        for i, d in enumerate(dims):

            print('{}: {} - {}'.format(i, testdir, os.listdir(testdir)))


            lib.make_random_image(fname, dims=d)
            img = fslimage.Image(fname)
            assert tuple(img.shape) == dims



def test_01(): _test_thing()
def test_02(): _test_thing()
def test_03(): _test_thing()
def test_04(): _test_thing()
def test_05(): _test_thing()
def test_06(): _test_thing()
def test_07(): _test_thing()
def test_08(): _test_thing()
def test_09(): _test_thing()
def test_10(): _test_thing()
def test_11(): _test_thing()
def test_12(): _test_thing()
def test_13(): _test_thing()
