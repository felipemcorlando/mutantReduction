
---

# **Mutant Reduction Framework**

This repository provides an **automated pipeline** for **mutant reduction in mutation testing**, leveraging **FSM-based mutation generation, feature extraction, clustering, and equivalent mutant detection**. The framework helps optimize mutation testing by **identifying and pruning redundant mutants**, ultimately reducing computational costs.

---

## **Table of Contents**
- [📌 Installation](#installation)
- [📂 Project Structure](#project-structure)
- [🚀 Pipeline Overview](#pipeline-overview)
- [🔧 Running the Pipeline](#running-the-pipeline)
  - [1️⃣ Mutation Testing](#1️⃣-mutation-testing)
  - [2️⃣ Feature Extraction](#2️⃣-feature-extraction)
  - [3️⃣ Clustering](#3️⃣-clustering)
  - [4️⃣ Equivalent Mutant Detection](#4️⃣-equivalent-mutant-detection)
  - [5️⃣ Equivalent Mutant Pruning](#5️⃣-equivalent-mutant-pruning)
  - [6️⃣ Evaluation](#6️⃣-evaluation)
- [📊 Results](#results)
- [❓ Troubleshooting](#troubleshooting)
- [👥 Contributors](#contributors)

---

## 📌 **Installation**
Ensure your system is updated and install the necessary dependencies:

```bash
sudo apt update
sudo apt install python3.8 python3.8-venv python3.8-dev default-jre
```

### **Setting Up the Virtual Environment**
```bash
python3.8 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### **Install Additional Dependencies if Needed**
```bash
pip install pytest-mutagen hdbscan matplotlib numpy pandas sklearn pyqt5
```

---

## 📂 **Project Structure**
```
/mutantReduction
|-- data/
|   |-- output/
|       |-- clustering/                  # Clustering results (DBSCAN/HDBSCAN/KMeans)
|       |-- equivalence_testing/         # Test execution data for equivalent mutant analysis
|       |-- evaluation_mutants/          # Selected mutants for evaluation
|       |-- evaluation_results.json      # Mutation testing evaluation results
|       |-- equivalent_mutants.json      # Identified equivalent mutants
|       |-- features.json                # Extracted features from mutants
|       |-- fsm_transitions.json         # FSM transition states for mutants
|       |-- mutants/                     # Generated mutants
|       |-- pruned_equivalent_mutants.json # Pruned mutants after equivalence analysis
|       |-- selected_mutants.json        # Final selected mutants after pruning
|
|-- src/
|   |-- benchmarks/                      # Benchmarking tools
|   |-- clustering/                       # Clustering algorithms (HDBSCAN, KMeans)
|   |-- equivalent_mutants/               # Equivalent mutant detection & pruning
|   |-- feature_extraction/               # Structural metrics extraction
|   |-- fsm_modeling/                     # FSM-based mutation testing
|   |-- mutation_testing/                 # Mutation testing execution & evaluation
|
|-- requirements.txt                      # Project dependencies
|-- README.md                             # Project documentation
```

---

## 🚀 **Pipeline Overview**
The framework follows these key steps:

1️⃣ **Mutation Testing** → Generate FSM-based mutants  
2️⃣ **Feature Extraction** → Extract structural & behavioral features  
3️⃣ **Clustering** → Identify redundant mutants via HDBSCAN/KMeans  
4️⃣ **Equivalent Mutant Detection** → Detect semantically equivalent mutants  
5️⃣ **Equivalent Mutant Pruning** → Keep only the most representative mutants  
6️⃣ **Evaluation** → Run mutation testing on the pruned set  

---

## 🔧 **Running the Pipeline**

### **1️⃣ Mutation Testing**
Generates FSM-based mutants and stores them in `data/output/mutants/`.

```bash
python -m src.mutation_testing.mutpy_integration
```

📌 **Output:**  
- Mutants stored in `data/output/mutants/`  
- FSM transition data in `data/output/fsm_transitions.json`  

---

### **2️⃣ Feature Extraction**
Extracts structural metrics (e.g., function calls, arithmetic operations, conditionals, etc.).

```bash
python src/feature_extraction/structural_metrics.py
```

📌 **Output:**  
- Extracted features stored in `data/output/features.json`  

---

### **3️⃣ Clustering**
Clusters mutants using **HDBSCAN** or **KMeans**.

#### **Run HDBSCAN Clustering**
```bash
python src/clustering/hdbscan_clustering.py
```

#### **Run KMeans Clustering**
```bash
python src/clustering/kmeans_clustering.py
```

📌 **Output:**  
- `data/output/clustering/hdbscan_clustering.png`  
- `data/output/clustering/kmeans_clustering.png`  
- Cluster assignments in `data/output/kmeans_cluster_assignments.json`  

---

### **4️⃣ Equivalent Mutant Detection**
Detects **equivalent mutants** using:
- **Structural analysis** (code similarity)
- **Behavioral analysis** (test execution comparison)

```bash
python src/equivalent_mutants/equivalent_mutant_detector.py
```

📌 **Output:**  
- Equivalent mutants stored in `data/output/equivalent_mutants.json`

---

### **5️⃣ Equivalent Mutant Pruning**
Removes redundant mutants while keeping the most representative ones.

```bash
python src/equivalent_mutants/equivalent_mutant_pruner.py
```

📌 **Output:**  
- **Pruned mutants** stored in `data/output/pruned_equivalent_mutants.json`  
- **Selected mutants** stored in `data/output/selected_mutants.json`  
- **Evaluation mutants moved to** `data/output/evaluation_mutants/`  

---

### **6️⃣ Evaluation**
Runs mutation testing **only on the pruned set of mutants**.

```bash
python src/mutation_testing/mutpy_evaluation.py
```

📌 **Output:**  
- Evaluation results in `data/output/evaluation_results.json`

---

## 📊 **Results**
After evaluation, compare:
- **Mutation Score Before vs. After Reduction**
- **Impact of Clustering (HDBSCAN vs. KMeans)**
- **Effectiveness of Equivalent Mutant Pruning**
- **Computational Savings from Pruning Redundant Mutants**

---

## ❓ **Troubleshooting**
#### **Dependency Issues**
If dependencies are missing, install them:
```bash
pip install -r requirements.txt
```

#### **Matplotlib GUI Issues**
If Matplotlib fails to render plots, install PyQt5:
```bash
pip install pyqt5
```

#### **Missing Java for AST Extraction**
Ensure Java is installed:
```bash
sudo apt install default-jre
```


---

## 👥 **Contributors**
- **Felipe Orlando & João Paulo Nogueira** - Research & Implementation  
