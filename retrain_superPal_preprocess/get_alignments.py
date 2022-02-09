from utils import *
from tqdm import tqdm
JACCARD_THR = 0.35


def span2indice(span, SentCharIdx):
    indice = []
    sub_spans = span.split(';')
    for sub_span in sub_spans:
        lims = [int(elem) - SentCharIdx for elem in sub_span.split(',')]
        indice += list(range(lims[0], lims[1]))
    return set(indice)


def calc_jaccard(row1, row2, isDoc):
    span1 = row1["docSpanOffsets"] if isDoc else row1["summarySpanOffsets"]
    span2 = row2["docSpanOffsets"] if isDoc else row2["summarySpanOffsets"]
    SentCharIdx1 = row1["docSentCharIdx"] if isDoc else row1["scuSentCharIdx"]
    SentCharIdx2 = row2["docSentCharIdx"] if isDoc else row2["scuSentCharIdx"]

    indice1 = span2indice(span1, SentCharIdx1)
    indice2 = span2indice(span2, SentCharIdx2)

    union_list = list(set.union(indice1,indice2))
    intersection_list = list(set.intersection(indice1,indice2))
    return float(len(intersection_list)) / float(len(union_list))

def get_final_df_row(QASem_row, pyramid_row, doc_jaccard, summary_jaccard):
    new_row = {"database": pyramid_row["database"],
               "topic": pyramid_row["topic"],
               "scuSentCharIdx": pyramid_row["scuSentCharIdx"],
               "scuSentence": pyramid_row["scuSentence"],
               "documentFile": pyramid_row["documentFile"],
               "docSentCharIdx": pyramid_row["docSentCharIdx"],
               "docSentText": pyramid_row["docSentText"],
               "docSpanOieOffsets": QASem_row["docSpanOffsets"],
               "docSpanOffsets": pyramid_row["docSpanOffsets"],
               "docSpanOieText": QASem_row["docSpanText"],
               "docSpanText": pyramid_row["docSpanText"],
               "summarySpanOieOffsets": QASem_row["summarySpanOffsets"],
               "summarySpanOffsets": pyramid_row["summarySpanOffsets"],
               "summarySpanOieText": QASem_row["summarySpanText"],
               "summarySpanText": pyramid_row["summarySpanText"],
                "docSpanJaccard": str(doc_jaccard),
                "summarySpanJaccard": str(summary_jaccard)}
    return new_row



def get_alignments_df(all_QASem_spans_df, aligned_pyramid_spans):
    final_df = pd.DataFrame(
        columns=["database", "topic", "scuSentCharIdx", "scuSentence", "documentFile", "docSentCharIdx", "docSentText", "docSpanOieOffsets",
                 "docSpanOffsets", "docSpanOieText", "docSpanText", "summarySpanOieOffsets", "summarySpanOffsets", "summarySpanOieText",
                 "summarySpanText", "docSpanJaccard", "summarySpanJaccard", "scuLabel"])

    pbar = tqdm(total=all_QASem_spans_df.shape[0], unit="QASem span pairs")
    for i, row in all_QASem_spans_df.iterrows():
        curr_aligned_pyramid_spans = aligned_pyramid_spans.loc[(aligned_pyramid_spans["topic"] == row["topic"]) &
                                                               (aligned_pyramid_spans["documentFile"] == row["documentFile"]) &
                                                               (aligned_pyramid_spans["scuSentCharIdx"] == row["scuSentCharIdx"]) &
                                                               (aligned_pyramid_spans["docSentCharIdx"] == row["docSentCharIdx"])]
        if curr_aligned_pyramid_spans.shape[0]>0: # not an empty df
            for j, p_row in curr_aligned_pyramid_spans.iterrows():
                doc_span_jaccard = calc_jaccard(row, p_row, True)
                summary_span_jaccard = calc_jaccard(row, p_row, False)
                if doc_span_jaccard > JACCARD_THR and summary_span_jaccard > JACCARD_THR:
                    final_df = final_df.append(get_final_df_row(row, p_row, doc_span_jaccard, summary_span_jaccard), ignore_index=True) # AVIVSL: change ignore_index to False?
        pbar.update(1)
    pbar.close()
    final_df =  final_df.drop_duplicates(subset=["database", "topic", "scuSentCharIdx",
                                                "scuSentence", "documentFile", "docSentCharIdx",
                                                "docSentText", "docSpanOieOffsets", "docSpanOieText",
                                                "summarySpanOieOffsets", "summarySpanOieText"]) # remove QASem spans duplicates
    return final_df

def main(args):
    indir = args.indir
    outdir = args.outdir

    aligned_pyramid_spans = pd.read_csv(indir)
    aligned_pyramid_spans = aligned_pyramid_spans.drop_duplicates(subset=["database", "topic", "scuSentCharIdx",
                                                                    "scuSentence", "documentFile", "docSentCharIdx",
                                                                    "docSentText", "docSpanOffsets", "docSpanText",
                                                                          "summarySpanOffsets", "summarySpanText"]) # remove pyramid spans duplicates (caused by intersections of the spans with more than one set of doc-summary oie spans)

    databases = list(set(aligned_pyramid_spans.database))
    for db in databases:
        all_QASem_spans_file = os.path.join(os.path.dirname(indir), HELPER_DIR_NAME, f"all_span_combinations_{db}.csv")
        all_QASem_spans_df = pd.read_csv(all_QASem_spans_file)

        print(f"start {db}")
        final_df = get_alignments_df(all_QASem_spans_df, aligned_pyramid_spans)

        curr_outdir = os.path.join(outdir, f"QAsem_aligned_spans_{db}.csv")
        final_df.to_csv(curr_outdir, index=True)
        print(f"done {db}")







if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="")
    argparser.add_argument("-i", "--indir", required=True, help="path to train_full_details_with_oies_no_duplications.csv")
    argparser.add_argument("-o", "--outdir", required=True, help="path to where to save the aligned spans")
    main(argparser.parse_args())