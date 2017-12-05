import sys
import logging
from reader import Reader
from model import AveragedPerceptron
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import numpy as np

reload(sys)
sys.setdefaultencoding('utf-8')

# create a logger
logger = logging.getLogger('util_logger')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

def run(lang1, lang2, embed_name, folder_name):
    # --- init reader
    reader = Reader()

    # --- read files for language 1
    logger.info('read ' + lang1)
    train_X1, train_y1, test_X1, test_y1, valid_X1, valid_y1 = reader.read_files(lang1)
    idf1 = reader.read_idf(lang1)

    # --- read files for language 2
    logger.info('read ' + lang2)
    train_X2, train_y2, test_X2, test_y2, valid_X2, valid_y2 = reader.read_files(lang2)
    idf2 = reader.read_idf(lang2)

    # --- read embedding
    logger.info('read embedding')
    word_dict1, embed_mat1, word_dict2, embed_mat2 = reader.load_embed(lang1, lang2, embed_name, folder_name)

    # --- vectorize language 1
    logger.info('vectorize ' + lang1)
    train_X1, test_X1, valid_X1 = reader.vectorize([train_X1, test_X1, valid_X1], idf1, word_dict1, embed_mat1)

    # --- vectorize language 2
    logger.info('vectorize ' + lang2)
    train_X2, test_X2, valid_X2 = reader.vectorize([train_X2, test_X2, valid_X2], idf2, word_dict2, embed_mat2)

    # --- train classifier model
    clf = AveragedPerceptron(max_iter=15)

    logger.info('training classifier on ' + lang1)
    clf.fit(train_X1, train_y1)
    logger.info('training classifier on ' + lang2)
    clf.fit(train_X2, train_y2)
    # clf.save_weight(lang=lang1, embed_name='I_matrix')

    logger.info('test on ' + lang1 + ' training set')
    rand_idx = np.random.choice(train_X1.shape[0], 1000)
    clf.evaluate(map(lambda x: train_X1[x], rand_idx), map(lambda x: train_y1[x], rand_idx))
    clf.evaluate(train_X1, train_y1)

    logger.info('test on ' + lang1 + ' test set')
    rand_idx = np.random.choice(test_X1.shape[0], 1000)
    clf.evaluate(map(lambda x: test_X1[x], rand_idx), map(lambda x: test_y1[x], rand_idx))
    clf.evaluate(test_X1, test_y1)

    logger.info('test on ' + lang2 + ' training set')
    rand_idx = np.random.choice(train_X2.shape[0], 1000)
    clf.evaluate(map(lambda x: train_X2[x], rand_idx), map(lambda x: train_y2[x], rand_idx))
    clf.evaluate(train_X2, train_y2)

    logger.info('test on ' + lang2 + ' test set')
    rand_idx = np.random.choice(test_X2.shape[0], 1000)
    clf.evaluate(map(lambda x: test_X2[x], rand_idx), map(lambda x: test_y2[x], rand_idx))
    clf.evaluate(test_X2, test_y2)


if __name__ == "__main__":
    lang = ['chinese', 'english', 'french', 'german', 'italian', 'spanish']
    # run(lang1='english', lang2='french', embed_name='BAE', folder_name='en-fr')
    run(lang1='english', lang2='spanish', embed_name='BAE', folder_name='en-es')
    # run(lang1='english', lang2='german', embed_name='I-Matrix', folder_name='de-en.40')
    # run_I_matrix('english', 'french', 'fr-en.80')
    # run_I_matrix('spanish', 'english', 'es-en.80')