# BioVision: A Fully Automated, Cross-Modal YOLOv11 and SAM 2.1 Framework for Biomedical Instance Segmentation and Classification

**BioVision** is a cutting-edge, standalone diagnostic platform that bridges the gap between foundational AI and clinical research. By leveraging a synergistic hybrid architecture—integrating **YOLOv11** for automated region proposal and **SAM 2.1** for pixel-precise segmentation—BioVision provides a zero-manual-prompt solution for high-throughput biomedical image analysis.

---

## 🔬 **Key Features**

*   **Synergistic Hybrid Architecture**: Eliminates the manual prompting bottleneck by using YOLOv11 as a "scout" for the SAM 2.1 transformer decoder.
*   **Multi-Modal Versatility**: Validated across **Ultrasound, X-ray, MRI, and Brightfield/Electron Microscopy**.
*   **Dual-Module GUI**: Dedicated workflows for **Instance Segmentation** and **Image Classification**.
*   **Automated Morphometry**: Instant export of physical descriptors (Area, Eccentricity, etc.) to **Excel and CSV**.

---

## 📊 **Performance Highlights (Mean Accuracy & 95% CI)**

BioVision has been rigorously validated across multiple clinical cohorts, demonstrating high precision and statistical reliability:

*   **Brain Tumor Classification (MRI)**: **99.56%** (95% CI: **99.21% – 99.92%**)
*   **Breast Cancer Classification (X-ray)**: **97.61%** (95% CI: **95.94% – 99.28%**)
*   **White Blood Cell (WBC) Classification**: **99.87%** (95% CI: **99.76% – 99.98%**)
*   **Fetal Biometry (Ultrasound)**: **>99%** accuracy in structural segmentation.

---

## 🏗️ **Technical Architecture**

BioVision operates through a two-stage automated pipeline:

1.  **Stage 1 (Detection)**: A fine-tuned **YOLOv11** engine identifies biological targets and generates automated bounding-box prompts.
2.  **Stage 2 (Segmentation)**: Bounding boxes are passed to the **SAM 2.1** mask decoder, confining the transformer’s attention to specific Regions of Interest (ROIs) for rapid, pixel-precise boundary definition.

---

## 💾 **Software & Model Downloads**

### **Complete Distribution**
*   **[BioVision Complete Package (Google Drive)](https://drive.google.com/drive/folders/1LzO3A1K51_qQuJX6fAoHclBic3wUGmHM)**: Includes the standalone software, source code, and comprehensive documentation.

### **Pre-trained Weights (.pt)**
*   **[YOLOv11 Trained Models](https://drive.google.com/file/d/1Mu0S7JYzwAArPMWXu2tPBpgBiTXHva0c/view?usp=drive_link)**: Weights for the **15 human organ atlas**, oncology diagnostics, and fetal biometry.
*   **[SAM 2.1 Checkpoints](https://drive.google.com/file/d/1WhabPUttfBppjNcj3r2bzIwBIR_1f-_o/view?usp=drive_link)**: Optimized models for boundary delineation across all scales.

---

## 📖 **Documentation**

*   **[Guidelines for BioVision installation software.pdf](./Guidelines%20for%20BioVision%20installation%20software.pdf)**: Detailed instructions for environment setup and system deployment.
*   **[BioVision User Manual](./BioVision%20User%20Manual.pdf)**: A step-by-step guide for navigating the GUI, loading models, and exporting data.

---

## 📈 **Validation & Open Science**

BioVision is built on the principles of **Open Science**. Our validation strategy utilizes patient-level and slide-level data isolation to prevent leakage and ensure true clinical generalizability.

*   **Codebase**: Fully open-source and modular.
*   **Reproducibility**: Pre-trained weights and example datasets are provided to allow for immediate verification of manuscript results.

---

## 📞 **Contact & Affiliations**

*   **Corresponding Author**: **Inass.odeh@campus.technion.ac.il**
*   **Institution**: **Technion – Israel Institute of Technology**
*   **Department**: Genetics and Developmental Biology, Rappaport Faculty of Medicine.

---

### 🙏 **Acknowledgments**
Special thanks to the developers of **YOLOv11**, **SAM 2.1**, and the **Roboflow** and **GTEx** communities for providing the foundational datasets and architectures that made this research possible.
