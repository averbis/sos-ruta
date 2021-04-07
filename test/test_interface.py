# Original work: Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Modified work: Copyright 2021 Averbis GmbH
# Distributed under the terms of the 3-clause BSD License.

from sos_notebook.test_utils import NotebookTest


class TestInterface(NotebookTest):

    def test_prompt_color(self, notebook):
        '''test color of input and output prompt'''
        idx = notebook.call(
            '''\
            DECLARE testVar;
            ''', kernel="UIMA Ruta")
        assert [0, 0, 0] == notebook.get_output_backgroundColor(idx)
