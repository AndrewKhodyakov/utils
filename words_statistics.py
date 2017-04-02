#!/usr/bin/env python
"""
    Words statistics
"""
import os
import sys
import pandas as pd


def _get_words_from_file(in_put):
    """
    Get word from file
    in_put: file object
    """
    raw_words = []
    for line in in_put:
        raw_words = raw_words + line.split(' ')

    banned = ['?', '!', ':', ',', '.', '"']
    stripper = lambda word, sign: word.strip(sign) if sign in word else word
    words = []
    for word in raw_words:
        for sign in banned:
            word = stripper(word, sign)
        if word not in ['-', ':']:
            words.append(word)

    return words

def _calc_stats(words):
    """
    words: words list
    """
    frame = pd.DataFrame(words, columns=['word'])
    out = []
    for unique in frame.word.unique():
        out.append((unique, (frame[frame.word == unique].count().values[0])))

    return out

def _save_result(result, f_name=None):
    """
    save file
    result: list of tupels
    """
    result = pd.DataFrame(result, columns=['word', 'freq'])
    result = result.sort_values(['freq', 'word'], ascending=[False, True])
    return result.to_csv(f_name, sep=':', header=False, index=False)


def _run_reading_and_calc(arg):
    """
    Read file and calc stats
    arg: path to file
    """
    if os.path.exists(arg) is False:
        msg = 'Check path {}'.format(arg)
        raise FileNotFoundError(msg)

    in_put = open(arg, 'rt')

    try:
        in_put.readline()
        in_put.seek(0)
    except:
        msg = 'Check file format in  {}'.format(arg)
        raise  IOError(msg)
    _save_result(_calc_stats(_get_words_from_file(in_put)),\
        './' + in_put.name.strip('txt').strip('.').strip('/') + '.csv')


def _run_unittests():
    """
    Run unittest
    """
    from io import StringIO
    import unittest

    class TestCounter(unittest.TestCase):
        """
        Test for counter
        """
        def setUp(self):
            """
            setup test data
            """
            self._short_text = 'aaaa, bbbb'
            self._short_file = StringIO(self._short_text)
            self._words = ['aaaa', 'bbbb']
            self._result = [('ab', 3), ('ac', 2), ('b', 4), ('c', 1)]
            self._output_format = "b:4\nab:3\nac:2\nc:1\n"

        def test_a(self):
            """
            Test read data
            """
            self.assertListEqual(_get_words_from_file(self._short_file), self._words)

        def test_b(self):
            """
            Test calc stats
            """
            result = _calc_stats(self._words)
            for res in result:
                self.assertEqual(res[1], 1)

        def test_c(self):
            """
            Save result
            """
            self.assertEqual(_save_result(self._result), self._output_format)

    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestCounter))
    unittest.TextTestRunner().run(suite)

def _read_args_and_run():
    """
    Set execute mode
    """
    arg = sys.argv
    n_arg = len(arg)

    help_msg = 'Input next arguments:\n'
    help_msg = help_msg + '\t' + '--run_self_test - for run unittests;\n'
    help_msg = help_msg + '\t' + '--get_stats path_to_file - for read from data from.\n'

    if (n_arg > 1) & (n_arg <= 3):
        if (n_arg == 2) & ('--run_self_test' in arg[1]):
            _run_unittests()

        elif (n_arg == 3) & ('--get_stats' in arg[1]):
            _run_reading_and_calc(arg[2])

        else:
            print(help_msg)

    else:
        print(help_msg)

if __name__ == "__main__":
    _read_args_and_run()
