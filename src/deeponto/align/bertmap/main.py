# documentation
# https://krr-oxford.github.io/DeepOnto/bertmap/

from src.deeponto.onto import Ontology
from src.deeponto.align.bertmap import BERTMapPipeline, DEFAULT_CONFIG_FILE
from torch.cuda import is_available, get_device_name, current_device

print(is_available(), get_device_name(current_device()))

# Define ontologies
base = "bertmap data\\data_to_upload\\ontos\\"
# src_onto_path = base + "fma2nci.small.owl"
# tgt_onto_path = base + "nci2fma.small.owl"

src_onto_path = base + "EFS.owl"
tgt_onto_path = base + "FIBOLt.owl"


# Setup config
config = BERTMapPipeline.load_bertmap_config(DEFAULT_CONFIG_FILE)
config.tgt_onto_path = tgt_onto_path
config.output_path = "bertmap data\\"


# annotation properties
config.annotation_property_iris += [
    "https://www.omg.org/spec/Commons/AnnotationVocabulary/synonym",
    "https://www.omg.org/spec/Commons/AnnotationVocabulary/abbreviation",
    "https://www.omg.org/spec/Commons/AnnotationVocabulary/acronym"
]

config.additional_annotation_iris = [
    "http://www.w3.org/2004/02/skos/core#definition",
    "https://www.omg.org/spec/Commons/AnnotationVocabulary/explanatoryNote",
    "http://www.w3.org/2004/02/skos/core#example",
    "http://www.w3.org/2004/02/skos/core#note"
]


# training parameters
config.bert.pretrained_path = "yiyanghkust/finbert-pretrain"
config.batch_size_for_training = 128
config.batch_size_for_prediction = 64


config.number_raw_candidates = 400
config.global_matching.num_best_predictions = 15
config.global_matching.mapping_extension_threshold = 0.85
config.global_matching.mapping_filtered_threshold = 0.95

# config.bert.resume_training = False
print(config)

# Load Ontologies and run bertmap pipeline
src_onto = Ontology(src_onto_path, config.reasoner)
tgt_onto = Ontology(tgt_onto_path, config.reasoner)
BERTMapPipeline(src_onto, tgt_onto, config)
