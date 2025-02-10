import os
import json
from code2vec.config import Config
from code2vec.code2vec import load_model_dynamically

class Code2VecWrapper:
    def __init__(self, model_path):
        print(f"🚀 Loading Code2Vec model from: {model_path}")
        try:
            # Initialize configuration
            self.config = Config(set_defaults=True)
            self.config.DL_FRAMEWORK = 'keras'  # Set the framework explicitly
            self.config.MODEL_LOAD_PATH = model_path
            self.model = load_model_dynamically(self.config)
            print("✅ Code2Vec model loaded successfully.")
        except Exception as e:
            import traceback
            print("❌ Error loading Code2Vec model:")
            traceback.print_exc()  # This will print the full error traceback
            self.model = None

    def extract_features(self, code_snippet):
        """
        Extract semantic features from a Python code snippet using Code2Vec.
        """
        if not self.model:
            print("⚠️ Model not loaded. Skipping feature extraction.")
            return None

        try:
            vector = self.model.predict(code_snippet)
            return vector
        except Exception as e:
            print(f"⚠️ Error processing snippet: {e}")
            return None

    def process_mutants(self, mutants_dir):
        """
        Process all mutant files in the specified directory and extract features.
        """
        features = {}
        processed_files = 0
        skipped_files = 0

        print(f"📂 Processing mutants from: {mutants_dir}")

        for filename in os.listdir(mutants_dir):
            if filename.endswith((".c2v", ".txt")): 
                mutant_path = os.path.join(mutants_dir, filename)
                try:
                    with open(mutant_path, "r") as file:
                        code = file.read()

                    vector = self.extract_features(code)
                    if vector:
                        features[filename] = vector
                        processed_files += 1
                        print(f"✅ Features extracted for {filename}")
                    else:
                        skipped_files += 1
                        print(f"⚠️ Skipped mutant {filename} due to extraction issue.")
                except Exception as e:
                    skipped_files += 1
                    print(f"❌ Error reading {filename}: {e}")

        # Save extracted features
        output_path = os.path.join(mutants_dir, "features.json")
        with open(output_path, "w") as f:
            json.dump(features, f, indent=4)

        print(f"\n🚀 Feature extraction complete.")
        print(f"✅ Processed: {processed_files} files.")
        print(f"⚠️ Skipped: {skipped_files} files due to errors.")
        print(f"📥 Features saved to: {output_path}")


if __name__ == "__main__":
    model_path = "data/models/code2vec_model/saved_model__entire-model/ckpt-1"  # Path to the pre-trained Code2Vec model
    mutants_dir = "data/output/preprocessed"  # Directory where mutants are stored

    code2vec = Code2VecWrapper(model_path)
    code2vec.process_mutants(mutants_dir)
