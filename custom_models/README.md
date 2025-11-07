# Custom Models — Advanced Model Registry Examples

## Overview

This directory provides examples demonstrating advanced model registration and inference techniques using the Snowflake Model Registry. These examples highlight how **Custom Model Classes** can extend standard model behavior or support non-ML workloads.

---

## 1. Extending `predict()` for Advanced Inference

**Author:** Narin Dhatwalia

This example demonstrates how to override the default `predict()` method when logging a model in the Snowflake Model Registry. It focuses on XGBoost models that require additional inference parameters such as `base_margin`, which are not supported by the automatically attached `predict()` method.

### Key Concepts

- Implementing a custom class derived from `CustomModel`
- Passing a trained model via `ModelContext`
- Defining a flexible `predict()` method that accepts additional inputs
- Logging the model with `Registry.log_model()` and including a complete input signature

**Notebook:** [`custom_models_demo.ipynb`](./custom_models_demo.ipynb)

**Reference:**  
"Using the Snowflake Model Registry with Custom Model Classes" — *Narin Dhatwalia, July 2025*

---

## 2. Deploying Non-ML Python Models as Services

**Author:** Chase Romano (to be added)

This example demonstrates how the Model Registry can be used to operationalize **non-ML Python classes** as servable functions. This approach is useful for customers who:

- Do not have Docker environments
- Wish to version and invoke Python-based logic (e.g., transformations, rules engines) directly within Snowflake

### Key Concepts

- Using `custom_model` for pure Python workloads
- Registering and invoking deterministic transformations through the Model Registry
- Leveraging Snowpark for inference execution

---

## Folder Structure

Below is the recommended folder layout for this example:
```
custom_models/
├── README.md                    ← Documentation (this file)
├── custom_models_demo.ipynb     ← Example notebook demonstrating custom predict() with base_margin
└── requirements.txt             ← Python dependencies for reproducibility
```

---

## Learning Objectives

- Understand when and why to use **CustomModel** classes
- Learn how to override `.predict()` for more flexible inference workflows
- Explore how the Model Registry can host both ML and non-ML Python workflows