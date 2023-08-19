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
    pass # tleven(s, t)


def sort_scores(scores):
    def compare_candidates(candidate):
        score, length = candidate[1], candidate[2]
        return -score, length

    sorted_scores = sorted(scores, key=compare_candidates, reverse=True)
    return sorted_scores


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

def rank_candidates(src_annots, tgt_candidates):
    tgt = ""
    final_candidates_scores = [score_scr_tgt_pair(tgt, src_annots, tgt_annots) for tgt_annots in tgt_candidates]
    print(final_candidates_scores)
    final_candidates_scores = sort_scores(final_candidates_scores)
    print(final_candidates_scores)

src_annots = ['contribution interest rate']
tgt_annots = [['rate'], ['interest rate'], ['something else with interest rate'], ['base interest']]

rank_candidates(src_annots, tgt_annots)

















