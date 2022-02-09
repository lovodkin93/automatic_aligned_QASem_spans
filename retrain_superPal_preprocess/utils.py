import os
import sys
import json
import pandas as pd
import argparse


HELPER_DIR_NAME = "train_full_details_with_QASem_helper"
EXTRA_SCRIPTS_DIR = r'C:\Users\aviv\Dropbox\My PC (DESKTOP-L80CN5A)\Desktop\studies\sandbox\ConSum_dataset_pipeline'


def create_dir(path_parts_list):
    """
    :param path_parts_list: a list of the parts of the path in order (e.g. ['/home/QAs', 'global', 'documents', 'duc2001', 'A1', 'doc1.json'] that corresponds to the path '/home/QAs/global/documents/duc2001/A1/doc1.json'
    :return: None
    """
    path_prefix = path_parts_list[0]
    if not os.path.exists(path_prefix):
        os.mkdir(path_prefix)
    for path_part in path_parts_list:
        path_prefix = os.path.join(path_prefix, path_part)
        if not os.path.exists(path_prefix):
            os.mkdir(path_prefix)

def get_path_components(helper_dir, root, replace_num, extra_components):
    """
    :function:
    separates path to its subdirectories and sends them as a list to the create_dir function
    :params:
    helper_dir - path/to/helper_dir
    root - path/to/directory_with_files
    replace_num - number of first components inside helper_dir to be replaced
    extra_components - list of extra components (to come instead of the replace_num first components inside helper_dir
                        (e.g. replace "jsons" with "QAs/QASRL" so replace_num=1 and extra_components = ["QAs", "QASRL"]
    :return: list of path components
    """
    normalized_path = os.path.normpath(root.replace(helper_dir, ""))
    path_components = normalized_path.split(os.sep)
    path_components = list(filter(None, path_components))
    path_components = [helper_dir] + extra_components + path_components[replace_num:]
    return path_components