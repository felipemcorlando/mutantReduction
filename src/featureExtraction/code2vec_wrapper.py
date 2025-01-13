from featureExtraction.code2vec.code2vec import Code2VecModel

class Code2VecWrapper:
    def __init__(self, model_path):
        self.model = Code2VecModel(model_path)
    
    def extract_features(self, code_snippet):
        """
        Extract semantic features from a Python code snippet.
        :param code_snippet: str, the code snippet
        :return: vector representation
        """
        return self.model.infer_vector(code_snippet)
