#!/usr/bin/env python
# -*- coding: utf-8 -*-
#=========================================================
"""
   Создает пустой шаблон питоновского скрипта в текущем каталоге
"""
#=========================================================
import sys
import os

#=========================================================
class New_script:
    def __init__(self):
        self.create_path = os.getcwd()
        self.script_name = sys.argv[2]
        self.script_comment = sys.argv[3]
        self.of = open((self.create_path + '/' + self.script_name + '.py'), 'w')
#=========================================================
    def create_header(self, spec_comment=''):
        self.of.write('#!/usr/bin/env python\n')
        self.of.write('# -*- coding: utf-8 -*-\n')
        self.of.write('#=' + '='*77 +'=\n')
        self.of.write('"""\n')
        self.of.write(('    ' + spec_comment + self.script_comment+'\n'))
        self.of.write('"""\n')
        self.of.write('#=' + '='*77 +'=\n')

    def create_middle(self): pass
    def create_import(self): pass
    def create_ending(self): pass
    def create_script(self): pass
#=========================================================
class Unit_test_script(New_script):

    def __init__(self):
        New_script.__init__(self)

    def import_modules(self):
        self.of.write('import unittest')
        self.of.write('\n')
        self.of.write('import random')
        self.of.write('\n')

    def create_middle(self):
        self.of.write('class  (unittest.TestCase) #TODO Напиши имя класса\n')
        self.of.write('\n')
        self.of.write('    def setUp(self):pass\n')
        self.of.write('#-------------------------------------------------------\n')
        self.of.write('\n')
        self.of.write('#-------------------------------------------------------\n')
        self.of.write('    def tearDown(self): pass\n')
        self.of.write('\n')


    def create_ending(self):
        self.of.write('#=' + '='*77 +'=\n')
        self.of.write('\n')
        self.of.write('if __name__ == "__main__":\n')
        self.of.write('    unittest.main()')
        self.of.write('\n')
        self.of.close()

    def create_script(self):
        self.create_header('Юнит тест для')
        self.import_modules()
        self.create_middle()
        self.create_ending()

#=========================================================
class Simple_script(New_script):

    def __init__(self):
        New_script.__init__(self)

    def import_modules(self):
        self.of.write('\n')

    def create_middle(self):
        self.of.write('\n')
        self.of.write('#-------------------------------------------------------\n')
        self.of.write('\n')
        self.of.write('#-------------------------------------------------------\n')
        self.of.write('\n')

    def create_ending(self):
        self.of.write('#=' + '='*77 +'=\n')
        self.of.write('\n')
        self.of.write('if __name__ == "__main__": pass\n')
        self.of.write('\n')
        self.of.close()

    def create_script(self):
        self.create_header()
        self.import_modules()
        self.create_ending()


#=========================================================
if __name__ == "__main__":
    f_keys = ['-s', '-t']
    if len(sys.argv) != 4:
        print("Введите три аргумента: имя_скрипта краткое_описание_скрипта\n")
    else:
        if sys.argv[1] == '-s':
            scrpt = Simple_script()
            scrpt.create_script()
        elif sys.argv[1] == '-t':
            scrpt = Unit_test_script()
            scrpt.create_script()
        else:
            print('Укажите правильный ключ:\n')
            print('     -s - генераци пустого python скрипта;\n')
            print('     -t - генераци unittest скрипта;\n')
