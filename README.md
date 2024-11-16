
# Disease Prediction System Using Flask and Decision Tree Classifier

This is a web application that predicts diseases based on user-selected symptoms. It leverages machine learning, specifically a **Decision Tree Classifier**, trained on a labeled dataset of symptoms and diseases.

---

## Features
- Predicts diseases based on selected symptoms.
- User-friendly web interface created using **Flask**.
- Utilizes a **Decision Tree Classifier** from `sklearn` for machine learning.
- Displays prediction accuracy on test data.

---

## How It Works

1. **Input**: Users select symptoms from dropdown menus on the website.
2. **Processing**:
   - Symptoms are encoded as a binary vector.
   - The vector is passed to a trained Decision Tree model.
3. **Output**: The application predicts the most likely disease and displays it.

---

## Theory Behind the Application

### Machine Learning Model

- **Model Used**: Decision Tree Classifier
- **Training Features**: A list of symptoms (`l1`) treated as binary input features (1 = present, 0 = absent).
- **Target Variable**: Diseases (`prognosis`), encoded numerically for training.
- The Decision Tree learns relationships between symptoms and diseases during training.
Here’s a simplified **example decision tree** for a subset of symptoms and diseases to help understand how the Decision Tree Classifier in this program works.

---

### Example Data
We’ll consider the following **symptoms** (subset):
- `fever`
- `cough`
- `headache`

And the following **diseases** (subset):
1. **Common Cold**
2. **Flu**
3. **Migraine**

---

### Example Training Data
| Fever | Cough | Headache | Disease          |
|-------|-------|----------|------------------|
| 1     | 1     | 0        | Common Cold      |
| 1     | 1     | 1        | Flu              |
| 0     | 0     | 1        | Migraine         |

---

### Visualized Decision Tree

Below is an example decision tree for this dataset:

```
               Fever
             /       \
         Yes           No
        /                \
      Cough             Headache
     /     \            /      \
   Yes     No      Yes (Migraine)
(Flu)  (Common Cold)
```

---

### Explanation of the Decision Tree
1. **Root Node (Fever)**:
   - The first decision is whether the patient has a fever (`1` for Yes, `0` for No).
2. **Left Subtree (Fever = Yes)**:
   - If the patient has a fever, the next question is about the presence of a cough.
     - If **Cough = Yes** → The disease is `Flu`.
     - If **Cough = No** → The disease is `Common Cold`.
3. **Right Subtree (Fever = No)**:
   - If the patient does not have a fever, the next question is about the presence of a headache.
     - If **Headache = Yes** → The disease is `Migraine`.
     - If **Headache = No** → No diagnosis from this tree.

---


### Dataset
- **Training Dataset**: `Training.csv` maps symptoms to diseases.
- **Testing Dataset**: `Testing.csv` evaluates the model's accuracy.
- The data is preprocessed by:
  - Replacing disease names with numerical labels.
  - Extracting symptoms and diseases as features and targets.

### Prediction
- The trained model predicts a disease based on the symptoms entered by the user. The result is mapped back to the disease name.

---

## Project Structure
```bash
.
├── app.py                # Main Flask application
├── Training.csv          # Training dataset
├── Testing.csv           # Testing dataset
├── templates/
│   └── index.html        # Frontend for symptom input
└── README.md             # Project documentation
```
---

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Flask
- scikit-learn
- pandas
- numpy

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Ganesh57803/disease_prediction.git
   ```
2. Install the required dependencies:
   ```bash
   pip install flask scikit-learn pandas numpy
   ```
   OR

   ```bash
   pip install -r requirements.txt
   ```
   
3. Run the application:
   ```bash
   python app.py
   ```
4. Open a browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

---

## Usage

1. Open the web application.
2. Select symptoms from the dropdown menus.
3. Submit the form.
4. View the predicted disease.

---

## Model Performance

- The application uses `accuracy_score` to evaluate the model on the test dataset:
  - **Overall Accuracy**: The percentage of correctly predicted diseases.
  - **Misclassified Count**: The number of incorrect predictions.

---

## Limitations

1. **Overfitting**: Decision trees may overfit to the training data, affecting accuracy on unseen data.
2. **Dataset Dependency**: Results rely on the quality and diversity of the training data.
3. **Symptom Overlap**: Diseases with similar symptoms might be harder to differentiate.

---

## Contribution

Feel free to submit issues or pull requests for enhancements.

---

## License

This project is licensed under the MIT License.

---

