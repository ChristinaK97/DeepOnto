from src.deeponto.onto import Ontology
from src.deeponto.align.bertmap import BERTMapPipeline, DEFAULT_CONFIG_FILE
from torch.cuda import is_available, get_device_name, current_device

print(is_available(), get_device_name(current_device()))

# documentation
# https://krr-oxford.github.io/DeepOnto/bertmap/

base = "C:\\Users\\christina\\Desktop\\Workspace\\alignment_tools\\bert_map\\bertmap data\\data_to_upload\\ontos\\"
# config_file = "path_to_config.yaml"
# src_onto_file = base + "fma2nci.small.owl"
# tgt_onto_file = base + "nci2fma.small.owl"

src_onto_file = base + "EFS.owl"
tgt_onto_file = base + "FIBOLt.owl"

config = BERTMapPipeline.load_bertmap_config(DEFAULT_CONFIG_FILE)
config.output_path = "C:\\Users\\christina\\Desktop\\Workspace\\alignment_tools\\bert_map\\bertmap data\\"
config.batch_size_for_training = 128
config.batch_size_for_prediction = 64


config.annotation_property_iris += [
    "https://www.omg.org/spec/Commons/AnnotationVocabulary/synonym",
    "https://www.omg.org/spec/Commons/AnnotationVocabulary/abbreviation",
    "https://www.omg.org/spec/Commons/AnnotationVocabulary/acronym"
]
config.bert.resume_training = False

config.bert.pretrained_path = "yiyanghkust/finbert-pretrain"
config.global_matching.mapping_filtered_threshold = 0.87
config.global_matching.mapping_extension_threshold = 0.85

print(config)

src_onto = Ontology(src_onto_file)
tgt_onto = Ontology(tgt_onto_file)
BERTMapPipeline(src_onto, tgt_onto, config)
