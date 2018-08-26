"""
Functions in this utility file:
unpickle(path)
flatten(lst)
curtail(lst, read_len, motif_number)
prepare_input(training_size, test_size, length_read, original_list, motif_number)
to_np_array(X_train, y_train, X_test, y_test)
save_model(model, path)
load_model(model_path, weights_path)
"""

def save_model(model, path) :
	"""
	Save MODEL as a .json file and its weight as .h5 file to PATH
	author: Zhanyuan Zhang
	This function is inspired by Jason Brownlee's post
	For details, look here: https://machinelearningmastery.com/save-load-keras-deep-learning-models/
	"""
	model_json = model.to_json()
	with open(path, "w") as json_file:
		json_file.write(model_json)
	model.save_weights("model.h5")
	print("Save model to " + path)

def load_model(model_path, weights_path):
	"""
	Load a model with its weight
	author: Zhanyuan Zhang
	This function is inspired by Jason Brownlee's post
	For details, look here: https://machinelearningmastery.com/save-load-keras-deep-learning-models/
	"""
	from keras.models import model_from_json
	json_file(model_path, 'r')
	load_model_json = json_file.read()
	json_file.close()
	loaded_model = models.model_from_json(loaded_model_json)
	loaded_model.load_weights(weights_path)
	print("Loaded model from " + model_path)


def unpickle(path):
    """
    A helper function to reconstruct a serialized file from bytes
    author: Zhanyuan Zhang
    :param path: a string of the file's path
    :return: the original file before serialization
    """
    import pickle
    with open(path, "rb") as fo:
        toReturn = pickle.load(fo, encoding='bytes')
    return toReturn

def flatten(lst):
    """
    A helper function to flatten a 2d list to 1d.
    Input: [[1, 2], [2, 3], [3, 4, 5]]
    Output: [1, 2, 2, 3, 3, 4, 5]
    author: YiChen Fang
    """
    new_lst = []
    for sub_lst in lst:
        for item in sub_lst:
            new_lst.append(item)
    return new_lst


def curtail(lst, read_len, motif_number):
    """
    A helper function to transform a lst so that its length becomes read_len by:
    1. If len(lst) > read_len, curtail the end of the lst.
    2. If len(lst) < read_len, keep extending the end of the lst with 0 (NA).
    author: Yichen Fang
"""
    if len(lst) > read_len:
        lst = lst[:read_len]
    else:
        for i in range(read_len - len(lst)):
            lst.append([0 for _ in range(motif_number + 4)])
    return lst


def prepare_input(training_size, test_size, length_read, original_list, motif_number):
    """
    Produce the train-test split
    length_read: the length that you want all DNA sequences to conform to
    author: Yichen Fang
    """
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    seq_count = 0
    while seq_count < training_size:
        X_train.append(flatten(curtail(original_list[seq_count][3], length_read, motif_number)))
        y_train.append(int(original_list[seq_count][1]))
        seq_count += 1
    while seq_count < (training_size + test_size):
        X_test.append(flatten(curtail(original_list[seq_count][3], length_read, motif_number)))
        y_test.append(int(original_list[seq_count][1]))
        seq_count += 1
    return X_train, y_train, X_test, y_test

def to_np_array(X_train, y_train, X_test, y_test):
    """
    Turn list into numpy tensors that can directly feed into a neural network model
    author: Yichen Fang
    """
    import numpy as np
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    if len(y_train.shape) == 1:
        y_train = np.transpose(np.array([y_train]))
    X_test = np.array(X_test)
    y_test = np.transpose(np.array(y_test))
    if len(y_test.shape) == 1:
        y_test = np.transpose(np.array([y_test]))
    return X_train, y_train, X_test, y_test