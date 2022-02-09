from utils import *
sys.path.append(EXTRA_SCRIPTS_DIR)
import QASem_to_spans

def get_spans(helper_dir):
    pass

def main(args):
    indir = args.indir
    helper_dir = os.path.join(os.path.dirname(indir), HELPER_DIR_NAME)
    QASem_to_spans.main(os.path.join(helper_dir, "QAs", "combined"), os.path.join(helper_dir, "all_span_combinations.csv"), True)



if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="")
    argparser.add_argument("-i", "--indir", required=True, help="path to train_full_details_with_oies_no_duplications.csv")
    main(argparser.parse_args())