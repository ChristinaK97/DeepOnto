import re
import string

import nltk
from nltk.corpus import stopwords
from rdflib import Graph
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class ThesaurusCorpus:

    def __init__(self, ontologyPath, allAnnotProperties):
        print("Build WordNet Corpus for", ontologyPath)
        self.annotProperties = allAnnotProperties
        self.stopwordsList = set(stopwords.words('english'))
        self.corpus = self.findSynAndAntonyms(
                            self.extractOntologyTokens(ontologyPath))
        print("WordNet corpus size =", len(self.corpus))



    def extractOntologyTokens(self, ontologyPath):
        g = Graph()
        g.parse(source=ontologyPath, format="application/rdf+xml")

        query = """
            SELECT ?annot
            WHERE {
                ?subject ?predicate ?annot .
                FILTER (?predicate IN (%s))
            }
        """ % ", ".join(f"<{prop}>" for prop in self.annotProperties)

        # Execute the query and get the results
        results = g.query(query)
        print("# annotation triples =", len(results))

        ontologyTokens = set()
        for annotation in results:
            ontologyTokens.update(self.getAnnotationToken(annotation[0]))

        print("# ontology tokens = ", len(ontologyTokens))
        return ontologyTokens


    def getAnnotationToken(self, annotation):
        return {
            self.rmvPunct(token.lower()) for token in word_tokenize(annotation) if token
                  not in string.punctuation and
                  not re.match(r'\d+', token) and
                  token.lower() not in self.stopwordsList
        }


    def findSynAndAntonyms(self, ontologyTokens):

        corpus = []

        for token in ontologyTokens:
            # print(token)
            tokenSynonyms, tokenAntonyms = set(), set()

            for syn in wordnet.synsets(token):
                for lemma in syn.lemmas():

                    name = lemma.name().lower()
                    if name != token:
                        tokenSynonyms.add(self.rmvPunct(name))

                    if lemma.antonyms():
                        tokenAntonyms.add(self.rmvPunct(lemma.antonyms()[0].name().lower()))

            # print("Syn", tokenSynonyms, "\nAnt", tokenAntonyms, "\n")

            for nameSet, label in ((tokenSynonyms, 1), (tokenAntonyms, 0)):
                for el in nameSet:
                    corpus.append([token, el, label])

        return corpus


    def rmvPunct(self, name):
        return re.sub(r"['/_-]", ' ', name).strip()



"""
annot = ['http://www.w3.org/2000/01/rdf-schema#label', 'http://www.geneontology.org/formats/oboInOwl#hasSynonym', 'http://www.geneontology.org/formats/oboInOwl#hasExactSynonym', 'http://www.w3.org/2004/02/skos/core#exactMatch', 'http://www.ebi.ac.uk/efo/alternative_term', 'http://www.orpha.net/ORDO/Orphanet_#symbol', 'http://purl.org/sig/ont/fma/synonym', 'http://www.w3.org/2004/02/skos/core#prefLabel', 'http://www.w3.org/2004/02/skos/core#altLabel', 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#P108', 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#P90']
annot += [
    'https://www.omg.org/spec/Commons/AnnotationVocabulary/synonym',
    'https://www.omg.org/spec/Commons/AnnotationVocabulary/abbreviation',
    'https://www.omg.org/spec/Commons/AnnotationVocabulary/acronym',

    'http://www.w3.org/2004/02/skos/core#definition',
    'https://www.omg.org/spec/Commons/AnnotationVocabulary/explanatoryNote',
    'http://www.w3.org/2004/02/skos/core#example',
    'http://www.w3.org/2004/02/skos/core#note'
]

base = 'bertmap data\\data_to_upload\\ontos\\'
src_onto_file = base + 'EFS.owl'
tgt_onto_file = base + 'FIBOLt.owl'

ThesaurusCorpus(tgt_onto_file, annot).corpus
"""

