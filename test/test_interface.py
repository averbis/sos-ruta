# Copyright 2021 Averbis GmbH
# This file is part of the sos-ruta project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file incorporates work covered by the following license notice:
#   Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
#   Distributed under the terms of the 3-clause BSD License.

from sos_notebook.test_utils import NotebookTest


class TestInterface(NotebookTest):

    def test_prompt_color(self, notebook):
        '''test color of input and output prompt'''
        idx = notebook.call(
            '''\
            DECLARE testVar;
            ''', kernel="UIMA Ruta")
        assert [0, 0, 0] == notebook.get_output_backgroundColor(idx)
