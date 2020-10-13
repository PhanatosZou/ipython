# -*- coding: utf-8 -*-
"""Test suite for the deepreload module."""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from pathlib import Path

import nose.tools as nt

from IPython.utils.syspathcontext import prepended_to_syspath
from IPython.utils.tempdir import TemporaryDirectory
from IPython.lib.deepreload import reload as dreload


def test_deepreload():
    "Test that dreload does deep reloads and skips excluded modules."
    with TemporaryDirectory() as tmpdir:
        with prepended_to_syspath(tmpdir):
            tmpdirpath = Path(tmpdir)
            Path(os.path.join(tmpdirpath, "A.py")).write_text("class Object(object):\n    pass\n")
            Path(os.path.join(tmpdirpath, "B.py")).write_text("import A\n")
            import A
            import B

            # Test that A is not reloaded.
            obj = A.Object()
            dreload(B, exclude=["A"])
            nt.assert_true(isinstance(obj, A.Object))

            # Test that A is reloaded.
            obj = A.Object()
            dreload(B)
            nt.assert_false(isinstance(obj, A.Object))
