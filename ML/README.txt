# Machine Learning – Employee Attrition Prediction

## Overview

This ML module is part of the **Creation of Workforce Insights Dashboard for Employee Skill and Analytics – Group 2** project.

The objective is to use employee data to **predict employee attrition** using machine learning techniques.

## Dataset

The dataset contains employee-related attributes such as:

* Age
* Hourly Rate
* Education
* Distance From Home
* Job Level
* Job Satisfaction
* Monthly Income
* Performance Rating
* Years at Company
* And other employee-related features

### Dataset Split

* **Training data:** 1,176 records
* **Testing data:** 294 records
* **Total dataset:** 1,470 records
* **Target variable:** `Attrition`

## ML Process

```text
Employee Dataset
      ↓
Data Preprocessing
      ↓
Feature Selection
      ↓
Train/Test Split
      ↓
ML Model Training
      ↓
Model Evaluation
      ↓
Attrition Prediction
```

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Jupyter Notebook

## Output

The trained ML model predicts whether an employee is likely to leave the organization:

* `0` → No Attrition
* `1` → Attrition

The predictions can be used in the **Workforce Insights Dashboard** for workforce analysis and decision support.

## Files

```text
ML/
├── Training Dataset
├── Testing Dataset
├── Attrition Labels
├── ML Model / Notebook
└── README.md
```

## Purpose

The ML module provides **predictive workforce insights** by identifying employee attrition patterns and generating attrition predictions from historical employee data.

