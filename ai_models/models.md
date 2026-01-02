# ⭐ **Machine Learning Models – Structured Overview**


```
                         MACHINE LEARNING MODELS
                                     |
        ----------------------------------------------------------------
        |                                                              |
   SUPERVISED LEARNING                                        UNSUPERVISED LEARNING
 (Learning with labels)                                      (No labels provided)
        |                                                              |
  ---------------------------                                   --------------------------
  |                         |                                   |                        |
REGRESSION MODELS     CLASSIFICATION MODELS               CLUSTERING               ASSOCIATION
(Predict numbers)     (Predict categories)               (Regroupement)           (Rule learning)
  |                         |                                   |                        |
  |                         |                                   |                        |
  - Linear Regression       - Logistic Regression               - K-Means                - Apriori
  - Polynomial             - Decision Tree                      - DBSCAN                 - FP-Growth
  - Ridge / Lasso          - Random Forest                      - Hierarchical           - ECLAT
  - Random Forest Reg.     - SVM                                - Gaussian Mixture
  - XGBoost Reg.           - KNN                                - Mean-Shift
  - Neural Networks        - Neural Networks
```

## **1) Supervised Learning Models**

Models that learn from labeled data ( **input → known output** ).

### **A. Regression Models**

Predict a  **continuous numeric value** .

Examples:

* Linear Regression
* Polynomial Regression
* Ridge / Lasso / Elastic Net
* Random Forest Regression
* XGBoost Regression
* Neural Network Regression

### **B. Classification Models**

Predict a  **class/category** .

Examples:

* Logistic Regression
* Decision Tree Classifier
* Random Forest Classifier
* Naive Bayes
* Support Vector Machine (SVM)
* K-Nearest Neighbors (KNN)
* Neural Networks (MLP, CNN, LSTM)

---

## **2) Unsupervised Learning Models**

Models that learn from  **unlabeled data** .

### **A. Clustering (Regroupement)**

Groups similar data points into clusters.

Examples:

* K-Means
* Hierarchical Clustering
* DBSCAN
* Mean-Shift
* Gaussian Mixture Models (GMM)

### **B. Association Rule Learning**

Discovers relationships, correlations, and patterns between items.

Examples:

* Apriori
* FP-Growth
* ECLAT

---

# ⭐ **Simplified Summary Table**

| Category               | Subtype        | Purpose         | Examples                      |
| ---------------------- | -------------- | --------------- | ----------------------------- |
| **Supervised**   | Regression     | Predict numbers | Linear Reg., RF Reg., XGBoost |
| **Supervised**   | Classification | Predict classes | SVM, RF Classifier, KNN, NN   |
| **Unsupervised** | Clustering     | Group data      | K-Means, DBSCAN, GMM          |
| **Unsupervised** | Association    | Find item rules | Apriori, FP-Growth            |
