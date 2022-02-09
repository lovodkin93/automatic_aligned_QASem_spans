from utils import *


def ensure_no_dups(curr_filtered_df, isDoc, file_name):
    if isDoc and (len(set(curr_filtered_df.database)) > 1 or len(set(curr_filtered_df.topic)) > 1):
        print(f"Document {file_name} is associated to more than one topic/database")
        exit()
    if not isDoc and len(set(curr_filtered_df.database)) > 1:
        print(f"topic {file_name} is associated to more than one database")
        exit()


def save_json_file(df, helper_dir, isDoc):

    file_name_col = 'documentFile' if isDoc else "topic"
    sent_ind_col = 'docSentCharIdx' if isDoc else "scuSentCharIdx"

    filtered_df = df.drop_duplicates(subset=[file_name_col, sent_ind_col])

    for file_name in set(filtered_df[file_name_col]):
        curr_filtered_df = filtered_df.loc[filtered_df[file_name_col] == file_name]
        curr_filtered_df = curr_filtered_df.sort_values(by=[sent_ind_col])
        ensure_no_dups(curr_filtered_df, isDoc, file_name)

        database = str(int(list(curr_filtered_df.database)[0]))
        topic = list(curr_filtered_df.topic)[0]


        if isDoc:
            create_dir([helper_dir, "jsons_files", "documents", database, topic])
            out_json_file = os.path.join(helper_dir, "jsons_files", "documents", database, topic, f"{file_name}.json")
        else:
            create_dir([helper_dir, "jsons_files", "summaries", database])
            out_json_file = os.path.join(helper_dir, "jsons_files", "summaries", database, f"{file_name}.json")

        with open(out_json_file, 'w') as fp:
            num_row = curr_filtered_df.shape[0]
            for i, row in curr_filtered_df.iterrows():
                curr_sent = row["docSentText"] if isDoc else row["scuSentence"]
                curr_sent_ind = row[sent_ind_col]
                json.dump({"sentence": curr_sent, "sent_index": curr_sent_ind}, fp)
                if i != num_row - 1:
                    fp.write("\n")


def save_json_file_wrapper(df, helper_dir):
    save_json_file(df, helper_dir, True) # documents
    save_json_file(df, helper_dir, False) # summaries


def main(args):
    indir = args.indir

    helper_dir = os.path.join(os.path.dirname(indir), HELPER_DIR_NAME)


    df =  pd.read_csv(indir)
    save_json_file_wrapper(df, helper_dir)
    print(f'done saving sentences to json files in {os.path.join(helper_dir, "QAs", "combined")}')







if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="")
    argparser.add_argument("-i", "--indir", required=True, help="path to train_full_details_with_oies_no_duplications.csv")
    main(argparser.parse_args())