"""Test cltk.lemmatize."""

import unittest

from cltk.lemmatize.latin.backoff import DefaultLemmatizer
from cltk.lemmatize.latin.backoff import IdentityLemmatizer
from cltk.lemmatize.latin.backoff import TrainLemmatizer
from cltk.lemmatize.latin.backoff import PPLemmatizer
from cltk.lemmatize.latin.backoff import RegexpLemmatizer
from cltk.lemmatize.latin.backoff import RomanNumeralLemmatizer
from cltk.lemmatize.latin.backoff import UnigramLemmatizer
from cltk.lemmatize.latin.backoff import NgramPOSLemmatizer
from cltk.lemmatize.latin.backoff import BigramPOSLemmatizer
#from cltk.lemmatize.latin.regexp_patterns import rn_patterns
from cltk.stem.latin.j_v import JVReplacer
from cltk.tokenize.word import WordTokenizer

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'


class TestSequenceFunctions(unittest.TestCase):
    """Class for unittest"""

    def test_default_lemmatizer(self):
        """Test default_lemmatizer()"""
        lemmatizer = DefaultLemmatizer('UNK')
        test_str = 'Ceterum antequam destinata componam'
        target = [('ceterum', 'UNK'), ('antequam', 'UNK'), ('destinata', 'UNK'), ('componam', 'UNK')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_identity_lemmatizer(self):
        """Test identity_lemmatizer()"""
        lemmatizer = IdentityLemmatizer()
        test_str = 'Ceterum antequam destinata componam'
        target = [('ceterum', 'ceterum'), ('antequam', 'antequam'), ('destinata', 'destinata'), ('componam', 'componam')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_model_lemmatizer(self):
        """Test model_lemmatizer()"""
        model = {'ceterum': 'ceterus', 'antequam': 'antequam', 'destinata': 'destino', 'componam': 'compono'}  # pylint: disable=line-too-long
        lemmatizer = TrainLemmatizer(model=model)
        test_str = 'Ceterum antequam destinata componam'
        target = [('ceterum', 'ceterus'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_unigram_lemmatizer(self):
        """Test unigram_lemmatizer()"""
        train = [[('ceterum', 'ceterus'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono')]]  # pylint: disable=line-too-long
        lemmatizer = UnigramLemmatizer(train=train)
        test_str = """Ceterum antequam destinata componam"""
        target = [('ceterum', 'ceterus'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_regex_lemmatizer(self):
        """Test regex_lemmatizer()"""
        pattern = [(r'(\w*)abimus', 'o')]
        lemmatizer = RegexpLemmatizer(pattern)
        test_str = 'amabimus'
        target = [('amabimus', 'amo')]
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_latin_pp_lemmatizer(self):
        """Test latin_pp_lemmatizer()"""
        pattern = [(r'(\w*)[a|ie]bimus\b', 1)]
        pps = { 'amo': [1, 'am', 'amare', 'amau', 'amat'] }
        lemmatizer = PPLemmatizer(pattern, pps=pps)
        test_str = 'amabimus'
        target = [('amabimus', 'amo')]
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)

    def test_roman_numeral_lemmatizer(self):
        """Test roman_numeral_lemmatizer()"""
        rn_patterns = [(r'(?=^[MDCLXVUI]+$)(?=^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|IU|V?I{0,3}|U?I{0,3})$)', 'NUM'), (r'(?=^[mdclxvui]+$)(?=^m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|iu|v?i{0,3}|u?i{0,3})$)', 'NUM')]
        lemmatizer = RomanNumeralLemmatizer(rn_patterns)
        test_str = 'i ii iii iv v vi vii vii ix x xx xxx xl l lx c cc'
        target = [('i', 'NUM'), ('ii', 'NUM'), ('iii', 'NUM'), ('iu', 'NUM'), ('u', 'NUM'), ('ui', 'NUM'), ('uii', 'NUM'), ('uii', 'NUM'), ('ix', 'NUM'), ('x', 'NUM'), ('xx', 'NUM'), ('xxx', 'NUM'), ('xl', 'NUM'), ('l', 'NUM'), ('lx', 'NUM'), ('c', 'NUM'), ('cc', 'NUM')]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)
        

    def test_bigram_pos_lemmatizer(self):
        train = [[('dixissem', 'dico', 'v')], [('de', 'de', 'r'), ('te', 'tu', 'p'), ('autem', 'autem', 'c'), (',', 'punc', 'u'), ('catilina', 'catilina', 'n'), (',', 'punc', 'u'), ('cum', 'cum2', 'c'), ('quiescunt', 'quiesco', 'v'), (',', 'punc', 'u'), ('probant', 'probo', 'v'), (',', 'punc', 'u'), ('cum', 'cum2', 'c'), ('patiuntur', 'patior', 'v'), (',', 'punc', 'u'), ('decernunt', 'decerno', 'v'), (',', 'punc', 'u'), ('cum', 'cum2', 'c'), ('tacent', 'taceo', 'v'), (',', 'punc', 'u'), ('clamant', 'clamo', 'v'), (',', 'punc', 'u'), ('neque', 'neque', 'c'), ('hi', 'hic', 'p'), ('solum', 'solus', 'd'), ('quorum', 'qui', 'p'), ('tibi', 'tu', 'p'), ('auctoritas', 'auctoritas', 'n'), ('est', 'sum', 'v'), ('uidelicet', 'uidelicet', 'd'), ('cara', 'carus', 'a'), (',', 'punc', 'u'), ('uita', 'uita', 'n'), ('uilissima', 'uilis', 'a'), (',', 'punc', 'u'), ('sed', 'sed', 'c'), ('etiam', 'etiam', 'c'), ('illi', 'ille', 'p'), ('equites', 'eques', 'n'), ('romani', 'romanus', 'a'), (',', 'punc', 'u'), ('honestissimi', 'honestus', 'a'), ('atque', 'atque', 'c'), ('optimi', 'bonus', 'a'), ('uiri', 'uir', 'n'), (',', 'punc', 'u'), ('ceteri', 'ceterus', 'a'), ('-que', '-que', 'c'), ('fortissimi', 'fortis', 'a'), ('ciues', 'ciuis', 'n'), ('qui', 'qui', 'p'), ('circumstant', 'circumsto', 'v'), ('senatum', 'senatus', 'n'), (',', 'punc', 'u'), ('quorum', 'qui', 'p'), ('tu', 'tu', 'p'), ('et', 'et', 'c'), ('frequentiam', 'frequentia', 'n'), ('uidere', 'uideo', 'v'), ('et', 'et', 'c'), ('studia', 'studium', 'n'), ('perspicere', 'perspicio', 'v'), ('et', 'et', 'c'), ('uoces', 'uox', 'n'), ('paulo', 'paulus', 'd'), ('ante', 'ante', 'd'), ('exaudire', 'exaudio', 'v'), ('potuisti', 'possum', 'v'), ('.', 'punc', 'u')]]
        lemmatizer = BigramPOSLemmatizer(train=train, include=['cum'])
        test_str = """Quod cum esset intellectum et animadversum fecit animo libentissimo populus Romanus"""
        target = [('quod', None), ('cum', 'cum2'), ('esset', None), ('intellectum', None), ('et', None), ('animaduersum', None), ('fecit', None), ('animo', None), ('libentissimo', None), ('populus', None), ('romanus', None)]  # pylint: disable=line-too-long
        jv_replacer = JVReplacer()
        tokenizer = WordTokenizer('latin')
        test_str = test_str.lower()
        test_str = jv_replacer.replace(test_str)
        tokens = tokenizer.tokenize(test_str)
        lemmas = lemmatizer.lemmatize(tokens)
        self.assertEqual(lemmas, target)
        
        
if __name__ == '__main__':
    unittest.main()
