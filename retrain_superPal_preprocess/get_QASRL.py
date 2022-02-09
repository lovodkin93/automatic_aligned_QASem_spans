import sys
import os
sys.path.append(os.path.dirname(sys.argv[0])) # add directory where the script is (so can import from utils.py)
sys.path.append(os.getcwd()) # make sure working dir is the directory where the nrl-qasrl project is
import qa_srl_debugger
from utils import *


def qasrl_parse_all(helper_dir):
    jsons_dir = os.path.join(helper_dir, "jsons_files")
    qas_dir = os.path.join(helper_dir, "QAs", "QASRL")

    for root, subdirs, files in os.walk(jsons_dir):
        if files: # got to files rather than sub-directories
            # create folder if not existing
            path_components = get_path_components(helper_dir, root, 1, ["QAs", "QASRL"])
            create_dir(path_components)

            curr_qas_dir = root.replace(jsons_dir, qas_dir)
            for file in files:
                json_file_path = os.path.join(root, file)
                qa_file_path = os.path.join(curr_qas_dir, file)

                if os.path.isfile(qa_file_path):
                    print(f"{file} json file with QAs already exist. skip parsing...")
                    continue

                qa_srl_debugger.qa_parse(json_file_path, qa_file_path, isJson=True)



def main(args):
    print("WARNING: make sure working directory is where the nrl-qasrl project is")
    indir = args.indir
    helper_dir = os.path.join(os.path.dirname(indir), HELPER_DIR_NAME)
    qasrl_parse_all(helper_dir)
    print(f'done saving QA-SRLs to json files, in {os.path.join(helper_dir, "QAs", "QASRL")}')







if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description="")
    argparser.add_argument("-i", "--indir", required=True, help="path to train_full_details_with_oies_no_duplications.csv")
    main(argparser.parse_args())