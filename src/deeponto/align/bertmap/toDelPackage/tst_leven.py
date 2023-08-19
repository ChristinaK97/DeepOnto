import itertools
import re
from itertools import product

from thefuzz import fuzz
from thefuzz import process


def tleven(s1, s2):
    print(fuzz.ratio(s1, s2))
    print(fuzz.partial_ratio(s1, s2))
    print(fuzz.token_sort_ratio(s1, s2))
    print(fuzz.token_set_ratio(s1, s2))
    print(fuzz.partial_token_sort_ratio(s1, s2))
    print()


def leven(src_annotations, tgt_annotations):
    return max([fuzz.token_sort_ratio(s_ann, t_ann) for s_ann, t_ann in product(src_annotations, tgt_annotations)])


src = "account person type"
tgt1 = "demand deposit account"
tgt2 = "person"
tgt3 = "interest rate"
for s, t in itertools.product([src], [tgt1, tgt2, tgt3]):
    pass  # tleven(s, t)


def sort_scores(scores):
    def compare_candidates(candidate):
        score, length = candidate[1], candidate[2]
        return score, length

    sorted_scores = sorted(scores, key=compare_candidates, reverse=False)
    return sorted_scores


def rank_candidates(src_annots, tgt_candidates):
    def score_scr_tgt_pair(tgt, src_annots, tgt_annots):
        candidate_scores = []
        for src_annot, tgt_annot in itertools.product(src_annots, tgt_annots):
            tgt_tokens = re.findall(r'\w+', tgt_annot)
            pair_score = [tgt, len(tgt_tokens), len(tgt_tokens)]
            for token in tgt_tokens:
                partial_score = fuzz.partial_ratio(token, src_annot)
                if partial_score == 100:
                    pair_score[1] -= 1

            candidate_scores.append(pair_score)
        final_candidate_score = sort_scores(candidate_scores)[0]
        return final_candidate_score

    tgt = ""
    final_candidates_scores = [score_scr_tgt_pair(tgt, src_annots, tgt_annots) for tgt_annots in tgt_candidates]
    final_candidates_scores = sort_scores(final_candidates_scores)


src_annots = ['contribution interest rate']
tgt_annots = [['rate'], ['interest rate'], ['something else with interest rate'], ['base interest']]

# rank_candidates(src_annots, tgt_annots)

l = [[4, 1, 2], [6, 1, 1], [11, 1, 1], [2, 2, 3], [1, 2, 3], [8, 2, 2], [10, 2, 2], [7, 3, 3], [5, 3, 3], [0, 5, 5]]
print(sort_scores(l))

"""
       def get_low_score_candidates(self, src_class_iri,
                                tgt_class_candidates, final_best_scores, final_best_idxs,
                                k=10, high_thrs=0.45, perc_thrs=0.5):

       def leven(idx):
           src_annotations = self.src_annotation_index[src_class_iri]
           tgt_annotations = self.tgt_annotation_index[tgt_class_candidates[idx][0]]
           self.writelog(f"\n\t\t{tgt_class_candidates[idx][0]}") ; [self.writelog(f"\n\t\t{t_ann} : {fuzz.token_sort_ratio(s_ann,t_ann)}") for s_ann, t_ann in itertools.product(src_annotations, tgt_annotations)]
           return max([fuzz.token_sort_ratio(s_ann, t_ann) for s_ann, t_ann in
                       itertools.product(src_annotations, tgt_annotations)])

       self.writelog(f"\n\tGET LOW SCORE CAND FOR {src_class_iri}\n")
       if final_best_scores[0] == -1:
           self.writelog("\n\tAll scores are -1\n")
           return


       final_best_scores = final_best_scores[:k]
       final_best_idxs = [idx.item() for idx in final_best_idxs[:k]]
       best_bert_score = final_best_scores[0]
       max_leven = leven(final_best_idxs[0])
       topToKeep = [(final_best_idxs[0], best_bert_score, max_leven)]

       for idx, cand_score in zip(final_best_idxs[1:], final_best_scores[1:]):
           if cand_score == -1:
               break
           percentage_diff = abs((cand_score - best_bert_score) / best_bert_score)
           cand_leven = leven(idx)

           if percentage_diff < perc_thrs or max_leven < cand_leven:
               topToKeep.append((idx, cand_score, cand_leven))
               max_leven = max(max_leven, cand_leven)


       bert_matched_mappings = []
       self.writelog("\n")
       for candidate_idx, mapping_score, _leven in topToKeep:
           self.writelog(f"\t\t{candidate_idx} score = {mapping_score}, {_leven}\t cand = {tgt_class_candidates[candidate_idx][0]}\n")
           tgt_candidate_iri = tgt_class_candidates[candidate_idx][0]
           bert_matched_mappings.append(
               self.init_class_mapping(
                   src_class_iri,
                   tgt_candidate_iri,
                   mapping_score.item(),
               )
           )
   """
