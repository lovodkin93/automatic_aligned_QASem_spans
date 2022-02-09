from qanom.nominalization_detector import NominalizationDetector
from allennlp.data.tokenizers.spacy_tokenizer import SpacyTokenizer
from utils import *
sys.path.append(EXTRA_SCRIPTS_DIR)
import QAnom_parsing
from pipeline import QASRL_Pipeline

def qanom_parse_all(helper_dir):

    QAnom_pipe = QASRL_Pipeline("kleinay/qanom-seq2seq-model-joint")
    detector = NominalizationDetector()
    word_tokenizer = SpacyTokenizer(language='en_core_web_sm', pos_tags=True)

    jsons_dir = os.path.join(helper_dir, "jsons_files")
    qas_dir = os.path.join(helper_dir, "QAs", "QANom")

    for root, subdirs, files in os.walk(jsons_dir):
        if files: # got to files rather than sub-directories
            # create folder if not existing
            path_components = get_path_components(helper_dir, root, 1, ["QAs", "QANom"])
            create_dir(path_components)

            curr_qas_dir = root.replace(jsons_dir, qas_dir)
            for file in files:
                json_file_path = os.path.join(root, file)
                qa_file_path = os.path.join(curr_qas_dir, file)

                if os.path.isfile(qa_file_path):
                    print(f"{file} json file with QAs already exist. skip parsing...")
                    continue

                QAnom_parsing.main(json_file_path, qa_file_path, QAnom_pipe, detector, word_tokenizer)



def main(args):
    indir = args.indir
    helper_dir = os.path.join(os.path.dirname(indir), HELPER_DIR_NAME)
    qanom_parse_all(helper_dir)
    print(f'done saving QA-Noms to json files, in {os.path.join(helper_dir, "QAs", "QANom")}')







if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description="")
    argparser.add_argument("-i", "--indir", required=True, help="path to train_full_details_with_oies_no_duplications.csv")
    main(argparser.parse_args())