from utils import *
sys.path.append(EXTRA_SCRIPTS_DIR)
import merge_qa_jsons

def qa_combine(helper_dir):

    qa_srl_dir = os.path.join(helper_dir, "QAs", "QASRL")
    qa_nom_dir = os.path.join(helper_dir, "QAs", "QANom")
    qa_combined_dir = os.path.join(helper_dir, "QAs", "combined")


    for root, subdirs, files in os.walk(qa_srl_dir):
        if files: # got to files rather than sub-directories
            # create folder if not existing
            path_components = get_path_components(helper_dir, root, 2, ["QAs", "combined"])
            create_dir(path_components)

            curr_qa_srl_dir = root
            curr_qa_nom_dir = root.replace(qa_srl_dir, qa_nom_dir)
            curr_qa_combined_dir = root.replace(qa_srl_dir, qa_combined_dir)

            for file in files:
                qa_srl_file_path = os.path.join(curr_qa_srl_dir, file)
                qa_nom_file_path = os.path.join(curr_qa_nom_dir, file)
                qa_combined_file_path = os.path.join(curr_qa_combined_dir, file)
                if os.path.isfile(qa_combined_file_path):
                    print(f'{"/".join(os.path.normpath(qa_combined_file_path).split(os.path.sep)[-4:])} already exists')
                    continue
                merge_qa_jsons.main([qa_srl_file_path, qa_nom_file_path], qa_combined_file_path)




def main(args):
    indir = args.indir

    helper_dir = os.path.join(os.path.dirname(indir), HELPER_DIR_NAME)
    qa_combine(helper_dir)
    print(f'done saving combined QA-SRLs and QA-Noms to json files, in {os.path.join(helper_dir, "QAs", "combined")}')







if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="")
    argparser.add_argument("-i", "--indir", required=True, help="path to train_full_details_with_oies_no_duplications.csv")
    main(argparser.parse_args())