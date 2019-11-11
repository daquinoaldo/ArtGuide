# SDAIS = Smart Deep AI for Search 
# Commentiamo tutte le funzioni e classi seguendo formato Doxygen
from .document_model import DocumentModel
from .semantic_search import Semantic_Search, BERT_distance
import spacy

class DocumentsAdaptation():
    def __init__(self, verbose=False):
        self.available_languages = {'en':'en_core_web_sm','de':'de_core_news_sm',
                            'fr':'fr_core_news_sm','es':'es_core_news_sm', 
                            'it':'it_core_news_sm', 'multi':'xx_ent_wiki_sm'}
        self.distance = BERT_distance()
        self.search_engine = Semantic_Search(self.distance)
        self.verbose = verbose

    # Input: json contenente informazioni dell'utente passate dall'applicazione
    # Out: serie di keyword da passare a SDAIS per la generazione di queries specializzate
    # Formato output: {
    #                  "keyword1":["keyword1_expanded_1","keyword1_expanded_2","keyword1_expanded_3"],
    #                   "keyword2":["keyword2_expanded_2","keyword2_expanded_3","keyword2_expanded_4"]
    #                   ....
    #                   }

    def get_language_stopwords(self, user):
        if (user.language in self.available_languages):
            spacy_nlp = spacy.load(self.available_languages[user.language])
        else:
            spacy_nlp =  spacy.load(self.available_languages['multi'])

        spacy_lang = getattr(spacy.lang, user.language, None)
        
        if spacy_lang:
            stop_words = spacy_lang.stop_words.STOP_WORDS
        else:
            stop_words = []

        return stop_words


    def get_keywords(self, tastes):
        res = {}
        for taste in tastes:
            res[taste] = [taste]
        if self.verbose:
            print(f"Expanded keywords: {res}")
        return res

    # Input: json contenente articoli ricevuti da SDAIS 
    # Out: articolo filtrato im base alle preferenze dell'utente 
    # Formato output: string
    # Proto: il primo articolo per ora puo' andare bene
    def get_tailored_text(self, results, user):
        stop_words = self.get_language_stopwords(user)

        if len(results)<=0:
            return "Content not found"
        
        documents =  list(map(lambda x: DocumentModel(x, user, stop_words=stop_words), results))
        for doc in documents: 
            salient_sentences = doc.salient_sentences()
            results = self.search_engine.find_most_similar_multiple_keywords(salient_sentences, user.tastes, verbose=False)
            doc.topics_affinity_score(results)
            doc.user_readability_score()
        
        # Da cambiare
        documents.sort(key=lambda x: (x.readability_score*10000)+x.affinity_score, reverse=True )

        if self.verbose:
            print("Ordered documents")
            print([{"title":doc.title, "url":doc.url, "affinity_score":doc.affinity_score, 'readability_score':doc.readability_score} for index, doc in enumerate(documents)])

        best_document = documents[0]
        return best_document.plain_text
        

    