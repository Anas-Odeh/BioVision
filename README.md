# BioVision: Universal, Cross-Modal Deep Learning for Biomedical Image Analysis

![Institution: Technion](https://img.shields.io/badge/Institution-Technion-red.svg)
![Field: Biomedical AI](https://img.shields.io/badge/Field-Biomedical%20AI-green.svg)

**BioVision** is an **integrated** software platform for automated **instance segmentation** and **classification** across diverse imaging modalities. By utilizing **YOLOv11** as an automated prompt generator for the **SAM 2.1** foundational architecture, the platform provides a solution for high-throughput biomedical image analysis without the need for manual spatial prompting.

---

## 📑 **Abstract**

Accurate instance segmentation is fundamental to clinical diagnostics across diverse imaging modalities. While foundation models like the **Segment Anything Model 2.1 (SAM 2.1)** offer delineation, their reliance on manual spatial prompting can limit automated workflows. We introduce **BioVision**, an integrated deep learning platform combining task-specific, fine-tuned **You Only Look Once version 11 (YOLOv11)** region-proposal models with the foundational SAM 2.1 architecture. 

**The platform was evaluated across a spectrum of biological scales and imaging modalities, ranging from low-magnification fetal analysis and clinical tumor identification to high-resolution cellular segmentation.** 

---

## 🔬 **Key Features**

*   **Integrated Architecture**: Combines **YOLOv11** (localization) and **SAM 2.1** (segmentation) into a single, automated pipeline.
*   **Multi-Modal Utility**: Validated for **MRI, X-ray, Ultrasound, and Brightfield Microscopy**.
*   **Automated Morphometry**: Instant export of physical descriptors (Area, Eccentricity, Centroids, etc.) to structured **Excel** and **CSV** reports.
*   **Standalone Software**: Features a dedicated **Graphical User Interface (GUI)** designed for researchers without specialized computational expertise.

---

## 📊 **Performance Benchmarks**

BioVision reached high accuracy levels across 20 biological targets, showing performance gains compared to zero-shot **VGG16**, **EfficientNet-B0**, and standalone **SAM 2.1** ($p < 0.05$).

| Application Area | Mean Confidence | 95% Confidence Interval (CI) |
| :--- | :--- | :--- |
| **Brain Tumor (MRI)** | **99.56%** | [99.21%, 99.92%] |
| **Breast Cancer (X-ray)** | **97.61%** | [95.94%, 99.28%] |
| **White Blood Cells (WBC)** | **99.87%** | [99.76%, 99.98%] |
| **Multi-Organ Histology** | **94.79%** | [93.51%, 96.08%] |

> **Note**: For full metrics across all 20 biological targets, refer to the **BioVision_Performance_Metrics.xlsx** file in this repository.

---

## 🏗️ **Technical Workflow**

The platform operates through a sequential automated pipeline:
1.  **Detection Phase**: A fine-tuned **YOLOv11** engine identifies biological targets and generates automated bounding-box prompts.
2.  **Segmentation Phase**: These coordinates are passed to the **SAM 2.1** mask decoder, confining the transformer’s attention to specific **Regions of Interest (ROIs)** for automated boundary definition.

---

## 💾 **Resources & Downloads**

*   📦 **[Standalone Software Package](https://drive.google.com/drive/folders/1LzO3A1K51_qQuJX6fAoHclBic3wUGmHM)**: Download the installation-ready BioVision engine.
*   🧠 **[Pre-trained Weights (.pt)](https://drive.google.com/file/d/1ueTQ-KnkjQ4mg3a9LpGoMV6_QxsG6mkf/view)**: Optimized models for clinical and histological analysis.
*   📖 **[BioVision User Manual](./BioVision%20User%20Manual.pdf)**: Documentation for system deployment and interface navigation.

---

## 📞 **Contact & Affiliations**

*   **Author**: **Anas Odeh** (Inass.odeh@campus.technion.ac.il)
*   **Principal Investigator**: **Peleg Hasson** (phasson@technion.ac.il)
*   **Institution**: **Technion – Israel Institute of Technology**, Rappaport Faculty of Medicine

### **Acknowledgments**
We acknowledge the developers of **YOLOv11** and **SAM 2.1**, and the **GTEx** and **Roboflow** communities for providing the foundational datasets and architectures that supported this research.
