import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from featureExtraction.code2vec_wrapper import Code2VecWrapper

model_path = "path/to/pretrained/code2vec/model"
wrapper = Code2VecWrapper(model_path)

code_snippet = """
def add(a, b):
    return a + b
"""

features = wrapper.extract_features(code_snippet)
print("Extracted Features:", features)
