import tensorflow as tf
import os
import datetime
import string
import cv2

from .data import preproc as pp
from .data.generator import DataGenerator, Tokenizer
from .data.reader import Dataset
from .network.model import HTRModel
from .data import line_seperation as seperator

# define parameters
source = "bentham"
arch = "flor"
epochs = 1000
batch_size = 16

# define paths
# source_path = os.path.join("..", "data", f"{source}.hdf5")
# output_path = os.path.join("..", "output", source, arch)
# target_path = os.path.join(output_path, "checkpoint_weights.hdf5")
# os.makedirs(output_path, exist_ok=True)

target_path = "checkpoint_weights.hdf5"

# define input size, number max of chars per line and list of valid chars
input_size = (1024, 128, 1)
max_text_length = 128
charset_base = string.printable[:95]

# print("source:", source_path)
# print("output", output_path)
# print("target", target_path)
# print("charset:", charset_base)

def predictions(img_path, predictions_per_line=5, verbose = False):
    '''
    	Input: Image path
    	Output: Tupple containing top 'predictions_per_line' predictions
    			in a list, prints if verbose is True
    '''

    # print("\n\n\n\n\n", img_path, "\n\n\n\n\n")

    # x = cv2.imread(img_path)
    # print(x)

    lines = seperator.get_lines(img_path)

    tokenizer = Tokenizer(chars=charset_base, max_text_length=max_text_length)


    model = HTRModel(architecture=arch,
                        input_size=input_size,
                        vocab_size=tokenizer.vocab_size,
                        top_paths=10)

    model.compile()
    model.load_checkpoint(target=target_path)

    l = []
    for index, line in enumerate(lines):
        img = pp.preprocess(line, input_size=input_size, actual = True)
        x_test = pp.normalization([img])
        predicts, probabilities = model.predict(x_test, ctc_decode=True)
        predicts = [[tokenizer.decode(x) for x in y[:predictions_per_line]] for y in predicts]

        l.append([predicts[0], probabilities[0]])

        if verbose:
        	print_predictions(predicts, probabilities)

        	# cv2.imshow(f'{index}', line)
        	# cv2.waitKey(0)
        	print("\n####################################"  )

    # print("\n\n\n\n",l ,"\n\n\n\n\n")
    s=""
    for item in l:
        s = s+item[0][0]+"\n"
    return s

def print_predictions(predicts, probs):
	for i, (pred, prob) in enumerate(zip(predicts, probs)):
		print("\nProb.\t- Predict")
	
		for (pd, pb) in zip(pred, prob):
			print(f"{pb:.4f} - {pd}")


# img_path = "images/handwritten6.jpg"
# predictions(img_path, verbose=True)