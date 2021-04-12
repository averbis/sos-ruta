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

import os
import tempfile

import cassis
from sos.utils import short_repr, env

RUTA_KERNEL_NAME = "UIMA Ruta"
SOS_KERNEL_NAME = "SoS"


class sos_Ruta:
    supported_kernels = {RUTA_KERNEL_NAME: [RUTA_KERNEL_NAME]}
    background_color = {RUTA_KERNEL_NAME: '#E6EEFF'}
    options = {}

    def __init__(self, sos_kernel, kernel_name=RUTA_KERNEL_NAME):
        self.ruta_kernel = sos_kernel
        self.kernel_name = kernel_name
        self.init_statements = ''

    def get_vars(self, var_names):
        """
        Functionality to transfer CAS objects and TypeSystem from SoS (python) kernel to the IRuta kernel.
        This function is called when a use invokes the line magic %get or %with.
        """
        if len(var_names) != 1:
            raise Exception("%get takes exactly one variable name as argument."
                            "If you want to transfer multiple CAS, then please write them to a directory and use `%inputDir` in IRuta kernel.")
        var_name = var_names[0]
        var_content = env.sos_dict[var_name]

        # Step 1: Writing Cas and TypeSystem to disk using dkpro-cassis
        temp_directory = tempfile.TemporaryDirectory()
        temp_typesystem_file = tempfile.NamedTemporaryFile(suffix=".xml", dir=temp_directory.name, delete=False)
        temp_typesystem_file_path = os.path.normpath(temp_typesystem_file.name).replace('\\', "/")
        temp_xmi_file = tempfile.NamedTemporaryFile(suffix=".xmi", dir=temp_directory.name, delete=False)
        temp_xmi_file_path = os.path.normpath(temp_xmi_file.name).replace('\\', "/")

        if isinstance(var_content, cassis.Cas):
            var_content.to_xmi(temp_xmi_file_path)
            var_content.typesystem.to_xml(temp_typesystem_file_path)
            cmd_transfer_var = "%displayMode NONE\n" \
                               f"%loadCas {temp_xmi_file_path}\n" \
                               f"%loadTypeSystem {temp_typesystem_file_path}"

        elif isinstance(var_content, cassis.TypeSystem):
            var_content.to_xml(temp_typesystem_file_path)
            cmd_transfer_var = "%displayMode NONE\n" \
                               f"%loadTypeSystem {temp_typesystem_file_path}"

        else:
            raise Exception(
                '%get only support transfering UIMA CAS objects or TypeSystem objects. '
                'Use %expand for transfering string variables. Received datatype {}'.format(short_repr(var_content)))

        # Step 2: Loading files
        env.log_to_file('KERNEL', f'Executing "{cmd_transfer_var}"')
        self.ruta_kernel.run_cell(
            cmd_transfer_var,
            silent=True,
            store_history=False,
            on_error=f'Failed to get variable {var_name}')

        # Step 3: Clean-up temp files
        temp_typesystem_file.close()
        temp_xmi_file.close()
        temp_directory.cleanup()

    def put_vars(self, items, to_kernel=None):
        """
        Functionality to transfer CAS objects from the IRuta kernel to the SoS (Python) kernel.
        This function is called when a user invokes the line magic %put or %with.
        """

        if len(items) != 1:
            raise Exception("%put takes exactly one variable name as argument. ")
        var_name = items[0]

        temp_directory = tempfile.TemporaryDirectory()
        temp_typesystem_file = tempfile.NamedTemporaryFile(suffix=".xml", dir=temp_directory.name, delete=False)
        temp_typesystem_file_path = os.path.normpath(temp_typesystem_file.name).replace('\\', "/")
        temp_xmi_file = tempfile.NamedTemporaryFile(suffix=".xmi", dir=temp_directory.name, delete=False)
        temp_xmi_file_path = os.path.normpath(temp_xmi_file.name).replace('\\', "/")

        # Step 1: Writing CAS and TypeSystem to disk with Ruta
        cmd_transfer_var = f"%displayMode NONE\n" \
                           f"%saveTypeSystem {temp_typesystem_file_path}\n" \
                           f"%saveCas {temp_xmi_file_path}"

        env.log_to_file('KERNEL', f'Executing "{cmd_transfer_var}"')
        self.ruta_kernel.run_cell(cmd_transfer_var, silent=True, store_history=False,
                                  on_error='Failed to write UIMA CAS to disk.')

        # Step 2: Reading CAS and TypeSystem from disk with python/cassis
        typesystem = cassis.load_typesystem(temp_typesystem_file)
        cas = cassis.load_cas_from_xmi(temp_xmi_file, typesystem=typesystem)

        # Step 3: Clean-up temp files
        temp_typesystem_file.close()
        temp_xmi_file.close()
        temp_directory.cleanup()

        return {var_name: cas}
