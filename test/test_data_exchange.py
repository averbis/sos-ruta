# Original work: Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Modified work: Copyright 2021 Averbis GmbH
# Distributed under the terms of the 3-clause BSD License.

import os
import pathlib

import cassis
from sos_notebook.test_utils import NotebookTest

from sos_ruta.kernel import SOS_KERNEL_NAME, RUTA_KERNEL_NAME

TEST_RESOURCE_DIR = os.path.join(pathlib.Path(__file__).parent, "resources")


class TestDataExchange(NotebookTest):
    def test_send_single_cas_from_python_to_ruta(self, notebook):
        # Step 1: Get the file paths
        typesytem_file = os.path.join(TEST_RESOURCE_DIR, "TypeSystem.xml")
        cas_file = os.path.join(TEST_RESOURCE_DIR, "example.xmi")

        # Step 2: Get a (local) python instance of the cas for comparison
        with open(typesytem_file, 'rb') as f:
            typesystem = cassis.load_typesystem(f)
        with open(cas_file, 'rb') as f:
            cas = cassis.load_cas_from_xmi(f, typesystem=typesystem)

        # Step 3: Send a command to a SoS notebook cell that is loading the cas in that cell in a notebook
        cas_init_expr = f"""
        import cassis
        with open("{typesytem_file}", 'rb') as f:
            typesystem = cassis.load_typesystem(f)
        with open("{cas_file}", 'rb') as f:
            cas_var = cassis.load_cas_from_xmi(f, typesystem=typesystem)
        """

        notebook.call(cas_init_expr, kernel=SOS_KERNEL_NAME)

        # Step 4: Execute `%get cas` command in a Ruta cell and capture the return.
        notebook.call("%get cas_var", kernel=RUTA_KERNEL_NAME)
        actual_sofa = notebook.check_output("%displayMode RUTA_COLORING", kernel=RUTA_KERNEL_NAME)

        expected_sofa = cas.sofa_string

        # Step 5: Compare results. Ignore special characters.
        assert [c for c in actual_sofa if c.isalpha()] == [c for c in expected_sofa if c.isalpha()]

    def test_send_typesystem_from_python_to_ruta(self, notebook):
        # Step 1: Get the file paths
        typesytem_file = os.path.join(TEST_RESOURCE_DIR, "TypeSystem.xml")

        # Step 2: Send a command to a SoS notebook cell that is loading the cas in that cell in a notebook
        cas_init_expr = f"""
        import cassis
        with open("{typesytem_file}", 'rb') as f:
            typesystem = cassis.load_typesystem(f)
        """

        notebook.call(cas_init_expr, kernel=SOS_KERNEL_NAME)

        # Step 3: Execute `%get typesystem` command in a Ruta cell and capture the return.
        notebook.call("%get typesystem", kernel=RUTA_KERNEL_NAME)

        # Step 4: We check that using the typesystem does not throw an error
        notebook.call("%documentText 'Hello World'", kernel=RUTA_KERNEL_NAME)
        notebook.call('"Hello" -> Diagnosis;', kernel=RUTA_KERNEL_NAME)

    def test_send_single_cas_from_ruta_to_python(self, notebook):
        # Step 1: Get the file paths
        typesystem_file = os.path.join(TEST_RESOURCE_DIR, "TypeSystem.xml")
        cas_file = os.path.join(TEST_RESOURCE_DIR, "example.xmi")

        # Step 2: Get a (local) python instance of the cas for comparison
        with open(typesystem_file, 'rb') as f:
            typesystem = cassis.load_typesystem(f)
        with open(cas_file, 'rb') as f:
            cas = cassis.load_cas_from_xmi(f, typesystem=typesystem)

        # Step 3: Load CAS into Ruta
        cas_init_expr = f"%displayMode NONE\n" \
                        f"%loadCas {cas_file}\n" \
                        f"%loadTypeSystem {typesystem_file}"
        notebook.call(cas_init_expr, kernel=RUTA_KERNEL_NAME)

        # Step 4: Send files to SoS Kernel with %put
        notebook.call("%put modified_cas", kernel=RUTA_KERNEL_NAME)

        # Step 5: Check variable content
        actual_sofa = notebook.check_output("print(modified_cas.sofa_string)", kernel=SOS_KERNEL_NAME)
        expected_sofa = cas.sofa_string.strip()
        assert actual_sofa == expected_sofa
