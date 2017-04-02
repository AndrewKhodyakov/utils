#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
"""
    Насчитываем_хеш_суммы_изображений
"""
import os, sys
import shutil
sys.path.append(os.getcwd())

from itertools import  islice
from multiprocessing import Pool
import datetime

from PIL import Image
import imagehash
import zipfile

PATH_TO_ZIPs = '../data'
PATH_TO_EXTRACT = '../tmp'
PATH_TO_RESULT = '../result'

#LAST_END_POINT = 655061
LAST_END_POINT = None

PROC_COUNT = 10
#===============================================================================
def one_step(image):
    """ 
    One step for hash compute.
    image: dict
    """ 
    image = image
    try:
        open_image = Image.open(image['path'])

        #calc imagehash
    
        image['aHash'] = imagehash.average_hash(open_image).__str__()
        image['dHash'] = imagehash.dhash(open_image).__str__()
        image['pHash'] = imagehash.phash(open_image).__str__()
        open_image.close()
    
        #calc md5sum
        image['md5sum'] = os.popen('md5sum ' + image['path']).read().split('  ')[0]

        os.remove(os.path.abspath(image['path']))
        return '{0}, {1}, {2}, {3}, {4}\n'.format(
            image['img_id'],
            image['aHash'],
            image['dHash'],
            image['pHash'],
            image['md5sum']
        )
    except:
        print('Битое изображение: {0}, индекс {1}'.format(
            image['path'],
            image['index']
        ))

        #delete file
        os.remove(os.path.abspath(image['path']))
        return None

def preprocessing(zipobj, result, last_end_point=None):
    """
    preparatory work
    zipobj: zipfile instance
    result: file instance
    """
    listzip = zipobj.namelist()
    len_listzip = len(listzip)

    if last_end_point:
        start_index = last_end_point
    else:
        start_index = 0

    indexes = islice(range(len_listzip), start_index, len_listzip, PROC_COUNT)

    for index in indexes: #перебираем прореженный счетчик файлов
        args = []

        for subindex in range(PROC_COUNT): 
            image = dict.fromkeys(
                ['img_id', 'aHash', 'dHash', 'pHash', 'md5sum', 'path', 'index']
            )
            tmp = index + subindex #полный индекс к файлу в массиве

            if tmp != len_listzip:
                prefix = None
                if ('.jpg' in listzip[tmp]):
                    prefix = '.jpg'

                elif ('.Jpg' in listzip[tmp]):
                    prefix = '.Jpg'

                elif ('.JPG' in listzip[tmp]):
                    prefix = '.JPG'

                elif ('.jpeg' in listzip[tmp]):
                    prefix = '.jpeg'

                elif ('.Jpeg' in listzip[tmp]):
                    prefix = '.Jpeg'

                elif ('.JPEG' in listzip[tmp]):
                    prefix = '.JPEG'

                if prefix:
                    image['index'] = tmp
                    image['path'] =\
                        zipobj.extract(listzip[tmp], PATH_TO_EXTRACT).__str__()
                    image['img_id'] = image['path'].split('/')[-1:][0].strip(prefix)
                    args.append(image)

            else:
                break

        if len(args) != 0:
            with Pool(3) as pool:
                for res in pool.map(one_step, args):
                    if res is not None:
                        result.write(res)

#===============================================================================

if __name__ == "__main__":


    for archive_name in os.listdir(PATH_TO_ZIPs):
        path_to_archive = os.path.abspath(PATH_TO_ZIPs) + '/' + archive_name
        path_to_result = os.path.abspath(PATH_TO_RESULT) +\
             '/' + archive_name + '.csv'

        print('='*50)
        with zipfile.ZipFile(path_to_archive) as zip_archive:
            print(
                'Start work with {0} - file count: {1} in time {2}'.\
                    format(
                        archive_name,
                        len(zip_archive.namelist()),
                        datetime.datetime.now()
                    )
            )
            result = open(path_to_result, 'a')
            preprocessing(zip_archive, result, last_end_point=LAST_END_POINT)

            result.close()

        #clear tmp 
        shutil.rmtree(
            os.path.abspath(PATH_TO_EXTRACT) + '/' +
            archive_name.split('.zip')[0]
        )
        #сбрасываем точку старта прошлого архива
        LAST_END_POINT = None
