# Medical Mimic Data Mining: Data Warehouse Module

## 📋 Project Overview

This directory contains the **Data Warehouse Module**, the foundational pillar of the **Medical Mimic Data Mining** ecosystem.

This project focuses on the end-to-end engineering of a modern clinical data warehouse using the **MIMIC-III** dataset. It implements a **Medallion Architecture** (Bronze, Silver, Gold layers) to ingest, transform, and model complex intensive care unit (ICU) data for business intelligence and advanced analytics.

---

## �️ High-Level Architecture

![High Level Vision](conception/HIGH_LEVEL_ARCH.png)

The ultimate vision for this project extends beyond a traditional Data Warehouse. The goal is to build a comprehensive **Data-Driven Ecosystem** comprising three interconnected pillars:

1. **Data Warehouse Module** (Current Focus): The central source of truth, ingesting and structuring clinical data (Bronze/Silver/Gold).
2. **AI-Models Cluster**: A dedicated environment for training and serving predictive models (e.g., Sepsis Prediction, Mortality Risk).
3. **Full-Stack Application**: A clinician-facing portal to visualize insights and real-time alerts.

---

## 🏫 Project Context
![1767322003475](image/README/1767322003475.png)

This work was conducted as a specialized **Data Mining Project** for the **5IIR16** course.

**Author:**

* **Ayoub Majjid**

---

## 📂 Repository Structure

* **[`project/`](./project/)**: **(Start Here)** The core implementation directory. Contains:
  * Source code for ETL pipelines (Bronze/Silver/Gold loaders).
  * Docker configuration for the PostgreSQL warehouse.
* **[`conception/`](./conception/)**: Architectural assets, class diagrams, and design documents.

For detailed installation instructions, architectural deep-dives, and the full technical report, please navigate to the **[`project/`](./project/)** directory.
