# BioVision: A Versatile Deep Learning Platform for Biomedical Image Segmentation

**BioVision** is a cutting-edge, standalone deep learning software platform that leverages YOLOv11 object detection models and fine-tuned SAM 2.1 for high-performance instance segmentation across diverse biological applications and imaging modalities.

## 🔬 Key Features

- **Multi-Modal Support**: Works across ultrasound, X-ray, MRI, electron microscopy, and brightfield microscopy
- **Cancer Diagnostics**: Accurate classification and segmentation of breast cancer (X-ray mammography) and brain tumors (MRI)
- **Comprehensive Organ Segmentation**: Supports 34 human organs and 8 mouse tissues from histology datasets
- **Fetal Biometry**: Precise fetal structure segmentation in ultrasound images for developmental assessment
- **Cellular Analysis**: White blood cell classification and subcellular structure segmentation (mitochondria)
- **User-Friendly Interface**: Intuitive GUI with both segmentation and classification workflows

## 🎯 Applications

### Medical Diagnostics
- **Breast Cancer Detection**: 88.5% classification accuracy, 100% segmentation accuracy
- **Brain Tumor Analysis**: 99.5% classification accuracy, 97.5% segmentation accuracy
- **Fetal Development**: 99% accuracy in fetal structure segmentation

### Research Applications
- **Histopathology**: Automated tissue identification across diverse organ systems
- **Hematology**: 99.4% accuracy in white blood cell classification
- **Cellular Biology**: Precise mitochondria segmentation in EM images
- **Comparative Biology**: Cross-species anatomical mapping

## 🏗️ Architecture

BioVision employs a sophisticated two-stage architecture:

1. **Stage 1**: Custom-trained YOLOv11 models for robust object detection and region proposal
2. **Stage 2**: Fine-tuned SAM 2.1 models for precise boundary delineation and instance segmentation

## 📊 Performance Highlights

- **High Accuracy**: >88.5% across all applications
- **Fast Processing**: 4.8-11.9ms per image (depending on modality and resolution)
- **Cross-Modal Robustness**: Consistent performance across different imaging techniques
- **Clinical Precision**: Minimal false negatives in cancer detection (0% for breast cancer)

## 🚀 Getting Started

### Requirements
- Python 3.11+
- PyTorch 2.6.0+
- Ultralytics 8.3.133
- NVIDIA GPU (recommended: A100-SXM4-40GB for optimal performance)

## 💾 Downloads

### Complete Software Package
- **Google Drive**: [BioVision Complete Package](https://drive.google.com/drive/folders/1LzO3A1K51_qQuJX6fAoHclBic3wUGmHM)
  - Pre-trained models for all applications
  - Complete source code
  - Example datasets
  - Documentation and tutorials

### Individual Components
- **Source Code**: Available in Google Drive package
- **Pre-trained Models**: Included in Google Drive package
- **Example Datasets**: Sample data for testing and validation

## 🔬 Scientific Impact

BioVision addresses critical challenges in biomedical image analysis by providing:

- **Standardized Workflows**: Consistent analysis across different imaging modalities
- **Clinical Translation**: Tools that bridge the gap between research and clinical practice
- **Open Science**: Fully open-source platform promoting reproducible research
- **Multi-Scale Analysis**: From subcellular structures to whole organisms

## 📈 Validation

Our comprehensive evaluation includes:
- **Cancer Detection**: Outperforming existing methods in brain tumor classification
- **Cross-Modal Testing**: Validated across 5+ imaging modalities
- **Large-Scale Datasets**: Tested on thousands of images across diverse biological contexts
- **Clinical Relevance**: Metrics optimized for real-world medical applications

## 🤝 Contributing

We welcome contributions from the scientific community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- Adding new applications
- Improving existing models
- Dataset contributions
- Bug reports and feature requests

## 📞 Contact

- **Corresponding Author**: Inass.odeh@campus.technion.ac.il
- **Department**: Genetics and Developmental Biology, Technion Israel Institute of Technology

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Technion Israel Institute of Technology
- The Rappaport Faculty of Medicine and Research Institute
- Google Colab for computational resources
- The open-source community for foundational tools and datasets

---

*BioVision: Advancing biomedical research through intelligent image analysis* 🔬✨



## 📚 Citation

If you use BioVision in your research, please cite:

```bibtex
@article{odeh2025biovision,
  title={BioVision: A Versatile Deep Learning Platform Leveraging YOLOv11 and SAM 2.1 for Instance Segmentation Across Fundamental Biological Questions and Diverse Imaging Modalities},
  author={Odeh, Anas and Salem, Rahaf and Salem, Yara and Salem, Ahmad and Shemesh, Ariel and Hasson, Peleg},
  journal={[Journal Name]},
  year={2025}
}
