import argparse
import codecs

import stanfordnlp
from gensim.models import KeyedVectors

from num2words import num2words
from utils.amr import AMR
from utils.text2int import text2int


class Aligner:

    def __init__(self, model):
        self.model = KeyedVectors.load_word2vec_format(model)
        self.nlp = stanfordnlp.Pipeline(lang='pt', processors='tokenize,lemma')
        self.countries = self.read_resource('resources/countries.txt')
        self.nationalities = self.read_resource('resources/nationalities.txt')
        self.negation = ['não', 'sem', 'mal']
        self.ner = self.read_resource('resources/ner.txt')
        self.abstract_concepts = self.read_resource('resources/abstract-concepts.txt')
        self.adverses = ['mas', 'porém', 'contudo', 'todavia', 'entretanto', 'entanto', 'obstante']

        self.threshold = 1.5

    @staticmethod
    def read_resource(input_f):
        resource = []
        with codecs.open(input_f, 'r', 'utf-8') as f:
            for value in f.read().split(','):
                resource.append(value.strip())
        return resource

    def create_alignment(self, file, amr_graph, sentence, key_l, value_l, amr_penman, tokens):
        alignment = {}

        concepts, attributes, relations = amr_graph.get_triples()

        attributes = self.remove_top_relation(attributes)
        filtered_tokens, lemma, oov = self.preprocess(sentence, tokens)
        self.align_top(concepts, filtered_tokens, tokens, lemma, alignment, relations, attributes, key_l, value_l)
        self.align_concepts(concepts[1:], filtered_tokens, tokens, lemma, key_l, value_l, alignment, relations,
                            attributes)
        self.align_attributes(attributes, filtered_tokens, tokens, lemma, key_l, value_l, alignment, oov)
        self.create_file_alignment(file, amr_penman, sentence, tokens, alignment)

    def align_attributes(self, attributes, filtered_tokens, tokens, lemma, key_l, value_l, alignment, oov):
        for x, y, attr in attributes:
            if attr == '-':
                self.align_negation(attr, filtered_tokens, tokens, lemma, key_l, value_l, alignment)
            elif attr == 'interrogative' and '?' in filtered_tokens:
                position = [pos[0] for pos in tokens].index('?')
                key = str(position)+'-'+str(position+1)+'|'
                value = value_l[key_l.index(attr)]
                if key not in alignment:
                    alignment[key] = value
            elif attr == 'imperative' and '!' in filtered_tokens:
                position = [pos[0] for pos in tokens].index('!')
                key = str(position)+'-'+str(position+1)+'|'
                value = value_l[key_l.index(attr)]
                if key not in alignment:
                    alignment[key] = value
            elif attr.isdigit() and num2words(int(attr), lang='pt_BR') in filtered_tokens:
                for t in range(len(filtered_tokens)):
                    if num2words(int(attr), lang='pt_BR') == filtered_tokens[t]:
                        position = tokens.index(filtered_tokens[t])
                        key = str(position)+'-'+str(position+1)+'|'
                        value = value_l[key_l.index(attr)]
                        if key not in alignment:
                            alignment[key] = value
                            break
            elif attr.isdigit() and num2words(int(attr), to='ordinal', lang='pt_BR') in filtered_tokens:
                for t in range(len(filtered_tokens)):
                    if num2words(int(attr), to='ordinal', lang='pt_BR') == filtered_tokens[t]:
                        position = tokens.index(filtered_tokens[t])
                        key = str(position)+'-'+str(position+1)+'|'
                        value = value_l[key_l.index(attr)]
                        if key not in alignment:
                            alignment[key] = value
                            break
            if attr.isdigit() and num2words(int(attr), lang='pt_BR') in oov:
                for t in range(len(tokens)):
                    if num2words(int(attr), lang='pt_BR') == tokens[t]:
                        position = t
                        key = str(position)+'-'+str(position+1)+'|'
                        value = value_l[key_l.index(attr)]
                        if key not in alignment:
                            alignment[key] = value
                            break
            if attr.isdigit() and attr in oov:
                for t in range(len(oov)):
                    if oov[t] == attr:
                        position = tokens.index(oov[t])
                        key = str(position)+'-'+str(position+1)+'|'
                        value = value_l[key_l.index(attr)]
                        if key not in alignment:
                            alignment[key] = value
                            break
            if attr.isdigit():
                for t in range(len(filtered_tokens)):
                    if text2int(filtered_tokens[t]) == attr:
                        position = tokens.index(filtered_tokens[t])
                        key = str(position)+'-'+str(position+1)+'|'
                        value = value_l[key_l.index(attr)]
                        if key not in alignment:
                            alignment[key] = value
                            break

    def align_negation(self, attribute, filtered_tokens, tokens, lemma, key_l, value_l, alignment):
        position = ''
        for t in range(len(filtered_tokens)):
            for neg in self.negation:
                if neg == lemma[t]:
                    position = t
        if position != '':
            key = str(position)+'-'+str(position+1)+'|'
            value = value_l[key_l.index(attribute)]
            if key not in alignment:
                alignment[key] = value

    @staticmethod
    def remove_top_relation(attributes):
        index = [y[0] for y in attributes].index('TOP')
        del attributes[index]
        return attributes

    def preprocess(self, sentence, tokens):

        filtered_tokens, oov = self.filter_tokens(tokens)
        if filtered_tokens:
            lemma = self.get_lemma(filtered_tokens)
        else:
            lemma = []
        return filtered_tokens, lemma, oov

    def filter_tokens(self, tokens):
        filtered_tokens, oov = [], []
        for token in tokens:
            if token in self.model.vocab:
                filtered_tokens.append(token)
            else:
                oov.append(token)
        return filtered_tokens, oov

    def get_lemma(self, filtered_tokens):
        lemma = []
        sentence = ' '.join(filtered_tokens)
        doc = self.nlp(sentence)
        for sent in doc.sentences:
            for word in sent.words:
                lemma.append(word.lemma)
        return lemma

    def align_abstract_concept(self, concepts, tokens, filtered_tokens, alignment, relations, attributes, key_l,
                               value_l, lemma):
        self.align_named_entities(concepts, concepts[0][1], concepts[0][2], relations, attributes, tokens,
                                  filtered_tokens, alignment, key_l, value_l, lemma)

    def align_top(self, concepts, filtered_tokens, tokens, lemma, alignment, relations, attributes, key_l, value_l):
        # For concrete concepts
        if concepts[0][2] in self.abstract_concepts or concepts[0][2] in self.ner:
            self.align_abstract_concept(concepts, tokens, filtered_tokens, alignment, relations, attributes, key_l,
                                        value_l, lemma)
        else:
            distance = 10
            for t in range(len(filtered_tokens)):
                aux = self.model.wmdistance(concepts[0][2].split('-')[0], lemma[t])
                if aux == 0.0:
                    token = filtered_tokens[t]
                    break
                elif aux < distance:
                    distance = aux
                    token = filtered_tokens[t]
            position = tokens.index(token)
            key = str(position)+'-'+str(position+1)+'|'
            value = '0'
            if key not in alignment:
                alignment[key] = value

    def align_concepts(self, concepts, filtered_tokens, tokens, lemma, key_l, value_l, alignment, relations,
                       attributes):
        for _, var, concept in concepts:
            if concept in self.ner or concept in self.abstract_concepts:
                self.align_named_entities(concepts, var, concept, relations, attributes, tokens, filtered_tokens,
                                          alignment, key_l, value_l, lemma)
            else:
                distance = 10
                for t in range(len(filtered_tokens)):
                    aux = self.model.wmdistance(concept.split('-')[0], lemma[t])
                    if aux == 0.0:
                        token = filtered_tokens[t]
                        break
                    if aux < distance:
                        distance = aux
                        token = filtered_tokens[t]
                if distance < self.threshold or aux == 0.0:
                    position = tokens.index(token)
                    key = str(position)+'-'+str(position+1)+'|'
                    try:
                        value = value_l[key_l.index(concept)]
                        if key not in alignment:
                            alignment[key] = value
                    except ValueError:
                        continue

    def align_named_entities(self, concepts, var_con, concept, relations, attributes, tokens, filtered_tokens,
                             alignment, key_l, value_l, lemma):
        position, word_level = [], []
        if concept == 'contrast-01':
            for token in range(len(tokens)):
                if tokens[token].lower() in self.adverses:
                    position.append(token)
                    # word_level.append(level.get(concept))
            if position:
                key = str(position[0])+'-'+str(position[-1]+1)+'|'
                value = value_l[key_l.index(concept)]
                if key not in alignment:
                    alignment[key] = value
        elif concept == 'be-located-at-91':
            for token in range(len(tokens)):
                if tokens[token] == 'eis' or tokens[token] == 'aqui' or tokens[token] == 'está':
                    position.append(token)
                    break
            if position:
                key = str(position[0]) + '-' + str(position[-1] + 1) + '|'
                value = value_l[key_l.index(concept)]
                if key not in alignment:
                    alignment[key] = value
        elif concept == 'be-temporally-at-91':
            return
        else:
            composition = ''
            node = [(rel, tgt, var) for rel, tgt, var in relations if tgt == var_con]
            attrs = [(rel, tgt, att) for rel, tgt, att in attributes if tgt == var_con]

            if node:
                attrs = [(rel, tgt, att) for rel, tgt, att in attributes if tgt == node[0][2]]
                if attrs:
                    for x, y, attr in attrs:
                        if attr[-1] == '_':
                            n_attr = attr[:-1]
                            if n_attr.lower() in tokens:
                                position.append(tokens.index(n_attr.lower()))
                                word_level.append(value_l[key_l.index('"'+n_attr+'"')])
                                key_l.remove('"'+n_attr+'"')
                                value_l.remove(word_level[-1])
                                attributes.remove((x, y, attr))
                            elif n_attr in self.countries:
                                try:
                                    position.append(tokens.index(self.nationalities[self.countries.index(n_attr)]))
                                except ValueError:
                                    distance = 10
                                    for t in range(len(filtered_tokens)):
                                        aux = self.model.wmdistance(n_attr, lemma[t])
                                        if aux < distance:
                                            distance = aux
                                            token = filtered_tokens[t]
                                position.append(tokens.index(token))
                                word_level.append(value_l[key_l.index('"' + n_attr + '"')])
                                key_l.remove('"' + n_attr + '"')
                                value_l.remove(word_level[-1])
                                attributes.remove((x, y, attr))
                    if position:
                        s = ''
                        for w in word_level:
                            s += w+'+'
                        key = str(position[0])+'-'+str(position[-1]+1)+'|'
                        value = value_l[key_l.index(concept)]+'+'+value_l[key_l.index(node[0][0])]+'+'+s[:-1]
                        aux = [(x, y, z) for x, y, z in concepts if node[0][2] == y][0]
                        concepts.remove(aux)
                        value_l.remove(value_l[key_l.index(node[0][0])])
                        key_l.remove(node[0][0])
                        value_l.remove(value_l[key_l.index(concept)])
                        key_l.remove(concept)
                        if key not in alignment:
                            alignment[key] = value
                else:
                    for rel, tgt, nod in concepts:
                        for x, y, z in node:
                            if z == tgt:
                                distance = 10
                                for t in range(len(filtered_tokens)):
                                    aux = self.model.wmdistance(nod, lemma[t])
                                    if aux < distance:
                                        distance = aux
                                        token = filtered_tokens[t]
                                if distance < self.threshold:
                                    position.append(tokens.index(token))
                                    word_level.append(value_l[key_l.index(nod)])
                                    key_l.remove(nod)
                                    value_l.remove(word_level[-1])
                    if word_level:
                        s = ''
                        for w in word_level:
                            s += w+'+'
                        key = str(position[0])+'-'+str(position[-1]+1)+'|'
                        value = value_l[key_l.index(concept)]+'+'+s[:-1]
                        if key not in alignment:
                            alignment[key] = value
            elif attrs:
                for x, y, attr in attrs:
                    if attr[-1] == '_':
                        n_attr = attr[:-1]
                        if n_attr.lower() in tokens:
                            position.append(tokens.index(n_attr.lower()))
                            word_level.append(value_l[key_l.index('"' + n_attr + '"')])
                            attributes.remove((x, y, attr))
                        elif n_attr.replace('"', '') in self.countries:
                            position.append(tokens.index(self.nationalities[self.countries.index(n_attr.replace('"', ''))]))
                            word_level.append(value_l[key_l.index('"' + n_attr + '"')])
                            attributes.remove((x, y, attr))
                    elif len(tokens) == 1:
                        if '-' in tokens[0]:
                            for t in tokens[0].split('-'):
                                if attr.lower() in t:
                                    composition += attr+'-'
                                    # position.append(tokens.index(attr.lower()))
                                    # word_level.append(level.get(attr))
                                    attributes.remove((x, y, attr))
                    else:
                        if attr.lower() in tokens:
                            position.append(tokens.index(attr.lower()))
                            word_level.append(value_l[key_l.index(attr)])
                            key_l.remove(attr)
                            value_l.remove(word_level[-1])
                            attributes.remove((x, y, attr))
                if composition:
                    if composition[:-1] == tokens[0]:
                        position.append(tokens.index(composition[:-1]))
                        for c in composition[:-1].split('-'):
                            word_level.append(value_l[key_l.index(c)])
                            key_l.remove(c)
                            value_l.remove(word_level[-1])
                        s = ''
                        for w in word_level:
                            s += w + '+'
                        # attributes.remove((x, y, attr))
                        key = str(position[0]) + '-' + str(position[-1] + 1) + '|'
                        value = value_l[key_l.index(concept)] + '+' + s[:-1]
                        if key not in alignment:
                            alignment[key] = value
                elif position:
                    s = ''
                    for w in word_level:
                        s += w + '+'
                    key = str(position[0])+'-'+str(position[-1]+1)+'|'
                    value = value_l[key_l.index(concept)]+'+'+s[:-1]
                    value_l.remove(value_l[key_l.index(concept)])
                    key_l.remove(concept)
                    if key not in alignment:
                        alignment[key] = value

    @staticmethod
    def create_file_alignment(input_f, amr_penman, sentence, tokens, alignment):
        with codecs.open('output/'+input_f+'.aligned', 'a', 'utf-8') as f:
            f.write('# ::snt ' + sentence + '\n')
            f.write('# ::tok ' + ' '.join(tokens) + '\n')
            f.write('# ::alignments ')
            for key, value in alignment.items():
                f.write(key)
                f.write(value+' ')
            f.write('\n')
            f.write(str(amr_penman) + '\n\n')


def main(data):
    flag = False
    print('Loading Pre-Trained Embeddings ...')
    aligner = Aligner('models/glove100.txt')
    print('Done!!!')

    print('### Running alignment ###')
    with codecs.open(data.file, 'r', 'utf-8') as amr_f:
        while True:
            amr, sentence, key, value, amr_penman, tokens = AMR.get_amr_line(amr_f)
            if amr == '':
                break
            try:
                amr = AMR.parse_AMR_line(amr)
            except Exception:
                flag = True
                break
            prefix = 'a'
            amr.rename_node(prefix)
            aligner.create_alignment(data.file, amr, sentence, key, value, amr_penman, tokens)
        if not flag:
            print('### Done ###')


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='AMR Aligner', epilog='Usage: python aligner.py -f file')
    args.add_argument('-f', '--file', help='Input AMR file', required=True)
    main(args.parse_args())
