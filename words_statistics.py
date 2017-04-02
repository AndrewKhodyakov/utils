#!/usr/bin/env python
"""
"""
import os
import sys
import pandas as pd
def _run_reading(arg):
    """
    Read file and calc stats
    arg: path to file
    """
    if os.path.exists(arg) is False:
        msg = 'Check path {}'.format(arg)
        raise FileNotFoundError(msg)
    in_put = open(arg, 'rt')
    try:
        tmp = in_put.readline()
        in_put.seek(0)
    except:
        msg = 'Check file format in  {}'.format(arg)
        raise  IOError(msg)

    raw_words = []

    banned = ['?', '!', ':', ',', '.', '"']
    stripper = lambda word, sign: word.strip(sign) if sign in word else word

    for line in in_put:
        raw_words = raw_words + line.split(' ')
    
    raw_words = []
    for word in words:
        for sign in banned:
            words.append(stripper(word, sign))

    

def _run_unittests():
    """
    Run unittest
    """
    from io import BytesIO
    import unittest

    class TestCounter(unittest.TestCase):
        """
        Test for counter
        """
            def setUp(self):
                """
                setup test data
                """
                self.file = io.StringIO("""На разрисованных райскими цветами
тарелках с черною широкой каймой лежала тонкими ломтиками нарезанная семга,
маринованные угри. На тяжелой доске кусок сыру в слезах, и в серебряной
кадушке, обложенной снегом, - икра. Меж тарелками несколько тоненьких
рюмочек и три хрустальных графинчика с разноцветными водками. Все эти
предметы помещались на маленьком мраморном столике, уютно присоседившемся
у громадного резного дуба буфета, изрыгавшего пучки стеклянного и серебряного
света. Посредине комнаты - тяжелый, как гробница, стол, накрытый белой
скатертью, а на нем два прибора, салфетки, свернутые в виде папских тиар,
и три темных бутылки.
3ина внесла серебряное крытое блюдо, в котором что-то ворчало. 3апах от блюда
шел такой, что рот пса немедленно заполнился жидкой слюной. "Сады
Семирамиды!", - подумал он и застучал, как палкой, по паркету хвостом.""")

            def test_read_data_from_file(self):
                """
                Test read data
                """
                pass
def _read_args_and_run():
    """
    Set execute mode
    """
    arg = sys.argv
    n_arg = len(arg)

    help_msg = 'Input next arguments:\n'
    help_msg = help_msg + '\t' + '--run_self_test - for run unittests;\n'
    help_msg = help_msg + '\t' + '--get_stats path_to_file - for read from
data from.\n'

    if (n_arg > 1) & (n_arg <= 3):

        if (n_arg == 2) & ('--run_self_test' in arg[1]):
            _run_unittests()

        elif (n_arg == 3) & ('--get_data' in arg[1]):
            _get_mode(arg[2])

        else:
            print(help_msg)

    else:
        print(help_msg)

if __name__ == "__main__":
    _read_args_and_run()
