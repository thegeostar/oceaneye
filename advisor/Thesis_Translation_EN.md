# Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning

> **Full English translation** of `【7】基于深度学习的水下图像超分辨率重建与目标检测方法研究1.pdf`
> (83 pages). Structure, headings, tables, figure numbers and page breaks follow the
> original exactly; only the language has changed. Page markers `--- p.N ---` map back
> to the original PDF page numbers.

---

--- p.1 ---

**GRADUATION THESIS (DESIGN)**

**TITLE**

# Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning

Student Name: **Li Kaixuan** (李凯旋)
Student ID: **2405023226**
School: **School of Computer and Software**
Major: **Artificial Intelligence Engineering Technology**
Class: **Intelligence 2432**
Supervisor: **Wang Li** (王丽)
Second Supervisor: **Chen Baoyu** (陈宝玉)

**May 2026**

--- p.2 ---

*(blank page)*

--- p.3 ---

**Nanjing Vocational University of Industry Technology**

**Graduation Thesis (Design) Statement of Academic Integrity**

I hereby solemnly declare: the graduation thesis (design) submitted herewith is the result of work carried out independently by me under the guidance of my supervisor. To the best of my knowledge, apart from content that is specifically marked and acknowledged in the text, this design (thesis) does not contain any results or works already published or written by any other individual or collective. All individuals and collectives who contributed to the research work involved in this design (thesis) have been explicitly identified in the text.

Author's signature:

Date: **22 May 2026**

--- p.4 ---

*(blank page)*

--- p.5 ---

i

## ABSTRACT (Chinese original)

Underwater images, during the acquisition process, are affected by light absorption and scattering effects, and generally suffer from colour imbalance, insufficient contrast and texture degradation, which severely constrain the effectiveness of advanced vision tasks such as underwater object detection. This thesis focuses on the two core tasks of underwater image super-resolution reconstruction and object detection, proposes two improved deep-learning-based methods, and validates them through systematic experiments on public datasets.

For underwater image super-resolution reconstruction, this thesis proposes the **Frequency–Spatial Coupled Inference Network (FSCIN)**. The core of this network is the **Spatial–Frequency Awareness Module (SFAM)**, which combines the Fast Fourier Transform (FFT) with Swin Transformer-based spatial-domain encoding. Using a dual-branch structure, it adaptively enhances the frequency-domain amplitude component and phase component separately, then restores them to the spatial domain via the Inverse Fast Fourier Transform (IFFT), achieving deep integration of global frequency-domain information and local spatial-domain features. In addition, this thesis introduces a **texture–structure joint loss function**, which applies targeted constraints to the image texture layer and structure layer separately, explicitly supervising the recovery of high-frequency details and geometric edges, thereby compensating for the limitations of conventional pixel-level losses. Experiments on the public USR-248 and UFO-120 datasets show that FSCIN achieves PSNR of **30.04 dB** and **25.98 dB** respectively at ×2 magnification, attains leading overall performance across multiple magnification factors, and delivers efficient reconstruction with only **30.70 GFLOPs** and **0.55 M** parameters.

For underwater image object detection, this thesis addresses the problems of YOLOv8 in underwater scenes — a limited local receptive field and insufficient feature representation capability for small objects — by designing a **fine-grained feature extraction module** to replace the original C2f module. This module is built collaboratively from three sub-modules: the **Channel–Spatial Adaptive Enhancement Module** precisely focuses on object edges and texture details through a channel–spatial dual attention mechanism; the **Mamba-based Global Perception Module** introduces a visual state space model to model global spatial dependencies with linear complexity; and the **Multi-Scale Cross-Attention Fusion Module** adaptively integrates local and global features through asymmetric convolution and cross-scale attention interaction. Experiments on the URPC2021 underwater object detection dataset show that, compared with the original YOLOv8, the improved model raises **mAP50 by 1.8 percentage points** and raises the small-object detection metric **APs by 1.1 percentage points**.

**Keywords:** underwater image super-resolution; frequency–spatial coupling; texture–structure loss; YOLOv8; underwater object detection

--- p.6 ---

ii

## ABSTRACT (English original — reproduced verbatim)

Underwater images are commonly degraded by light absorption and scattering, leading to colour imbalance, insufficient contrast, and texture degradation that severely compromise the performance of advanced visual tasks such as underwater object detection. This thesis addresses two core tasks — underwater image super-resolution reconstruction and target detection — by proposing two deep learning-based methods, validated through systematic experiments on public datasets.

For super-resolution, a Frequency-Spatial Coupled Inference Network (FSCIN) is proposed. Its core component, the Spatial Frequency Awareness Module (SFAM), combines the Fast Fourier Transform (FFT) with Swin Transformer-based spatial encoding. A dual-branch structure adaptively enhances the amplitude and phase components in the frequency domain respectively, then restores them to the spatial domain via Inverse FFT, achieving deep integration of global frequency information and local spatial features. A texture-structure joint loss function is further introduced to impose targeted supervision on the texture and structural layers separately, compensating for the limitations of conventional pixel-level losses. Experiments on USR-248 and UFO-120 show that FSCIN achieves PSNR of 30.04 dB and 25.98 dB at ×2 scale, with leading performance across multiple upscaling factors and efficient computation at only 30.70G FLOPs and 0.55M parameters.

For target detection, a fine-grained feature extraction module (FFEM) is designed to replace the C2f module in YOLOv8, addressing its limitations in underwater scenes. Three collaborative submodules are proposed: CAEM for local edge and texture enhancement, VSSM for long-range dependency modeling, and MCFM for adaptive multi-scale feature fusion.

**KEYWORDS:** Underwater image, Super-resolution reconstruction, Object detection, Deep learning, Frequency-space coupling, YOLOv8

--- p.7 ---

iii

## TABLE OF CONTENTS

| Entry | Page |
|---|---|
| Title | 1 |
| Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning | 1 |
| Nanjing Vocational University of Industry Technology | 1 |
| Graduation Thesis (Design) Statement of Academic Integrity | 1 |
| Abstract | 1 |
| Keywords | 1 |
| ABSTRACT | ii |
| KEYWORDS | ii |
| List of Figures and Tables | 1 |
| **Chapter 1 Introduction** | 3 |
| 1.1 Research Background and Significance | 3 |
| 1.2 Research Status at Home and Abroad | 4 |
| 1.2.1 Research Status of Underwater Image Super-Resolution Reconstruction | 4 |
| 1.2.2 Research Status of Underwater Image Object Detection | 6 |
| 1.3 Main Work of This Thesis | 8 |
| 1.4 Thesis Organisation | 9 |
| **Chapter 2 Related Theoretical Foundations** | 11 |
| 2.1 Theoretical Foundations of Deep Learning | 11 |
| 2.1.1 Convolutional Neural Networks | 11 |
| 2.1.2 The Transformer Model | 16 |
| 2.1.3 The Mamba Model | 17 |
| 2.2 Theoretical Analysis of Underwater Image Super-Resolution | 19 |
| 2.2.1 Underwater Image Degradation Model | 19 |
| 2.2.2 Principles of Underwater Image Super-Resolution Reconstruction | 20 |
| 2.3 Theoretical Foundations of Object Detection | 25 |
| 2.3.1 Two-Stage Object Detection Methods | 25 |
| 2.3.2 One-Stage Object Detection Methods | 26 |
| 2.3.3 Key Technologies of Deep-Learning-Based Object Detection | 27 |
| 2.3.4 Analysis of the Characteristics of Underwater Object Detection | 27 |
| 2.4 Chapter Summary | 27 |

--- p.8 ---

iv

| Entry | Page |
|---|---|
| **Chapter 3 An Underwater Image Super-Resolution Reconstruction Method Based on a Frequency–Spatial Coupled Inference Network** | 29 |
| 3.1 Introduction | 29 |
| 3.2 Related Techniques | 30 |
| 3.2.1 The Swin Transformer Network | 30 |
| 3.2.2 The Fourier Transform | 31 |
| 3.3 The Frequency–Spatial Coupled Inference Network Underwater Image Super-Resolution Reconstruction Model | 32 |
| 3.3.1 Network Architecture Design | 32 |
| 3.3.2 Frequency Awareness Module (SFAM) | 33 |
| 3.3.3 Texture–Structure Joint Loss | 34 |
| 3.4 Experimental Results and Analysis | 35 |
| 3.4.1 Experimental Data and Experimental Environment | 35 |
| 3.4.2 Evaluation Metrics | 36 |
| 3.4.3 Experimental Design and Implementation | 37 |
| 3.4.4 Quantitative Analysis | 37 |
| 3.4.5 Qualitative Analysis | 39 |
| 3.4.6 Ablation Experiments | 40 |
| 3.5 Chapter Summary | 41 |
| **Chapter 4 An Underwater Image Object Detection Method Based on an Improved YOLOv8** | 42 |
| 4.1 Introduction | 42 |
| 4.2 Related Techniques | 43 |
| 4.2.1 The YOLOv8 Object Detection Network | 43 |
| 4.2.2 Attention Mechanisms | 44 |
| 4.3 The Improved YOLOv8 Underwater Image Object Detection Model | 44 |
| 4.3.1 Network Architecture Design | 44 |
| 4.3.2 Channel–Spatial Adaptive Enhancement Module | 45 |
| 4.3.3 Multi-Scale Cross-Attention Fusion Module | 47 |
| 4.3.4 Mamba-Based Global Perception Module | 48 |
| 4.4 Experimental Results and Analysis | 49 |
| 4.4.1 Experimental Data and Experimental Environment | 49 |
| 4.4.2 Evaluation Metrics | 50 |

--- p.9 ---

v

| Entry | Page |
|---|---|
| 4.4.3 Experimental Design and Implementation | 51 |
| 4.4.4 Quantitative Analysis | 51 |
| 4.4.5 Qualitative Analysis | 53 |
| 4.4.6 Ablation Experiments | 55 |
| 4.5 Evaluation of Object Detection Performance on Super-Resolution Reconstructed Underwater Images | 56 |
| 4.6 Chapter Summary | 60 |
| **Chapter 5 Conclusions and Outlook** | 61 |
| 5.1 Conclusions | 61 |
| 5.2 Outlook | 62 |
| References | 63 |
| Acknowledgements | 70 |
| Appendix | 72 |

--- p.10 ---

*(blank page)*

--- p.11 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

1

## LIST OF FIGURES AND TABLES

| Figure | Page |
|---|---|
| Figure 1.1 Images captured in underwater scenes | 4 |
| Figure 1.2 Feature-matching test | 4 |
| Figure 1.3 Overall technical roadmap | 8 |
| Figure 1.4 Thesis organisation diagram | 9 |
| Figure 2.1 Artificial neural network | 11 |
| Figure 2.2 Multilayer perceptron | 12 |
| Figure 2.3 Convolution operation | 13 |
| Figure 2.4 Pooling operation | 14 |
| Figure 2.5 The Sigmoid function | 15 |
| Figure 2.6 The Tanh function | 15 |
| Figure 2.7 The ReLU function | 16 |
| Figure 2.8 The Transformer model | 17 |
| Figure 2.9 VSSM architecture diagram | 18 |
| Figure 2.10 2D selective scan module | 18 |
| Figure 2.11 The Jaffe–McGlamery underwater imaging process | 20 |
| Figure 2.12 Schematic of bilinear interpolation computation | 21 |
| Figure 2.13 Schematic of bicubic interpolation computation | 22 |
| Figure 2.14 Schematic of deconvolution upsampling | 22 |
| Figure 2.15 Schematic of sub-pixel upsampling | 23 |
| Figure 2.16 Flowchart of learning-based image super-resolution reconstruction methods | 23 |
| Figure 2.17 Structure diagram of two-stage image object detection | 26 |
| Figure 2.18 Structure diagram of one-stage image object detection | 26 |
| Figure 3.1 Schematic of the Swin Transformer structure | 30 |
| Figure 3.2 Swin Transformer schematic | 31 |
| Figure 3.3 Schematic of the Fourier transform (amplitude-spectrum and phase-spectrum decomposition) | 32 |
| Figure 3.4 Schematic of the overall FSCIN network structure | 33 |
| Figure 3.5 Concrete examples from the USR-248 and UFO-120 datasets | 35 |
| Figure 3.6 Visual comparison on the USR-248 dataset (×2/×4/×8) | 39 |
| Figure 3.7 Visual comparison on the UFO-120 dataset (×2/×3/×4) | 40 |
| Figure 4.2 Schematic of the improved YOLOv8 network structure | 45 |
| Figure 4.3 Schematic of the overall structure of the fine-grained feature extraction module | 45 |
| Figure 4.5 Schematic of the structure of the multi-scale cross-attention fusion module | 48 |
| Figure 4.6 Schematic of the structure of the Mamba-based global perception module (VSSM) | 49 |
| Figure 4.7 Sample images from the URPC2021 dataset | 50 |

--- p.12 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

2

| Figure | Page |
|---|---|
| Figure 4.8 Loss-function curves for YOLOv8 during training and validation | 53 |
| Figure 4.9 Loss-function curves for the improved YOLOv8 during training and validation | 53 |
| Figure 4.10 Comparison of object detection results between the original YOLOv8 and the improved YOLOv8 on the URPC2021 validation set | 55 |
| Figure 4.11 Heat-map visualisation effects of the different modules | 56 |
| Figure 4.12 Schematic of how FSCIN super-resolution reconstruction promotes improved-YOLOv8 underwater object detection | 57 |

| Table | Page |
|---|---|
| Table 3.1 ×2 comparison of different methods on the USR-248 dataset | 38 |
| Table 3.2 ×4 comparison of different methods on the USR-248 dataset | 38 |
| Table 3.3 ×8 comparison of different methods on the USR-248 dataset | 38 |
| Table 3.4 Quantitative evaluation of underwater image super-resolution on the UFO-120 dataset (×2/×3/×4) | 38 |
| Table 3.5 Ablation experiment on the effectiveness of the SFAM module (USR-248, ×2) | 40 |
| Table 3.6 Ablation experiment on the multi-modal loss function (UFO-120, ×2) | 41 |
| Table 4.1 Experimental environment configuration | 50 |
| Table 4.2 Comparison of detection performance on the URPC2021 dataset | 52 |
| Table 4.3 Ablation results for each sub-module of the fine-grained feature extraction module | 56 |

--- p.13 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

3

# Chapter 1 Introduction

## 1.1 Research Background and Significance

With the rapid development of fields such as marine resource exploitation, marine environmental monitoring and underwater engineering inspection, underwater vision technology has gradually become an important means of acquiring marine information. With the release of the *New Generation Artificial Intelligence Development Plan*, an explicit requirement was set for China to become the world's principal AI innovation centre by 2030, and this includes key technical fields such as deep learning and image processing. Against this backdrop, underwater vision technology has become a core means of acquiring marine information. Among these, the acquisition of high-quality underwater images is the prerequisite for achieving accurate object detection. By raising the resolution and level of detail of underwater images through super-resolution reconstruction technology, and then combining this with object detection methods, precise perception for biological identification, target localisation and resource surveying can be achieved in systems such as underwater robots, autonomous underwater vehicles (AUVs) and remotely operated vehicles (ROVs), providing reliable technical support for underwater scientific research and engineering.

The underwater imaging environment is complex, and light propagation is simultaneously affected by absorption and scattering. The absorption effect causes light of different wavelengths to attenuate at different rates; among them, blue light attenuates relatively slowly, causing images to exhibit a blue-green colour cast. The scattering effect deflects light from its original path: forward scattering blurs edge details, while backward scattering reduces contrast and sharpness. As a result, underwater images generally suffer from low contrast, colour distortion, blurred details and noise interference, which makes it difficult for traditional vision algorithms to accurately extract target features and limits the performance of detection systems, as shown in Figure 1.1. To cope with the complex interference of the underwater imaging environment, many scholars have taken a hardware approach and designed high-precision, high-speed cameras to improve image acquisition quality. Although such equipment reduces noise to a certain extent and mitigates the influence of the water body on imaging, the acquired images still lack fine detail and texture information and struggle to meet the requirements of subsequent object detection or analysis tasks; at the same time they are expensive, which is unfavourable for large-scale application. By contrast, underwater image super-resolution reconstruction technology can, without changing the original imaging equipment, restore details and textures lost in low-resolution images. This not only significantly improves image quality but also provides richer feature information for object detection, achieving effective coupling between image enhancement and target recognition, and thereby improving the accuracy and stability of underwater target localisation and recognition. As shown in Figure 1.2, processed underwater images can substantially increase the number of matched feature points.

--- p.14 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

4

**Figure 1.1 Images captured in underwater scenes**

(a) (b)

(a) Original image: 25 points correctly matched  (b) Restored image: 79 points correctly matched

**Figure 1.2 Feature-matching test**

In summary, this thesis proposes a complete underwater visual perception framework whose main thread is "original underwater image → super-resolution sharpening → high-quality clear image → object detection → detection result". This framework organically links the two modules of image quality improvement and object detection: first, a deep-learning-based super-resolution reconstruction method is used to enhance the originally degraded image, restoring its texture details, improving colour imbalance and raising contrast; then, with the high-quality clear image as input, an improved object detection model performs precise recognition and localisation of underwater targets. Experimental research shows that performing object detection after enhancement processing of underwater images can effectively improve the model's detection accuracy, thereby improving overall detection performance. Therefore, researching deep-learning-based underwater image super-resolution reconstruction and object detection methods has important theoretical significance and application value for improving the performance of underwater vision systems.

## 1.2 Research Status at Home and Abroad

### 1.2.1 Research Status of Underwater Image Super-Resolution Reconstruction

Image super-resolution (SR) reconstruction technology aims to recover high-resolution (HR) image detail from low-resolution (LR) images, and has important application value in fields such as medical imaging, remote sensing and underwater vision. With the rise of deep learning, super-resolution methods based on convolutional neural networks have achieved substantive breakthroughs. SRCNN, proposed by Dong et al., was the first to introduce convolutional neural networks into the field of image super-resolution;

--- p.15 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

5

through a three-layer convolutional structure it learns an end-to-end mapping from low-resolution to high-resolution images, establishing the foundational paradigm of deep learning super-resolution research [1]. VDSR, proposed by Kim et al., introduced global residual learning and used an extremely deep network structure to improve reconstruction accuracy [2]. Lim et al. designed the enhanced deep residual network EDSR, removing batch-normalisation layers and expanding network capacity, substantially improving performance on general super-resolution benchmarks [3]. RDN, proposed by Zhang et al., makes full use of hierarchical features through residual dense connections, achieving comprehensive recovery of multi-scale detail [4]; Zhang et al. further introduced a channel attention mechanism to propose RCAN, which adaptively weights the feature responses of different channels so that the network can selectively focus on the key information required for high-frequency reconstruction [5]. In terms of generative adversarial network applications, the GAN framework proposed by Goodfellow et al. provided a new avenue for improving super-resolution image quality [6]; SRGAN, proposed by Ledig et al., was the first to introduce GANs into image super-resolution reconstruction, introducing a perceptual loss function to drive the network to generate high-frequency visual detail [7]; building on this, Wang et al. proposed ESRGAN, which further enhanced the realism of texture reconstruction through residual dense blocks and a relativistic GAN loss, becoming an important benchmark for subsequent research [8]. Zhao Ran et al. proposed a medical ultrasound image super-resolution reconstruction method based on video multi-frame fusion, effectively improving reconstruction resolution through cross-frame integration of temporal information [9]; Ran Wenbing et al. combined generative adversarial networks with attention mechanisms, significantly improving the super-resolution reconstruction of medical images [10]. In the remote-sensing image field, Zhao Huiyan et al. proposed a GAN-based super-resolution analysis method for Sentinel-2 remote-sensing images [11]; Zhang Yan et al. proposed a high-resolution satellite image reconstruction scheme based on an HMRF prior model, improving the structural fidelity of reconstruction results by introducing Markov random field constraints [12]. The body of methods formed by the above work provides important reference for the underwater image super-resolution research of this thesis.

In research on underwater image quality improvement, early work relied mainly on physical imaging models for image restoration. Yang Aiping et al. proposed an underwater image restoration method based on colour-distortion removal and the dark channel prior, improving colour reproduction by estimating underwater light attenuation parameters [13]; Yang Aiping et al. further proposed a single-image underwater sharpening method based on multi-feature fusion, comprehensively exploiting colour, structural and texture features to achieve image enhancement — however, these methods lack robustness in scenes where water quality conditions are complex and highly variable [14]. Addressing the particular nature of underwater image degradation, researchers began to design specialised super-resolution methods for underwater scenes. Islam et al. constructed the USR-248 underwater image super-resolution dataset and proposed the SRDRM method, effectively restoring texture detail in underwater images through multi-scale residual learning [15]; Islam et al. further constructed the UFO-120 dataset and proposed a joint framework for simultaneous enhancement and super-resolution [16]. AMPCNet, proposed by Zhang et al., adaptively focuses on key regions of underwater targets through an attention-guided multi-path cross CNN [17]; Ren et al. proposed URSCT, fusing an enhanced Swin-Convs Transformer with a convolutional network to achieve collaborative optimisation of underwater image enhancement and super-resolution [18]; DeepWaveNet, proposed by Sharma et al., explicitly models the attenuation laws of light of different wavelengths in water and achieves excellent results in colour restoration [19]; Chen et al. proposed RDLN, which through multi-scale feature extraction combined with collaborative learning of long- and short-range dependencies effectively solves the problem of coexisting local distortion and global blur in underwater images [20]; Chen et al. proposed the Progressive Attention Learning (PAL) method, which restores underwater image detail in stages through a progressively refined attention strategy [21]; Cherian et al.

--- p.16 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

6

proposed the AlphaSRGAN method, achieving a good balance between detail restoration and perceptual quality [22]; Pramanick et al. proposed a multi-resolution, multi-scale attention underwater image restoration method, comprehensively exploiting features at different scales to achieve detail reconstruction [23]. Related research in 2026 further combines enhancement, saliency modelling and super-resolution reconstruction: DeFu-UIESR adopts a saliency-guided dual-branch decoupled fusion framework to handle underwater image enhancement and super-resolution simultaneously; the lightweight frequency-domain Transformer network proposed by Wu et al. improves reconstruction efficiency and detail fidelity from the perspective of frequency modelling [24][25].

In terms of frequency-domain modelling, Dharejo et al. proposed SwinWave-SR, combining the Swin Transformer with the wavelet transform to achieve lightweight, high-quality underwater image super-resolution reconstruction on the basis of multi-scale frequency decomposition [26]; the wavelet super-resolution method proposed by Chen et al. introduces wavelet-domain information into underwater image reconstruction, further enriching the technical approach to frequency-domain modelling [27]; Wang et al. introduced spatial–frequency mutual learning into super-resolution networks, significantly improving the reconstruction capability for fine textures through the coordinated combination of frequency-domain global modelling and spatial-domain local modelling, providing important reference for the frequency-domain/spatial-domain coupled design of this thesis [28]. From the perspective of image decomposition, Zhou et al. proposed a texture–structure-aware image decomposition neural network model, revealing the theoretical basis that an image can be expressed as the sum of a texture layer and a structure layer, which lays the theoretical foundation for the design of the texture–structure joint loss in this thesis [29]. In terms of Transformer architectures, the Swin Transformer proposed by Liu et al. achieves global information perception at linear computational complexity through a local-window attention mechanism, and has become one of the most important backbone networks for current visual super-resolution [30]; Liang et al. introduced the Swin Transformer into the image super-resolution framework to propose SwinIR, achieving then-leading reconstruction performance in general scenes [31]. In terms of underwater Transformer methods, Wang et al. proposed a frequency-domain Transformer-based underwater image restoration method [32]; Shen et al. proposed UDAformer, performing underwater image enhancement based on a dual-attention Transformer [33]; Peng et al. proposed a U-shaped Transformer applied to the underwater image enhancement task [34] — all of which provide new ideas for underwater image quality improvement from the perspective of global modelling.

In summary, existing super-resolution methods have made significant progress in general scenes, but the exploitation of frequency-domain priors for underwater images remains insufficient, and the decoupled supervision of the image texture layer and structure layer by loss functions is still imperfect. It is precisely these shortcomings that this thesis addresses by proposing the FSCIN network, which systematically improves underwater image super-resolution reconstruction quality along two dimensions — frequency-domain/spatial-domain collaborative modelling and a texture–structure joint loss — with its output serving directly as the high-quality input to the subsequent object detection module.

### 1.2.2 Research Status of Underwater Image Object Detection

Object detection is a core task in the field of computer vision, aiming to simultaneously accomplish the localisation and classification of targets in an image, and is in strong demand in applications such as underwater robot navigation, marine biological monitoring and underwater security. Current deep-learning object detection methods can be divided, according to their processing flow, into two major categories: two-stage detection and one-stage detection. In terms of two-stage detection methods, R-CNN, proposed by Girshick et al., generates candidate regions through selective search and uses a convolutional neural network to extract features, pioneering research into deep learning in the field of object detection [35]; Girshick further proposed Fast R-CNN, which significantly improved detection efficiency by sharing

--- p.17 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

7

convolutional feature maps [36]; Ren et al. proposed Faster R-CNN, which fuses a region proposal network (RPN) with the detection network end-to-end and made important advances in both accuracy and speed, becoming a milestone in two-stage detection methods [37]. The feature pyramid network (FPN) proposed by Lin et al. achieves multi-scale feature fusion through a top-down semantic path and a bottom-up positional information path, effectively improving detection capability for targets of different sizes, and has been widely integrated into various detection frameworks [38]. In underwater scenes, Jia et al. proposed an underwater object detection method based on an improved EfficientDet and compared multiple classes of detection model on datasets such as URPC, verifying the effectiveness of feature enhancement and multi-scale fusion for target recognition in complex underwater scenes, laying a foundation for subsequent underwater detection research [39].

In terms of one-stage detection methods, YOLO (You Only Look Once), proposed by Redmon et al., models object detection as a regression problem solved in a single forward inference pass, outputting target position and category simultaneously in an end-to-end manner and achieving a breakthrough improvement in detection speed [40]. Thereafter the YOLO series continued to iterate and evolve: Bochkovskiy et al. proposed YOLOv4, introducing the CSP cross-stage partial connection network and a variety of data augmentation strategies [41]; Jocher et al. proposed YOLOv5, improving engineering deployability through a lightweight design [42]; YOLOv8, proposed by Jocher et al., adopts the C2f module in place of the original C3 module, introduces a decoupled detection head and optimises the PAN-FPN structure, achieving comprehensive performance that balances accuracy and efficiency on general object detection tasks, and has been widely applied in various engineering scenarios [43]. Among one-stage methods developed in parallel with YOLO, SSD, proposed by Liu et al., achieves better multi-scale target coverage through dense prediction on multi-scale feature maps [44]; RetinaNet, proposed by Lin et al., introduced Focal Loss to solve the problem of extreme positive/negative sample imbalance in one-stage detection, substantially improving detection accuracy [45]. In terms of feature enhancement and attention mechanisms, SENet, proposed by Hu et al., applies adaptive weights to different semantic channels through a channel attention mechanism [46]; CBAM, proposed by Woo et al., cascades spatial attention on top of channel attention, further guiding the network to focus on salient target regions and effectively suppressing interference from underwater background clutter [47]. Recent underwater object detection research has further centred on small targets, complex backgrounds and multi-scale feature fusion: YOLO-Starfish improves starfish target detection accuracy through an improved YOLOv8, while YOLO-MFD introduces a dynamic detection head and a multi-scale feature fusion strategy for complex underwater environments, providing reference for the subsequent object detection improvements in this thesis [48][49].

In terms of Transformer-based detection methods, the Vision Transformer (ViT) proposed by Dosovitskiy et al. divides an image into a sequence of patches which are fed into a Transformer encoder, establishing long-range dependencies between pixels through a global self-attention mechanism and providing stronger global context modelling capability for visual detection tasks [50]; Carion et al. proposed DETR based on the Transformer, achieving object detection in an end-to-end manner and eliminating complex post-processing steps such as traditional anchor-box design and non-maximum suppression [51]; Zhu et al. further proposed Deformable DETR, introducing a deformable attention mechanism to solve the problems of slow convergence and weak small-target detection [52]. However, the quadratic computational complexity of the Transformer still poses challenges for deployment on real-time embedded underwater platforms. Addressing this limitation, state space models (SSMs) represented by Mamba provide a new technical path: the structured state space model (S4) proposed by Gu et al. demonstrated the feasibility of SSMs capturing long-range dependencies in long-sequence modelling with

--- p.18 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

8

linear complexity [53]; Mamba, proposed by Gu and Dao, introduces a selective scan mechanism and, through an input-adaptive parameter update strategy, achieves more efficient global information modelling than the standard Transformer, replacing the Transformer's O(L²) with linear O(L) complexity and providing an effective modelling tool for the global blur problem in underwater images caused by scattering [54].

In summary, existing underwater object detection methods have achieved good results in general scenes, but clear limitations remain in three areas: fine-grained perception of small targets, global dependency modelling, and adaptive multi-scale feature fusion. It is particularly worth noting that the low contrast and texture degradation inherent in underwater images directly weaken the feature extraction capability of detection networks, and improving the detection model structure alone cannot fundamentally solve the problem of insufficient input image quality. Therefore, this thesis unifies the two tasks of super-resolution enhancement and object detection within the complete processing framework "original image → sharpening → clear image → object detection → detection result", collaboratively improving the overall performance of the underwater object detection system along the two dimensions of input quality and model capability.

## 1.3 Main Work of This Thesis

Addressing problems such as underwater image quality degradation and insufficient object detection accuracy, this thesis conducts research centred on underwater image super-resolution reconstruction and object detection, and constructs an underwater visual perception framework with the complete processing chain "original underwater image → super-resolution sharpening → high-quality clear image → object detection → detection result", as shown in Figure 1.3. The core logic of this framework is: in the first stage, super-resolution enhancement compensates for the effects of underwater degradation at the image-quality level; in the second stage, object detection is performed on the basis of the high-quality image. The cascaded collaboration of the two improves overall system performance. The specific research route is shown in Figure 1.3 below.

**Figure 1.3 Overall technical roadmap**

First, addressing degradation problems present in underwater images such as insufficient contrast, blurred detail and colour deviation, the Frequency-domain–Spatial-domain Coupled Inference Network (FSCIN) is proposed, and a spatial–frequency awareness module (SFAM) is designed that combines the fast Fourier transform with

--- p.19 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

9

the spatial-domain encoding of the Swin Transformer, achieving deep fusion of frequency-domain global priors and spatial-domain local features; at the same time, a texture–structure joint loss function is introduced which applies targeted constraints to the image texture layer and structure layer separately, significantly improving the perceptual quality and detail fidelity of underwater images. The high-quality clear images output by FSCIN serve directly as the input to the object detection stage, forming the front-end processing module of the overall framework.

Second, on the basis of the high-quality clear images output by FSCIN, targeted improvements are made to the YOLOv8 model: a fine-grained feature extraction module (FFEM) is designed to replace the original C2f module. This module is built collaboratively from three sub-modules — the channel–spatial adaptive enhancement module, the Mamba-based global perception module, and the multi-scale cross-attention fusion module — which respectively improve the detection capability for underwater targets along three dimensions: local fine-grained perception, global long-range dependency modelling, and dynamic cross-scale feature fusion.

Finally, through systematic experiments on the public datasets USR-248, UFO-120 (super-resolution reconstruction) and URPC2021 (object detection), the effectiveness of FSCIN and of the improved YOLOv8 is verified respectively, and the actual improvement effect of super-resolution pre-processing on object detection performance is analysed, in order to quantitatively evaluate the overall benefit of the "enhancement–detection" cascaded framework.

## 1.4 Thesis Organisation

This thesis conducts research centred mainly on underwater image super-resolution reconstruction and object detection methods; the structure of the thesis is arranged as shown in Figure 1.4.

**Figure 1.4 Thesis organisation diagram**

--- p.20 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

10

**Chapter 1** is the introduction. It presents the research background and significance, reviews the research status at home and abroad in the two directions of underwater image super-resolution reconstruction and object detection, clarifies the overall technical thinking behind this thesis's "enhancement–detection" cascaded framework, and sets out the main research content and organisational structure of the thesis.

**Chapter 2** covers related theoretical foundations. It introduces the underwater image degradation model, the principles of super-resolution reconstruction, and the core deep learning modules (including convolutional neural networks, the Transformer model, the Mamba model and object detection theory), providing theoretical support for subsequent chapters.

**Chapter 3** is the first-stage work of this thesis's "enhancement–detection" framework. It proposes an underwater image super-resolution reconstruction method based on the Frequency-domain–Spatial-domain Coupled Inference Network (FSCIN), and details the network structure design, the core SFAM module and the texture–structure joint loss. The high-quality clear images output by this chapter serve directly as the input to the object detection of Chapter 4, forming the front-end processing module of the overall framework.

**Chapter 4** is the second-stage work of this thesis's "enhancement–detection" framework. On the basis of the super-resolution enhanced images of Chapter 3, it proposes an underwater object detection method based on an improved YOLOv8, and details the design and experimental verification of the FFEM module.

**Chapter 5** summarises the work of the whole thesis, analyses the collaborative role of the two core modules within the complete "enhancement–detection" framework, and offers an outlook on future research directions.

--- p.21 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

11

# Chapter 2 Related Theoretical Foundations

## 2.1 Theoretical Foundations of Deep Learning

### 2.1.1 Convolutional Neural Networks

**(1) Basic principles**

As shown in Figure 2.1, an artificial neural network (ANN) is a class of computational model established by simulating the information-processing mechanisms of biological nervous systems. Its core idea is to achieve the modelling and learning of complex data through the connection relationships among a large number of neurons. A neuron typically receives multiple input signals, computes their weighted sum, and then obtains an output result after mapping through a non-linear activation function. Here *xᵢ* denotes the *i*-th input signal, *wᵢ* denotes the corresponding weight parameter, *b* is the bias term, and *f*(·) is the non-linear activation function.

This computational process can be expressed as:

$$y = f\left(\sum_{i=1}^{n} x_i w_i + b\right) \tag{2.1}$$

As research has deepened, scholars have successively proposed a variety of neural network structures, such as the perceptron, the Boltzmann machine, the restricted Boltzmann machine and the multilayer perceptron. In 1986, Rumelhart et al. applied the back propagation (BP) algorithm to the training process of the multilayer perceptron, enabling neural networks to automatically adjust weight parameters through gradient descent, which significantly advanced the development of neural networks in the field of machine learning [55].

*[Figure content: x₁, x₂, … xₙ — Input | Weights w₁, w₂, … wₙ | Neuron f | b | Output y]*

**Figure 2.1 Artificial neural network**

A BP network is usually composed of an input layer, hidden layers and an output layer. In the forward propagation stage, input data is passed layer by layer and generates a prediction result; if an error exists between the predicted value and the true value, that error is passed back layer by layer through the back-propagation mechanism, while network parameters are updated using a gradient-descent strategy, so that after multiple iterations the error is gradually reduced. However, when the number of network layers is large, the BP algorithm is prone to problems such as vanishing or exploding gradients, which affects model training performance.

To overcome the limitations of traditional neural networks in image processing tasks, LeCun et al. proposed the convolutional neural network (CNN). This model draws on the concept of the "receptive field"

--- p.22 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

12

from the biological visual system, and through local connectivity and weight-sharing mechanisms significantly reduces the number of model parameters while improving feature extraction capability [56]. Compared with traditional fully connected networks, CNNs can more efficiently capture local structural information in images, such as edges, textures and shapes, and are therefore widely applied in the field of computer vision. In addition, He et al. proposed the residual network (ResNet), alleviating the degradation problem in training deep networks through residual connections [57]. Kim et al. proposed the deeply-recursive convolutional network (DRCN), using a recursive structure to enlarge the receptive field and enhance feature representation [58]. Huang et al. proposed DenseNet, strengthening feature reuse and gradient propagation through dense connections [59]. Tong et al. introduced dense skip connections into the image super-resolution task, proposing SRDenseNet to improve the reconstruction capability for high-frequency detail [60].

*[Figure content: Input layer (x₁, x₂, … xₙ) — Hidden layer (weights wᵢⱼ, wⱼₖ; nodes i, j, k) — Output layer (y₁, y₂, y₃)]*

**Figure 2.2 Multilayer perceptron**

**(2) Basic structure**

A convolutional neural network is generally composed of convolutional layers, pooling layers, activation function layers and fully connected layers, which cooperate with one another to achieve the progressive extraction of information from low-level features to high-level semantics.

**Convolutional layer**

The convolutional layer is the most critical component of a convolutional neural network; its main role is to automatically extract feature information from the input image. This process simulates the human visual system's mechanism of attending to local regions, allowing the model to focus on important information regions in the image. Multiple convolutional layers are stacked one after another in a hierarchical structure, thereby progressively completing the extraction process from shallow features to deep features.

In the shallow stages of the network, convolutional layers mainly capture low-level features in the image, such as colour variation and texture structure; as network depth increases, convolutional layers gradually learn higher-level abstract features, such as the shape and semantic information of targets. Each convolutional layer is usually composed of multiple convolution kernels; a common kernel size is 3×3, which effectively reduces the number of parameters while guaranteeing representational capability, and is therefore widely used.

Let the input matrix be *I*, the convolution kernel be *K* with kernel size *m*×*n*, the output feature map be *O*, and * denote the convolution operation; then the two-dimensional convolution operation can be expressed as:

$$O(i,j) = (K * I)(i,j) = \sum_m \sum_n I(i-m, j-n) K(m,n) \tag{2.2}$$

--- p.23 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

13

In actual computation, convolutional neural networks generally use the cross-correlation operation, whose expression can be written as:

$$O(i,j) = (K * I)(i,j) = \sum_m \sum_n I(i+m, j+n) K(m,n) \tag{2.3}$$

The convolution process is illustrated in Figure 2.3. The size of the output feature map is usually smaller than the input size; it is computed as follows:

$$h_{out} = \frac{h_{in} - k + 2p}{s} + 1; \quad w_{out} = \frac{w_{in} - k + 2p}{s} + 1 \tag{2.4}$$

where: *h_in*, *w_in* are the input feature map dimensions; *h_out*, *w_out* are the output feature map dimensions; *k* is the convolution kernel size; *p* is the padding size; and *s* is the stride. Because edge pixels participate in the computation fewer times, boundary information may be lost; therefore, in practical applications zeros are usually padded at the boundary of the input image to mitigate the problem of missing edge information.

*[Figure content: a 6×6 input matrix of values 2 and 4, convolved (*) with a 3×3 kernel of columns 1, 0, −1, producing an output matrix with values −2, −4, −6, 0, 2, 4, 6. Labels: Input | Convolution kernel | Output]*

**Figure 2.3 Convolution operation**

**Pooling layer**

When the number of convolutional layers increases, the network generates a large number of feature maps, which not only significantly increases computational complexity but may also lead to excessive storage overhead. For this reason, pooling layers are introduced to down-sample the feature maps, thereby reducing feature dimensionality and lowering the computational burden. Pooling operations usually shrink the spatial dimensions of the feature map, for example reducing the width and height to one half of the original, thereby reducing the number of model parameters. At the same time, pooling layers can also enlarge the receptive field and improve the model's robustness to image translation. Common pooling methods mainly include: **average pooling**, which takes the mean of the pixels within a region and can preserve overall background information; and **max pooling**, which selects the maximum value within a region and is more conducive to highlighting salient features.

The pooling operation is illustrated in Figure 2.4.

--- p.24 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

14

*[Figure content: a 6×6 input matrix (values 0, ±2, ±4, ±6) is reduced by average pooling to a 3×3 matrix (−0.5, −1.5, 3 / −2.5, −2.5, 5 / −0.5, 0.5, 1) and by max pooling to a 3×3 matrix (0, 0, 4 / 0, 0, 6 / 0, 0, 2). Labels: Average pooling | Max pooling]*

**Figure 2.4 Pooling operation**

**Fully connected layer**

The fully connected layer is usually located at the end of a convolutional neural network; its main function is to map the features extracted by the preceding convolutional layers into the final classification result. In this layer, every neuron establishes a connection with all neurons of the previous layer, thereby achieving global information integration. Increasing the number of neurons in the fully connected layer can improve the model's representational capability, but at the same time significantly increases computational cost and may lead to model overfitting. Therefore, in practical design a trade-off must be made between model performance and complexity.

**Activation function layer**

The convolution operation is essentially a linear transformation, and relying on linear operations alone makes it difficult to describe complex data distribution relationships. Therefore, activation functions are introduced into convolutional neural networks to enhance the model's non-linear representational capability so that it can handle more complex tasks. Common activation functions are as follows:

**Sigmoid function:**

$$\sigma(x) = \frac{1}{1 + e^{-x}} \tag{2.5}$$

This function takes the shape of an "S" curve, as illustrated in Figure 2.5. It can compress the input into the interval (0,1), which helps stabilise model output. However, when the input value is too large or too small, the gradient of the function approaches 0, which easily leads to the vanishing gradient problem. In addition, its output mean is not 0, which reduces the network's convergence speed.

--- p.25 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

15

*[Figure: plot of the Sigmoid curve]*

**Figure 2.5 The Sigmoid function**

**Tanh function:**

$$\text{Tanh}(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}} \tag{2.6}$$

The shape of this function is similar to the Sigmoid function, as illustrated in Figure 2.6. Its output range is (−1,1) and its mean is 0, which improves training efficiency to a certain extent. However, it likewise exhibits the vanishing gradient phenomenon over large input ranges, and its computational complexity is relatively high.

*[Figure: plot of the Tanh curve]*

**Figure 2.6 The Tanh function**

**ReLU function:**

$$f(x) = \max(0, x) \tag{2.7}$$

--- p.26 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

16

The ReLU function is simple to compute — its function plot is shown in Figure 2.7 — and its gradient is constantly 1 when *x* > 0, so it can effectively alleviate the vanishing gradient problem and improve computational efficiency. However, when the input is negative, a neuron may remain inactive for a long time, giving rise to the "dying neuron" phenomenon.

*[Figure: plot of the ReLU curve]*

**Figure 2.7 The ReLU function**

### 2.1.2 The Transformer Model

In 2017, Vaswani et al. proposed the Transformer model, whose overall structure is shown in Figure 2.8. This model significantly improved processing efficiency and result accuracy in sequence-modelling tasks such as machine translation [61].

Within the Transformer structure, the self-attention mechanism is the most core component. This mechanism achieves information interaction by constructing a query vector *Q*, a key vector *K* and a value vector *V*. Here, *Q* is used to represent the word currently requiring attention, *K* is used to represent the positional features of each word in the sequence, and *V* contains the specific semantic information. All three vectors are obtained from the input data through linear transformation. Finally, the computational form of self-attention is as follows:

$$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_K}}\right)V \tag{2.8}$$

where: *Kᵀ* is the transpose of vector *K*; the inner product of *Q* and *K* is used to measure the correlation between the current word and other positions, and this result reflects the degree of connection between the word being processed and each position in the sequence. √*d_K* is a scaling factor used to prevent the inner-product values from becoming too large and affecting training stability, and softmax is used to normalise the weights. Finally, the normalised result is multiplied with *V*, thereby obtaining an output representation containing contextual information. On this basis, the Transformer further introduces the multi-head attention mechanism, which computes attention results in parallel across multiple subspaces, captures the relationships between features from different perspectives, and finally concatenates and fuses them to form the final output of the Transformer module.

--- p.27 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

17

*[Figure: the Transformer architecture diagram]*

**Figure 2.8 The Transformer model**

Following the Transformer's success in the field of natural language processing, Dosovitskiy et al. proposed the Vision Transformer (ViT) model in 2020 [50], extending this structure to computer vision tasks such as image classification and semantic segmentation, and achieving performance comparable to mainstream convolutional neural networks. Thereafter, the Transformer gradually became one of the important research directions in the visual field, demonstrating potential superior to traditional CNN models in multiple tasks.

Unlike convolutional neural networks, which rely on local receptive fields, the Vision Transformer can directly establish global relationships among input features through the self-attention mechanism, thereby characterising the contextual information of the image more comprehensively. This globally-modelled approach gives the model stronger representational capability when processing complex scenes.

In terms of specific implementation, the Transformer generally adopts a multi-head self-attention mechanism, mapping input features into multiple subspaces for parallel computation so as to obtain attention distributions under different dimensions. The computation results of the various subspaces are subsequently concatenated and fused, thereby improving the model's capability to characterise feature relationships. In addition, because self-attention itself has no capability to perceive positional information, positional encoding must be additionally introduced to supplement the spatial or ordinal information in the sequence.

Although the Transformer possesses good modelling capability, the computational complexity of its self-attention grows quadratically with the length of the input sequence. When the sequence length is *L*, the computational complexity of multi-head self-attention is O(N · L²d), where *d* denotes the feature dimension. This computational characteristic entails considerable resource consumption when processing high-resolution images. To alleviate this problem, Dosovitskiy et al. proposed dividing the image into multiple patches as input, thereby reducing the computational scale. However, in high-resolution tasks requiring fine-grained modelling, this method still has certain limitations.

### 2.1.3 The Mamba Model

In recent years, with the widespread application of long-sequence modelling tasks in the fields of natural language processing and computer vision, traditional attention-based models have gradually exposed their limitations in terms of computational complexity. Addressing this problem, modelling methods based on visual state space models (Visual SSM, VSSM) have gradually attracted researchers' attention. Against this background, Gu et al. proposed the Mamba model, which achieves efficient modelling of long-sequence data by introducing a selective state space mechanism [54]; its structure diagram is shown in Figure 2.9. The figure shows that input features are processed through two parallel paths. In the first path, the feature channels are first expanded through a linear mapping, then processed by depth-wise convolution and a SiLU activation function, and finally further processed by the 2D Selective Scan Module (2D-SSM) and a LayerNorm layer. In the second path, the input features first undergo linear mapping and an activation function.

--- p.28 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

18

The outputs of the two paths are fused through a Hadamard product, and then projected back to the original channels through a linear mapping, yielding the final output features.

*[Figure content: Path 1 — Linear → DWConv → SiLU → 2D SSM → LN; Path 2 — Linear → SiLU; the two merge into Linear]*

**Figure 2.9 VSSM architecture diagram**

*[Figure content: a 2×2 patch grid (1 2 / 3 4) is unfolded into four 1-D scan sequences (1 2 3 4 / 1 3 2 4 / 4 2 3 1 / 4 3 2 1), which are then summed (Sum) and folded back. Labels: unfold | Sum]*

**Figure 2.10 2D selective scan module**

As shown in Figure 2.10, the two-dimensional image features are first unfolded into one-dimensional sequences along four scanning directions, and then discrete state space equations are used to perform long-range dependency modelling on the sequences. Finally, the sequences from each direction are summed and reshaped back into the original two-dimensional feature format. This design can effectively preserve image spatial information while enhancing feature extraction capability. Its basic form can be expressed as:

$$h_t = A \cdot h_{t-1} + B \cdot x_t \tag{2.9}$$

$$y_t = C \cdot h_t + D \cdot x_t \tag{2.10}$$

where *x_t* denotes the input sequence, *h_t* denotes the hidden state, *y_t* denotes the output result, and *A*, *B*, *C*, *D* are model parameter matrices. Through the above recurrence relations, the model can progressively update the state along the temporal dimension, thereby capturing long-term dependency information in the sequence.

Compared with the traditional Transformer model, the core innovation of Mamba lies in the introduction of the selective scan mechanism. This mechanism can dynamically modulate the state-update process according to the input features, causing the model to pay more attention to key information during sequence modelling, thereby breaking through the problems of fixed parameters and limited representational capability found in traditional state space models.

In terms of computational complexity, self-attention in the Transformer must model interactions between any two positions in the sequence, with complexity O(L²); Mamba, on the other hand, completes state updates through a linear recurrence, reducing the complexity to O(L), where *L* denotes the sequence length. Therefore, Mamba has lower computational overhead and memory footprint when processing long sequences or high-resolution visual features.

--- p.29 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

19

From the perspective of modelling capability, Mamba possesses the advantages of both local feature extraction and global dependency modelling. On the one hand, its state-update process can capture local contextual information; on the other hand, the state-transfer mechanism can accumulate long-range information along the sequence dimension. For the two-dimensional spatial structure of images, the 2D selective scan module further performs bidirectional scanning along the horizontal and vertical directions, covering spatial dependency relationships more fully while maintaining linear complexity.

Therefore, Mamba is suitable for complex visual tasks such as underwater image enhancement and object detection. Underwater images generally suffer from problems such as low contrast, strong noise interference and blurred target edges, and require a model to possess both fine-grained feature perception and global structural understanding capabilities. Although Mamba's performance in visual tasks still depends on the specific network structure design, combining it with convolutional networks or attention structures can achieve a good balance between computational efficiency and feature representation capability.

## 2.2 Theoretical Analysis of Underwater Image Super-Resolution

### 2.2.1 Underwater Image Degradation Model

In the underwater environment, the process of light propagation is jointly affected by absorption effects and scattering effects; these two factors are the main causes of the decline in underwater image quality. The absorption effect refers to the fact that when light propagates through a body of water, part of its energy is absorbed by water molecules and by substances dissolved in the water, causing the light intensity to gradually attenuate. Because light of different wavelengths is absorbed at different rates in water — for example, blue light attenuates relatively slowly — underwater images generally exhibit a pronounced blue-green colour cast. The scattering effect occurs when light encounters suspended particles or other minute substances in the water during propagation, causing its direction of propagation to change and thereby producing phenomena such as blurring or brightness variation in the image. The Jaffe–McGlamery underwater image imaging model is shown in Figure 2.11. According to the direction of scattering, it can be divided into two forms: forward scattering and backward scattering. Forward scattering changes the propagation path of light, making image edges blurred, while backward scattering reflects part of the light back to the camera equipment, producing a halo effect and reducing image clarity. Taking both light absorption and scattering into comprehensive consideration, the underwater image degradation process can generally be described by the classical underwater imaging model, whose mathematical expression is as follows:

$$I(x,y) = J(x,y)T(x,y) + A(1 - T(x,y)) \tag{2.11}$$

where *I*(*x*,*y*) denotes the observed degraded underwater image, *J*(*x*,*y*) denotes the ideal clear scene image, *T*(*x*,*y*) denotes the transmission map, used to describe the attenuation ratio of light during propagation; *A* denotes the background light intensity, used to represent the portion of scattered light entering the camera equipment; and *x*, *y* denote the position coordinates of the image pixel.

The transmission map *T*(*x*,*y*) is usually related to the attenuation characteristics of the water body and the distance between the object and the camera equipment; its expression can be further written as:

$$T(x,y) = e^{-\beta(d(x,y))} \tag{2.12}$$

where β denotes the total attenuation coefficient of the water body, which is generally composed of the light absorption coefficient *a* and the scattering coefficient *b*, i.e. β = *a* + *b*; *d*(*x*,*y*) denotes the propagation distance of light in the water body, which is usually related to the depth of the underwater scene and the observation angle.

--- p.30 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

20

From the above model it can be seen that the degradation of underwater image quality mainly originates from light-energy attenuation and scattering interference; therefore, when performing underwater image processing, it is necessary to restore the true scene information through corresponding algorithms in order to improve image quality.

*[Figure: the Jaffe–McGlamery underwater imaging process]*

**Figure 2.11 The Jaffe–McGlamery underwater imaging process**

### 2.2.2 Principles of Underwater Image Super-Resolution Reconstruction

During acquisition, underwater images often suffer from problems such as low resolution, missing detail and insufficient texture information; it is therefore necessary to reconstruct the image through super-resolution technology in order to obtain higher-quality visual information. Super-resolution reconstruction refers to the process of recovering a high-resolution image from a low-resolution image through an algorithm; its core objective is to reconstruct the high-frequency detail information in the image so that it appears visually clearer. At present, image super-resolution reconstruction methods are mainly divided into traditional interpolation methods and deep-learning-based methods. Throughout the development of image super-resolution technology, interpolation-based methods have consistently held an important position. Their core idea is to estimate and fill in unknown pixel values between known pixel points through mathematical interpolation, thereby achieving an increase in image resolution.

**(1) Bilinear interpolation**

Bilinear interpolation is a method of interpolating in two-dimensional space, computing the value of the target pixel by performing linear interpolation separately in two directions. Specifically, for a pixel requiring interpolation, bilinear interpolation first considers the four neighbouring pixels around that pixel. It then performs one linear interpolation in the horizontal direction on each of the two pairs of adjacent pixels, and subsequently performs one linear interpolation in the vertical direction on the two interpolation results obtained, thereby obtaining the interpolation result for the target pixel.

--- p.31 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

21

A schematic of the computation is shown in Figure 2.12; the computational process is as follows. Suppose the value of the desired pixel *R*(*x*, *y*) is required, and the values of the four points around this pixel — *P*₁₁(*x*₁, *y*₁), *P*₁₂(*x*₁, *y*₂), *P*₂₁(*x*₂, *y*₁), *P*₂₂(*x*₂, *y*₂) — are known; then linear interpolation is performed on these four points in the *x* direction to obtain *Q*₁ and *Q*₂:

$$Q_1 = f(P_{11}) \frac{x_2 - x}{x_2 - x_1} + f(P_{21}) \frac{x - x_1}{x_2 - x_1} \tag{2.13}$$

$$Q_2 = f(P_{12}) \frac{x_2 - x}{x_2 - x_1} + f(P_{22}) \frac{x - x_1}{x_2 - x_1} \tag{2.14}$$

Then linear interpolation is performed on *Q*₁ and *Q*₂ in the *y* direction to obtain the value of *R*(*x*, *y*):

$$R = Q_1 \frac{y_2 - y}{y_2 - y_1} + Q_2 \frac{y - y_1}{y_2 - y_1} \tag{2.15}$$

*[Figure content: points P₁₁, P₁₂, P₂₁, P₂₂ with intermediate points Q₁, Q₂ and target R, on axes x (x₁, x₂) and y (y₁, y₂)]*

**Figure 2.12 Schematic of bilinear interpolation computation**

**(2) Bicubic interpolation**

Compared with bilinear interpolation, bicubic interpolation can provide smoother edges and higher image quality in image enlargement and reduction processing. The specific operation is as follows: for a pixel *P*(*x*, *y*) requiring interpolation, the values of the nearest sixteen adjacent pixels must be comprehensively considered, and one cubic interpolation is performed in each of the two directions to obtain the final value.

A schematic of the computation is shown in Figure 2.13; the computational process is as follows:

$$W_x = \begin{cases} (a+2)|x|^3 - (a+3)|x|^2 + 1 & \text{for } |x| \le 1 \\ a|x|^3 - 5a|x|^2 + 8a|x| - 4a & \text{for } 1 < |x| < 2 \\ 0 & \text{otherwise} \end{cases} \tag{2.16}$$

where *W_x* is the interpolation kernel function formula. According to the above formula, the values *W_x* for the four adjacent pixels along the *x* axis can be computed; similarly, the values *W_y* for the four adjacent pixels along the *y* direction can be obtained. The interpolation formula for *P*(*x*, *y*) can then be expressed as follows:

--- p.32 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

22

$$P = W_x \cdot Q \cdot W_y^T \tag{2.17}$$

$$W_x = [W_{x1}\ W_{x2}\ W_{x3}\ W_{x4}] \tag{2.18}$$

$$W_y = [W_{y1}\ W_{y2}\ W_{y3}\ W_{y4}] \tag{2.19}$$

$$Q = \begin{bmatrix} Q_{11} & Q_{12} & Q_{13} & Q_{14} \\ Q_{21} & Q_{22} & Q_{23} & Q_{24} \\ Q_{31} & Q_{32} & Q_{33} & Q_{34} \\ Q_{41} & Q_{42} & Q_{43} & Q_{44} \end{bmatrix} \tag{2.20}$$

*[Figure content: a 4×4 grid of points Q₁₁ … Q₄₄ with the interpolated point P, kernel W(x), and axes x₁–x₄, y₁–y₄]*

**Figure 2.13 Schematic of bicubic interpolation computation**

**(3) Deconvolution upsampling**

Deconvolution is a distinctive form of convolution used to predict the corresponding high-resolution image from low-resolution image feature maps [62]. The specific operational process is as follows: it begins with edge padding to proportionally enlarge the feature map size, and then performs a convolution operation with a convolution kernel and stride of appropriate size, so as to produce an HR image of the expected dimensions. The computational process of deconvolution upsampling is shown in Figure 2.14. In the figure, the blue grid represents the input LR image feature map, while the green rectangle represents the convolution operation. Deconvolution upsampling combines the characteristics of traditional convolution with the advantages of end-to-end image reconstruction, and has been widely applied in the field of image super-resolution. However, if the convolution kernel size and stride are not proportional, non-uniform aliasing phenomena may arise in the generated image.

*[Figure: deconvolution upsampling schematic]*

**Figure 2.14 Schematic of deconvolution upsampling**

**(4) Sub-pixel upsampling**

The sub-pixel upsampling technique provides a viable upsampling strategy based on end-to-end learning [63]. This method uses convolution operations to increase the number of channels and recombines pixels at the channel level to achieve enlargement of the spatial dimensions. The specific

--- p.33 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

23

computational flow is shown in Figure 2.15. Taking the feature map of a low-resolution image as an example, with input dimensions set to *h* × *w* × *c* and scale factor *s*, this technique first uses a convolution operation to generate *s*² times the number of channels, at which point the feature map dimensions become *h* × *w* × *s*²*c*. Subsequently, a channel-recombination operation is performed; through a periodic screening approach this step fills the pixels from the newly generated channels into the original feature map, thereby achieving enlargement of width and height and reducing the feature map dimensions from *h* × *w* × *s*²*c* to *sh* × *sw* × *c*, completing the *s*-fold enlargement process.

*[Figure: sub-pixel upsampling schematic]*

**Figure 2.15 Schematic of sub-pixel upsampling**

With the development of deep learning, the basic idea of learning-based image super-resolution reconstruction methods is to draw on machine learning theory to learn the mapping relationship between LR images and their corresponding HR images from a large number of training examples, thereby recovering the high-frequency information lost in the LR image and achieving the goal of reconstructing an HR image; the method's flow is shown in Figure 2.16. This method achieves reconstruction of image detail information by learning the non-linear mapping relationship between low-resolution images and high-resolution images.

*[Figure: flowchart of learning-based image super-resolution reconstruction]*

**Figure 2.16 Flowchart of learning-based image super-resolution reconstruction methods**

Suppose the training dataset contains a set of samples {(*Iᵢ*, *Jᵢ*)}ᵢ₌₁ᴺ, where *Iᵢ* denotes the *i*-th low-resolution underwater image and *Jᵢ* denotes the corresponding high-resolution image. The objective of the super-resolution model is to learn a mapping function *f*(*I*; θ), thereby achieving the conversion from the low-resolution image *I* to the high-resolution image *Ĵ*:

$$\hat{J} = f(I; \theta) \tag{2.21}$$

where *f* denotes the deep learning model and θ denotes the model parameters, including the convolution kernel weights and bias parameters within the network.

--- p.34 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

24

In the actual deep learning model *f*, image features are first extracted through a multi-layer convolutional network. Assuming the network contains *L* convolutional layers, the output of the *L*-th convolutional layer can be expressed as:

$$F_l = \sigma(W_l * F_{l-1} + b_l) \tag{2.22}$$

$$F_0 = I \tag{2.23}$$

where *F_l* denotes the feature map generated by layer *l*, *F_{l−1}* is the input feature map from the previous layer, *W_l* and *b_l* respectively denote the weight parameters and bias term of the *l*-th layer's convolution kernel, σ is the non-linear activation function (for example the ReLU function), and ∗ denotes the convolution operation.

Through layer-by-layer convolution operations, the network can progressively extract texture, edge and semantic feature information from the image. After feature extraction is complete, the network must progressively raise the spatial resolution of the feature maps through upsampling modules so that they approach the target high-resolution image. Common upsampling methods include transposed convolution (deconvolution), pixel shuffle, and interpolation upsampling. Among them, PixelShuffle achieves efficient reconstruction through sub-pixel convolution [63]. Wavelet direction-adaptive interpolation provides a frequency-domain modelling reference for traditional interpolation upsampling [64]. After the upsampling operation, the final convolutional layer maps the feature map into the final predicted high-resolution image. In the model training stage, a loss function must be constructed to measure the degree of difference between the model output and the true high-resolution image. By minimising this loss function, the model parameters can be continually optimised so that the predicted image gradually approaches the true image.

During training, the back-propagation algorithm is generally used to compute the gradient of the loss function with respect to the model parameters, and an optimisation algorithm is used to update the parameters θ. The model parameter update process usually begins from random initialisation, and through continuous iterative adjustment of the parameters the loss function is gradually reduced. When the model's performance on the validation set stabilises — that is, when the loss value no longer decreases significantly — the training process can end. Among the many optimisation algorithms, the Adam (Adaptive Moment Estimation) optimiser is widely applied in deep learning model training. This method adaptively adjusts the learning rate of each parameter by combining first-moment and second-moment estimates of the gradient, thereby improving training stability while guaranteeing convergence speed. Given model parameters θ and their gradients *g_t*, the Adam optimisation process can be expressed as:

$$m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t \tag{2.24}$$

$$\nu_t = \beta_2 \nu_{t-1} + (1 - \beta_2) g_t^2 \tag{2.25}$$

$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t} \tag{2.26}$$

$$\hat{\nu}_t = \frac{\nu_t}{1 - \beta_2^t} \tag{2.27}$$

$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{\nu}_t} + \epsilon} \hat{m}_t \tag{2.28}$$

--- p.35 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

25

where *m_t* denotes the first-moment estimate of the gradient (the momentum term), *ν_t* denotes the second-moment estimate of the gradient; β₁ and β₂ are exponential decay coefficients; η is the learning rate; ε is a very small constant that prevents the denominator from being zero, usually taking the value 10⁻⁸; *m̂_t* and *ν̂_t* respectively denote the bias-corrected momentum estimate and second-moment estimate; and finally the updated parameter θ_{t+1} is obtained.

Through this adaptive update mechanism, the Adam optimiser can maintain relatively stable learning-rate variation during training, thereby improving model training efficiency and convergence performance.

## 2.3 Theoretical Foundations of Object Detection

Object detection is one of the important research directions in the field of computer vision. Its main task is to locate and identify targets of interest in an image — that is, to accomplish both "classification" and "localisation" simultaneously. Unlike traditional image classification, which outputs only a category label, object detection must output both the position and the category information of targets, and therefore has higher complexity.

In practical applications, the output of an object detection model generally consists of a bounding box and a category label. The bounding box is generally represented in the following form:

$$B = (x, y, w, h) \tag{2.29}$$

where *x*, *y* denote the coordinates of the target's centre point, and *w*, *h* denote the width and height of the target box.

To evaluate the accuracy of detection results, the Intersection over Union (IoU) is generally adopted as the evaluation metric; it is computed as follows:

$$IoU = \frac{Area(B_{pred} \cap B_{gt})}{Area(B_{pred} \cup B_{gt})} \tag{2.30}$$

where *B_pred* denotes the predicted box and *B_gt* denotes the ground-truth annotation box. The larger the IoU value, the closer the prediction is to the true target position.

### 2.3.1 Two-Stage Object Detection Methods

Two-stage detectors generally first generate region proposals and then perform classification and regression prediction on the candidate regions; the structure diagram is shown in Figure 2.17. Typical representatives include models such as R-CNN, Fast R-CNN and Faster R-CNN.

R-CNN first generates candidate regions through selective search, then uses a convolutional neural network to extract features and perform classification. However, this method suffers from relatively low computational efficiency. To address this, Fast R-CNN significantly improved detection speed by sharing convolutional feature maps, while Faster R-CNN further introduced the Region Proposal Network (RPN) to achieve end-to-end learning of candidate regions, thereby substantially improving detection efficiency and accuracy.

The main advantage of two-stage methods is their relatively high detection accuracy, making them especially suitable for tasks with high detection-accuracy requirements. Their disadvantage, however, is high computational complexity, making it difficult to meet real-time requirements.

--- p.36 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

26

*[Figure: two-stage image object detection structure diagram]*

**Figure 2.17 Structure diagram of two-stage image object detection**

### 2.3.2 One-Stage Object Detection Methods

Unlike two-stage methods, one-stage detectors unify the target localisation and classification processes within a single network, thereby significantly increasing detection speed; the structure diagram is shown in Figure 2.18. Representative models include the YOLO (You Only Look Once) series and SSD (Single Shot MultiBox Detector).

The YOLO model divides the input image into multiple grid cells and directly predicts the target category and bounding box information within each cell, thereby achieving end-to-end detection. Its objective function generally consists of localisation error, classification error and confidence error. Through successive version iterations (such as YOLOv3, YOLOv5 and YOLOv8), the model has achieved a good balance between accuracy and speed.

The SSD model, by performing detection on multi-scale feature maps, improves recognition capability for targets of different sizes. Compared with YOLO, SSD performs more stably in small-target detection.

The advantage of one-stage methods lies in their fast detection speed, making them suitable for real-time detection scenarios such as autonomous driving and video surveillance. However, their detection accuracy is generally slightly lower than that of two-stage methods.

*[Figure: one-stage image object detection structure diagram]*

**Figure 2.18 Structure diagram of one-stage image object detection**

--- p.37 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

27

### 2.3.3 Key Technologies of Deep-Learning-Based Object Detection

With the development of deep learning, object detection technology has continued to evolve, forming a series of key technologies.

**(1) Feature extraction network:** Object detection models generally rely on a convolutional neural network as the feature extraction backbone — for example structures such as VGG and ResNet — extracting multi-scale features of the image through multi-layer convolution.

**(2) Multi-scale feature fusion:** Because the scale of targets in an image varies considerably, modern detection algorithms generally adopt a feature pyramid network (FPN) structure for multi-scale feature fusion, thereby improving the model's detection capability for targets of different sizes.

**(3) Anchor mechanism:** The anchor mechanism presets candidate boxes of different sizes and aspect ratios so that the model can predict target positions more efficiently. However, this method requires manual design of parameters and has relatively low flexibility.

**(4) Anchor-free detection:** In recent years, anchor-free methods have gradually risen to prominence; by directly predicting key points or centre-point positions they avoid complex anchor-box design and improve the model's generalisation capability.

**(5) Loss function design:** Object detection tasks generally adopt a multi-task loss function, including classification loss and regression loss. For example, the regression loss may use L1 loss or GIoU loss to improve bounding-box prediction accuracy.

### 2.3.4 Analysis of the Characteristics of Underwater Object Detection

Compared with ordinary scenes, the underwater environment has characteristics such as illumination attenuation, colour distortion and noise interference, and these factors have a significant impact on object detection performance. Therefore, in underwater object detection tasks it is necessary to combine image enhancement with feature extraction methods to improve the model's adaptability to complex environments.

At the same time, because underwater targets are often small in scale with blurred boundaries, traditional detection models are prone to missed detections or false detections. Therefore, combining super-resolution reconstruction with deep feature modelling methods can effectively improve detection performance, which is also the key direction of the subsequent research in this thesis.

## 2.4 Chapter Summary

This chapter has discussed the related theoretical foundations of underwater image processing and object detection tasks. First, the underwater image degradation model was analysed, explaining the main causes of declining underwater image quality from the two aspects of light absorption and scattering, and describing the degradation process mathematically through an imaging model.

Subsequently, the basic principles of underwater image super-resolution reconstruction were introduced, with particular focus on the application of convolutional neural networks in image reconstruction tasks, and a detailed explanation of the model structure, training process and optimisation methods.

In the deep learning theory section, the basic structure and working mechanism of convolutional neural networks were systematically expounded; at the same time, the Transformer model and its self-attention mechanism were analysed, and the advantages of the Mamba model in long-sequence modelling were further introduced.

--- p.38 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

28

Finally, the basic principles and mainstream methods of object detection were summarised, including the characteristics and applicable scenarios of two-stage and one-stage detection algorithms, and the challenges facing object detection were analysed in the light of the characteristics of the underwater environment.

The content of this chapter provides an important theoretical foundation for the design of the subsequent underwater image enhancement and object detection algorithms.

--- p.39 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

29

# Chapter 3 An Underwater Image Super-Resolution Reconstruction Method Based on a Frequency–Spatial Coupled Inference Network

## 3.1 Introduction

The underwater imaging environment is complex: during propagation, light is simultaneously affected by both absorption and scattering effects, and the degree of attenuation differs markedly for light of different wavelengths. This characteristic causes the underwater images acquired to generally exhibit visual defects such as colour imbalance, low contrast and texture degradation. These degradation phenomena not only affect human intuitive interpretation but also severely constrain the effectiveness of advanced applications such as underwater object detection, path planning and structural inspection. Super-resolution (SR) reconstruction technology, by inferring high-resolution output from low-resolution input, can effectively restore degraded structural and textural components in the image, and is currently an important technical means of improving image quality in underwater vision systems.

Thanks to the wide-ranging breakthroughs of deep learning in the field of image restoration, underwater image SR methods based on convolutional neural networks and Transformer architectures have successively emerged [18]. Such methods generally reconstruct high-frequency texture through multi-level spatial feature extraction and cascaded modules, and have achieved good reconstruction results on public datasets. However, the vast majority of the above methods perform feature modelling only within the spatial domain, and their exploitation of the global structural information and periodic patterns contained in the frequency domain remains very limited [32]; when faced with the complex and diverse degradation phenomena of underwater scenes, they struggle to stably capture global contextual cues and high-frequency detail.

At the same time, existing methods mostly rely on pixel-level L1 loss or generic perceptual loss in their loss function design [7], and these loss functions have insufficient constraining power over image structural contours and fine textures. According to texture–structure decomposition theory, an image can be represented as the superposition of a structure layer and a texture layer; decoupling the two components and applying supervision to each separately can provide more targeted optimisation guidance during reconstruction [29]. Inspired by this, this chapter introduces a texture–structure joint loss, applying constraints respectively to high-frequency texture detail and low-frequency structural edges, so that the network can likewise recover perceptually realistic and geometrically accurate reconstruction results under complex underwater degradation conditions.

Addressing the limitations of existing methods, this chapter proposes a new Frequency-Spatial Coupled Inference Network (FSCIN), which achieves enhanced reconstruction of underwater image super-resolution by fusing frequency and spatial priors. FSCIN integrates the Spatial Frequency Awareness Module (SFAM), which performs joint modelling of the frequency domain and the spatial domain through the Fast Fourier Transform (FFT) and Swin Transformer-based spatial encoding. SFAM aligns amplitude and phase information through dual-branch processing, thereby effectively capturing and enhancing the high-frequency components and global contextual information of the image. In addition, to maintain perceptual fidelity, this chapter also introduces a texture–structure joint constraint loss, which decomposes the reconstructed image into a texture layer and a structure layer and applies targeted supervision to each layer. This loss effectively constrains FSCIN to preserve the integrity of structural boundaries while reconstructing fine-grained visual detail. Extensive experimental results show that FSCIN demonstrates superior performance in reconstructing underwater images with good visual quality and accurate structure.

--- p.40 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

30

The content of this chapter is arranged as follows: Section 4.2 introduces the related basic techniques; Section 4.3 details the overall architecture of the improved network and each functional module; Section 4.4 presents the experimental setup and result analysis; Section 4.5 analyses the influence of super-resolution reconstructed images on object detection performance; Section 4.6 is the chapter summary. *(Note: the section numbers here appear as written in the original.)*

## 3.2 Related Techniques

### 3.2.1 The Swin Transformer Network

The standard Transformer model faces two prominent bottlenecks when applied to visual tasks: first, the scale of image features varies dynamically with the task, making it difficult to directly apply the fixed-token-size processing paradigm from natural language processing; second, the computational complexity of the global self-attention mechanism is proportional to the square of the image size, making the computational overhead extremely large when processing high-resolution images. Addressing these two limitations, Liu et al. proposed the Swin Transformer, a general-purpose visual backbone network with a hierarchical structure [30], which imitates the multi-scale feature extraction approach of CNNs and restricts self-attention computation within local fixed windows, reducing computational complexity from quadratic to linear while still accounting for the perception of global information.

As shown in Figure 3.1 and Figure 3.2, the Swin Transformer is composed of four successively progressive processing stages. The input image is first divided by a Patch Partition operation into a number of two-dimensional image patches of size P×P (P=4), which form a sequence that is fed into the subsequent stages. From the second stage onwards, adjacent patches are merged by the Patch Merging module, which expands the channel dimension while reducing spatial resolution, progressively building a hierarchical feature representation similar to that of a CNN. Each processing stage is composed of several consecutive Swin Transformer blocks, with two adjacent blocks alternately using W-MSA (Window-based MSA) and SW-MSA (Shift-Window-based MSA). W-MSA reduces computation by restricting attention computation within local windows, while SW-MSA introduces a window-shifting mechanism to ensure that information between adjacent windows is effectively transmitted, compensating for the deficiency of purely local window attention in cross-window contextual interaction.

Let the input feature map size be *H* × *W* and the window size be *M* × *M*; the computational complexity of W-MSA can be approximately expressed as O(*HW* · *M*²), far lower than the O((*HW*)²) of global attention, laying the efficiency foundation for practically deploying the Transformer structure in high-resolution visual tasks such as super-resolution.

*[Figure content: Images → Patch Partition → Linear Embedding → Swin Transformer Block (Stage 1, H/4 × W/4 × C) → Patch Merging → Swin Transformer Block (Stage 2, H/8 × W/8 × 2C) → Patch Merging → Swin Transformer Block (Stage 3, H/16 × W/16 × 4C) → Patch Merging → Swin Transformer Block (Stage 4, H/32 × W/32 × 8C). Input H × W × 3; patch tokens H/4 × W/4 × 48]*

**Figure 3.1 Schematic of the Swin Transformer structure**

--- p.41 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

31

*[Figure content: two consecutive blocks — Z^{l−1} → LN → W-MSA → (+) → Ẑ^l → LN → MLP → (+) → Z^l → LN → SW-MSA → (+) → Ẑ^{l+1} → LN → MLP → (+) → Z^{l+1}]*

**Figure 3.2 Swin Transformer schematic**

### 3.2.2 The Fourier Transform

The Fourier transform is a foundational mathematical tool in the field of signal and image processing; its core role is to convert a signal from the spatial domain to the frequency domain, revealing the global periodic structure of the signal in the form of a spectrum. For two-dimensional images, the Discrete Fourier Transform (DFT) is defined as:

$$F(u,v) = \sum_{x=0}^{H-1}\sum_{y=0}^{W-1} f(x,y) \cdot e^{-j2\pi\left(\frac{ux}{H} + \frac{vy}{W}\right)} \tag{3.1}$$

where *f*(*x*, *y*) is the spatial-domain image, *F*(*u*, *v*) is the corresponding frequency-domain representation, (*u*, *v*) are the frequency-domain coordinates, and *H*, *W* are respectively the height and width of the image. The frequency-domain representation *F*(*u*, *v*) is in complex form and can be further decomposed into an amplitude spectrum |*F*(*u*, *v*)| and a phase spectrum ∠*F*(*u*, *v*): the amplitude spectrum reflects the energy distribution of each frequency component and is closely related to the overall brightness and texture energy of targets in the image; the phase spectrum encodes the spatial position information of each frequency component and plays a key role in the geometric form of image structure.

In the super-resolution task, high-frequency components correspond to fine structures in the image such as edges and textures, and are the core determinant of reconstruction quality; low-frequency components correspond to the contours and overall brightness of the image, as shown in Figure 3.3. In engineering practice, the Fast Fourier Transform (FFT) is generally used, replacing the O(*N*²) of directly computing the DFT with a time complexity of O(*N* log *N*), significantly improving the practical efficiency of frequency-domain transformation within deep networks. After frequency-domain features have been modelled, the Inverse FFT (IFFT) can restore the processed spectrum back to the spatial domain, guaranteeing the spatial consistency of the features. This round-trip transformation mechanism of "spatial domain → frequency domain → spatial domain" is the core theoretical basis for the design of the SFAM module in this chapter.

--- p.42 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

32

*[Figure: Fourier transform schematic showing amplitude-spectrum and phase-spectrum decomposition]*

**Figure 3.3 Schematic of the Fourier transform (amplitude-spectrum and phase-spectrum decomposition)**

## 3.3 The Frequency–Spatial Coupled Inference Network Underwater Image Super-Resolution Reconstruction Model

### 3.3.1 Network Architecture Design

The overall processing flow of FSCIN is shown in Figure 3.4; the network passes through three functional stages in sequence to complete the conversion from low-resolution input to high-resolution output. Let the input low-resolution underwater image be *X*, the corresponding output high-resolution reconstructed image be *Y*, and *r* be the upsampling factor.

**Stage one: shallow feature extraction stage.** A 3×3 convolutional layer is applied to the input low-resolution image *X* ∈ *R^{H×W×3}* to extract an initial low-level feature representation:

$$F_0 = Conv_{3\times3}(X) \tag{3.2}$$

where *Conv*₃ₓ₃(·) denotes the standard 3×3 convolution operation, the number of output feature channels is set to *C* = 50, and *H*, *W* correspond respectively to the height and width of the input image. The shallow features *F*₀ ∈ *R^{H×W×C}* generated at this stage serve as the initial input to the subsequent deep modules, providing the network with rich low-level texture information.

**Stage two: frequency–spatial collaborative feature enhancement stage.** *T* SFAM modules are stacked consecutively, performing iterative joint frequency-domain and spatial-domain modelling on the feature maps. The processing of the *t*-th SFAM can be expressed as:

$$F_{SFAM}^{t} = H_{SFAM}^{t}(F_{SFAM}^{t-1}) = H_{SFAM}^{t}(H_{SFAM}^{t-1}(F_0)) \tag{3.3}$$

Each SFAM module obtains amplitude–phase frequency information and spatial dependency relationships by combining the Fast Fourier Transform (FFT) with a Swin Transformer-based dual-branch attention mechanism, achieving progressive enhancement of frequency-aware features. This stage aims to make full use of the image's global contextual information and high-frequency detail cues, so that the feature representation is strengthened in both the spatial and frequency domains. The detailed structure of SFAM will be introduced in Section 3.3.2.

**Stage three: high-resolution image reconstruction stage.** An upsampling operation is performed on the deep features *F_{SFAM}^{T}* enhanced in stage two to progressively restore spatial resolution, finally reconstructing the high-resolution image *Y*:

--- p.43 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

33

$$S = H_{HU}(F_{SFAM}^{T}) + H_{LU}(X) \tag{3.4}$$

where *H_HU*(·) and *H_LU*(·) respectively denote upsampling operations performed on the deeper features *F_{SFAM}^{T}* and on the initial input LR image *X*. Specifically, both contain a convolutional layer (a 3×3 convolution for *H_HU*(·) and a 5×5 convolution for *H_LU*(·)) and a sub-pixel convolution layer.

*[Figure content: Stage 1 — LR → 3×3 Conv; Stage 2 — 1st SFAM → t-th SFAM → T-th SFAM; Stage 3 — SR, compared against HR via Structural decomposition and Texture decomposition with Gradient update. SFAM detail: 1×1 Conv → FFT → (SwinT → 3×3 Conv) and (SwinT → 3×3 Conv) → IFFT → 1×1 Conv]*

**Figure 3.4 Schematic of the overall FSCIN network structure**

### 3.3.2 Frequency Awareness Module (SFAM)

To effectively model spatial dependency relationships and global frequency information in underwater images, this thesis designs the Spatial Frequency Awareness Module (SFAM) as the core component of FSCIN. The SFAM module aims to jointly process the amplitude component and phase component in the frequency domain, enhancing structural fidelity and fine-grained texture representation during reconstruction.

Given the input feature map of the *t*-th SFAM, the Fast Fourier Transform (FFT) is first used to convert it into the frequency domain. Specifically, the input features first undergo a preliminary convolution operation to complete feature normalisation, then the corresponding frequency-domain representation is obtained and further decomposed into an amplitude component 𝒜 and a phase component 𝒫:

$$\mathcal{A} = |FFT(Conv(F_{t-1}))|, \quad \mathcal{P} = \angle FFT(Conv(F_{t-1})) \tag{3.5}$$

--- p.44 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

34

In each branch, this thesis employs a Swin Transformer (SwinT) block followed by a 3×3 convolutional layer. SwinT is responsible for modelling long-range dependency relationships and adaptive spatial-frequency attention within windows, while the convolutional layer is used to enhance local feature refinement capability.

The dual-branch structure helps to model high-level frequency information and local spatial cues simultaneously; its computational process is expressed as:

$$\mathcal{A}' = Conv(SwinT(\mathcal{A})), \quad \mathcal{P}' = Conv(SwinT(\mathcal{P})) \tag{3.6}$$

After processing is complete, the outputs of the amplitude branch and the phase branch are fused through element-wise addition, and then the Inverse Fast Fourier Transform (IFFT) is used to convert the enhanced frequency-domain features back to the spatial domain. The resulting feature map simultaneously contains frequency-aware enhancement information and spatial consistency, and is passed on to the next stage:

$$F_t = F_{t-1} + IFFT(\mathcal{A}' + \mathcal{P}') \tag{3.7}$$

### 3.3.3 Texture–Structure Joint Loss

To supervise the network in recovering perceptually realistic and structurally consistent underwater images, this thesis designs a multi-modal joint loss function that jointly constrains the model learning process from three aspects: pixel-level fidelity, adversarial realism and frequency-aware perceptual consistency. The overall loss function is expressed as:

$$\mathcal{L} = \mathcal{L}_1 + \lambda_1 \mathcal{L}_{adv} + \lambda_2 \mathcal{L}_{texture} + \lambda_3 \mathcal{L}_{structure} \tag{3.8}$$

where ℒ₁ is the pixel-level reconstruction loss, ℒ_adv is the adversarial loss, ℒ_texture is used to constrain local texture consistency, ℒ_structure is used to guarantee structural edge alignment, and λ₁, λ₂, λ₃ are balancing weights, set respectively to 0.2, 0.4 and 0.4.

**(1) Pixel-level reconstruction loss**

This thesis uses the ℒ₁ loss to measure the absolute difference between the reconstructed image *Y* and the true high-resolution image *S*:

$$\mathcal{L}_1 = \|Y - S\|_1 \tag{3.9}$$

This term is used to maintain global colour and intensity consistency.

**(2) Adversarial loss**

To enhance perceptual realism, this thesis employs a standard GAN loss with a discriminator *D*:

$$\mathcal{L}_{adv} = -\mathbb{E}[\log D(Y)] \tag{3.10}$$

This loss makes the generated image conform to the distribution of natural underwater images.

**(3) Texture consistency loss**

Following the frequency-awareness principle, this thesis computes gradients in the spatial domain to quantify texture similarity:

$$\mathcal{L}_{texture} = \|\nabla Y - \nabla S\|_1 \tag{3.11}$$

where ∇ denotes the spatial gradient operator and *S* denotes the edge-preserving true high-resolution guide image.

**(4) Structural alignment loss**

To preserve geometric edges and structural contours, this thesis defines the structural alignment loss as follows:

$$\mathcal{L}_{structure} = \|\Phi(Y) - \Phi(S)\|_1 \tag{3.12}$$

--- p.45 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

35

where Φ(·) denotes the structure extractor. This term is used to ensure that the reconstructed image can maintain high-frequency boundaries aligned with the reference image.

## 3.4 Experimental Results and Analysis

### 3.4.1 Experimental Data and Experimental Environment

This chapter selects two public underwater image super-resolution benchmark datasets, USR-248 [15] and UFO-120 [16], for training and evaluating FSCIN, as shown in Figure 3.5. Both datasets provide paired low-resolution images and high-resolution reference images, and can be used to learn the mapping relationship from degraded underwater images to clear high-resolution images.

*[Figure content: (a) HR (640×480) with LR (320×240), LR (160×120), LR (80×60); (b) HR (640×480) with LR (320×240), LR (213×160), LR (160×120)]*

(a) USR-248 supports ×2, ×4 and ×8 training  (b) UFO-120 supports ×2, ×3 and ×4 training

**Figure 3.5 Concrete examples from the USR-248 and UFO-120 datasets**

The USR-248 dataset was constructed for the underwater single-image super-resolution task. It contains high-resolution images of 640×480 pixels together with their corresponding low-resolution versions at three sizes — 320×240, 160×120 and 80×60 — corresponding respectively to ×2, ×4 and ×8 magnification factors. This dataset contains 1,050 training sample pairs and provides 248 test images for performance evaluation. The image sources cover marine exploration, field acquisition and public online resources; the low-resolution images are generated by simulated degradation, and can reasonably reflect the problem of underwater detail loss under different resolution conditions.

The UFO-120 dataset was constructed specifically for underwater image enhancement and super-resolution reconstruction tasks. Its images were collected from multiple marine exploration scenarios, covering different water-body environments and types of visual degradation. This dataset contains 1,500 training sample groups and 120 test sample groups, corresponding to the three upsampling factors ×2, ×3 and ×4. Its low-resolution images are generated through style-transfer perturbation, Gaussian blur and bicubic down-sampling, and can simulate the compound degradation caused by factors such as underwater light attenuation, scattering and imaging-equipment limitations.

--- p.46 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

36

During training, the Adam optimiser is used to minimise the multi-modal joint loss function, with hyperparameters set to β₁=0.9, β₂=0.999, ε=10⁻⁸, and an initial learning rate set to 0.001, decayed at fixed intervals during training. Each mini-batch contains 16 low-resolution image patches of spatial size 50×50 pixels. The model is implemented on the PyTorch framework, and the training platform is an NVIDIA RTX 3090 GPU.

### 3.4.2 Evaluation Metrics

This chapter comprehensively adopts three complementary metrics — Peak Signal-to-Noise Ratio (PSNR), Structural Similarity Index Measure (SSIM) and Underwater Image Quality Measure (UIQM) — to quantitatively evaluate super-resolution reconstruction results. PSNR focuses on pixel-level error, SSIM focuses on structural consistency, and UIQM evaluates colour, sharpness and contrast from the perspective of underwater imaging characteristics; combining the three can more comprehensively reflect the objective quality of the reconstructed image and the underwater visual perception effect.

**Peak Signal-to-Noise Ratio (PSNR)** measures the pixel-level difference between the reconstructed image and the true high-resolution image based on Mean Squared Error (MSE), and is one of the most commonly used objective evaluation metrics in super-resolution tasks. Its computational formula is:

$$PSNR = 10 \cdot \log_{10}\left(\frac{L^2}{MSE}\right), \quad MSE = \frac{1}{HW}\|Y - S\|_2^2 \tag{3.13}$$

where *L* denotes the maximum pixel value of the image, usually 255 for an 8-bit image; *H* and *W* respectively denote the image height and width; *Y* is the reconstructed image output by the model, and *S* is the true high-resolution image. The PSNR value is expressed in dB; the higher the value, the smaller the pixel error between the reconstructed image and the reference image, and the lower the degree of objective distortion [65]. It should be noted that PSNR is relatively sensitive to overall pixel deviation but cannot fully reflect texture naturalness and structural perceptual quality, and therefore must be analysed together with other metrics.

**Structural Similarity Index (SSIM)** measures the degree of similarity between two images along the three dimensions of luminance, contrast and structure. Compared with purely pixel-error metrics, SSIM is closer to the way the human eye perceives changes in image structure. Its computational formula is:

$$SSIM(Y,S) = \frac{(2\mu_Y\mu_S + c_1)(2\sigma_{YS} + c_2)}{(\mu_Y^2 + \mu_S^2 + c_1)(\sigma_Y^2 + \sigma_S^2 + c_2)} \tag{3.14}$$

where *μ_Y* and *μ_S* respectively denote the means of the reconstructed image and the reference image, *σ_Y²* and *σ_S²* denote their variances, *σ_YS* denotes the covariance, and *c*₁ and *c*₂ are stabilising constants introduced to avoid a zero denominator. SSIM values usually lie between 0 and 1; the closer to 1, the more similar the two images are in terms of luminance, contrast and structure [66]. In the underwater image super-resolution task, SSIM can reasonably reflect whether edge contours and structural textures have been stably recovered.

**The Underwater Image Quality Measure (UIQM)** is a no-reference image quality evaluation method designed for underwater scenes. It does not rely on a true high-resolution image, but instead comprehensively evaluates image quality from the perspective of underwater visual perception characteristics. UIQM is obtained as a linear weighting of three sub-metrics — colourfulness measure (UICM), sharpness measure (UISM) and contrast measure (UIConM):

--- p.47 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

37

$$UIQM = c_1 \cdot UICM + c_2 \cdot UISM + c_3 \cdot UIConM \tag{3.15}$$

where UICM is used to measure image colour balance and colour reproduction, UISM is used to evaluate edge and texture sharpness, UIConM is used to reflect local contrast performance, and *c*₁, *c*₂ and *c*₃ are empirical weighting coefficients. The higher the UIQM value, the better the overall performance of the underwater image in terms of colour naturalness, texture sharpness and contrast [67]. Because underwater images are often accompanied by colour casts, low contrast and texture attenuation, UIQM can provide an important supplement to PSNR and SSIM for underwater visual quality analysis.

### 3.4.3 Experimental Design and Implementation

To comprehensively evaluate the reconstruction performance of FSCIN, this chapter selects a set of representative methods from the current image super-resolution field as comparison baselines, covering the following categories: traditional CNN methods (SRCNN, VDSR); GAN-based methods (SRGAN [7], SRDRM, SRDRM-GAN); and methods designed specifically for underwater scenes (PAL, AMPCNet [17], DeepWaveNet [19], RDLN). All comparative experiments are conducted under a unified dataset split and identical evaluation metrics, in order to guarantee the fairness of the comparison results.

This chapter combines two evaluation approaches, quantitative analysis and qualitative analysis: quantitative analysis makes numerical comparisons based on the three metrics PSNR, SSIM and UIQM; qualitative analysis uses visualised results to intuitively demonstrate the differences in the performance of each model in terms of edge sharpness, texture fidelity and colour naturalness.

### 3.4.4 Quantitative Analysis

**(1) Quantitative analysis on the USR-248 dataset**

Tables 3.1 to 3.3 respectively list the quantitative evaluation results of each method at ×2, ×4 and ×8 magnification, with bold indicating the best value in each column; FLOPs are measured with reference to a 640×480 high-resolution image. From Tables 3.1 to 3.3 it can be seen that FSCIN achieves leading overall performance at all three magnification factors. At ×2 magnification, FSCIN obtains the highest PSNR (30.04 dB) and SSIM (0.83); compared with SRDRM-GAN, the comparison method with the largest parameter count (289.38 GFLOPs, 11.31 M parameters), FSCIN achieves better reconstruction performance with only 30.70 GFLOPs and 0.55 M parameters. At ×4 magnification, FSCIN likewise maintains the best PSNR (26.22 dB) while having relatively low computational cost. In the large ×8 magnification scenario, FSCIN achieves the highest PSNR (24.03 dB) with only 2.45 GFLOPs (the lowest among all methods), demonstrating an outstanding balance between reconstruction performance and inference efficiency, and verifying the robustness and efficiency of the frequency–spatial coupled design in large-factor reconstruction.

**(2) Quantitative analysis on the UFO-120 dataset**

Table 4.4 *(as numbered in the original; corresponds to Table 3.4)* presents comprehensive evaluation results at the three magnification factors ×2, ×3 and ×4. On the UFO-120 dataset, FSCIN obtains the highest PSNR (25.98 dB) and the highest UIQM (2.99, tied with DeepWaveNet) at ×2 magnification; at ×3 and ×4 magnification, FSCIN maintains the best PSNR (26.07 dB and 25.23 dB respectively), demonstrating good

--- p.48 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

38

cross-magnification generalisation capability. Although Deep WaveNet performs prominently on SSIM and on some UIQM metrics, FSCIN holds a consistent and clear advantage on the PSNR metric, and performs more evenly in comprehensively balancing reconstruction fidelity and perceptual quality.

**Table 3.1 ×2 comparison of different methods on the USR-248 dataset**

| Method | FLOPs (G) | Params (M) | PSNR (dB) | SSIM | UIQM |
|---|---|---|---|---|---|
| SRCNN | 21.3 | 0.06 | 26.81 | 0.76 | 2.74 |
| VDSR | 205.28 | 0.67 | 28.98 | 0.79 | 2.57 |
| SRGAN | 377.76 | 5.95 | 28.05 | 0.78 | 2.74 |
| SRDRM | 203.91 | 0.83 | 28.36 | 0.80 | 2.78 |
| SRDRM-GAN | 289.38 | 11.31 | 28.55 | 0.81 | 2.77 |
| PAL | 203.82 | 0.83 | 28.41 | 0.80 | — |
| AMPCNet | — | 1.15 | 29.54 | 0.80 | 2.77 |
| DeepWaveNet | 21.47 | 0.28 | 29.09 | 0.80 | 2.73 |
| RDLN | 74.86 | 0.84 | 29.96 | 0.83 | 2.68 |
| **FSCIN (this thesis)** | 30.70 | 0.55 | **30.04** | **0.83** | 2.72 |

**Table 3.2 ×4 comparison of different methods on the USR-248 dataset**

| Method | FLOPs (G) | Params (M) | PSNR (dB) | SSIM | UIQM |
|---|---|---|---|---|---|
| SRCNN | 21.3 | 0.06 | 23.38 | 0.67 | 2.38 |
| VDSR | 205.28 | 0.67 | 25.70 | 0.68 | 2.44 |
| SRGAN | 529.86 | 5.95 | 24.76 | 0.69 | 2.42 |
| SRDRM | 291.73 | 1.90 | 24.64 | 0.68 | 2.46 |
| SRDRM-GAN | 377.2 | 12.38 | 24.62 | 0.69 | 2.48 |
| PAL | 303.42 | 1.92 | 24.89 | 0.69 | — |
| AMPCNet | — | 1.17 | 25.90 | 0.66 | 2.58 |
| DeepWaveNet | 5.59 | 0.29 | 25.20 | 0.68 | 2.54 |
| RDLN | 29.56 | 0.84 | 26.16 | 0.66 | 2.38 |
| **FSCIN (this thesis)** | 9.58 | 0.56 | **26.22** | 0.68 | 2.47 |

**Table 3.3 ×8 comparison of different methods on the USR-248 dataset**

| Method | FLOPs (G) | Params (M) | PSNR (dB) | SSIM | UIQM |
|---|---|---|---|---|---|
| SRCNN | 21.3 | 0.06 | 19.97 | 0.57 | 2.01 |
| VDSR | 205.28 | 0.67 | 23.58 | 0.63 | 2.17 |
| SRGAN | 567.88 | 5.95 | 20.14 | 0.60 | 2.10 |
| SRDRM | 313.68 | 2.97 | 21.20 | 0.60 | 2.18 |
| SRDRM-GAN | 3915 | 13.45 | 20.25 | 0.61 | 2.17 |
| PAL | 325.51 | 2.99 | 22.51 | 0.63 | — |
| AMPCNet | — | 1.25 | 23.83 | 0.62 | 2.25 |
| DeepWaveNet | 1.62 | 0.34 | 23.25 | 0.62 | 2.21 |
| RDLN | 18.23 | 0.84 | 23.91 | 0.54 | 2.18 |
| **FSCIN (this thesis)** | 2.45 | 0.64 | **24.03** | 0.54 | 2.18 |

**Table 3.4 Quantitative evaluation of underwater image super-resolution on the UFO-120 dataset (×2/×3/×4)**

| Method | PSNR ×2 | PSNR ×3 | PSNR ×4 | SSIM ×2 | SSIM ×3 | SSIM ×4 | UIQM ×2 | UIQM ×3 | UIQM ×4 |
|---|---|---|---|---|---|---|---|---|---|
| SRCNN | 24.75 | 22.22 | 19.05 | 0.72 | 0.65 | 0.56 | 2.39 | 2.24 | 2.02 |
| SRGAN | 26.11 | 23.87 | 21.08 | 0.75 | 0.70 | 0.58 | 2.44 | 2.39 | 2.56 |
| SRDRM | 24.62 | — | 23.15 | 0.72 | — | 0.67 | 2.59 | — | 2.57 |
| SRDRM-GAN | 24.61 | — | 23.26 | 0.72 | — | 0.67 | 2.59 | — | 2.55 |
| DeepWaveNet | 25.71 | 25.23 | 25.08 | 0.77 | 0.76 | 0.74 | 2.99 | 2.96 | 2.97 |
| AMPCNet | 25.24 | 25.73 | 24.70 | 0.71 | 0.70 | 0.70 | 2.93 | 2.85 | 2.88 |
| URSCT | 25.96 | — | 23.59 | 0.80 | — | 0.66 | — | — | — |
| **FSCIN (this thesis)** | **25.98** | **26.07** | **25.23** | 0.78 | 0.75 | 0.70 | 2.99 | 2.96 | 2.90 |

--- p.49 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

39

### 3.4.5 Qualitative Analysis

Figure 3.6 shows the visualised reconstruction results (×2/×4/×8) of FSCIN and the comparison methods on the USR-248 dataset. As can be seen from the figure, as the magnification factor increases the other methods generally exhibit problems such as over-smoothing, artefacts or distortion, which is especially evident at the large ×8 factor; FSCIN, by contrast, is able to recover sharper edge contours, clearer texture layering and more natural colour distribution at every magnification factor, with overall visual quality superior to all comparison methods. This result strongly corroborates the effectiveness of the frequency–spatial coupled design in restoring the fine detail and structural integrity of underwater images.

Figure 3.7 shows the visual comparison results on the UFO-120 dataset (×2/×3/×4). When handling typical underwater fine-grained structures such as fish scales and coral branches, FSCIN successfully recovers rich edge patterns and natural colour tones, whereas the other methods exhibit, to varying degrees, problems such as colour shift, texture blurring or loss of detail. The above qualitative comparisons further verify the practical effectiveness of the frequency-domain/spatial-domain coupled design and the texture–structure-guided optimisation strategy proposed in this chapter.

*[Figure: visual comparison grid on USR-248]*

**Figure 3.6 Visual comparison on the USR-248 dataset (×2/×4/×8)**

--- p.50 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

40

*[Figure: visual comparison grid on UFO-120]*

**Figure 3.7 Visual comparison on the UFO-120 dataset (×2/×3/×4)**

### 3.4.6 Ablation Experiments

**(1) Verification of the effectiveness of the SFAM module.** To examine the contribution of SFAM in isolation, we replace SFAM with a standard Frequency Residual Block (FRB) to obtain the control variant FSCIN-FRB, and compare them on the USR-248 dataset at ×2 magnification; the results are shown in Table 3.5.

**Table 3.5 Ablation experiment on the effectiveness of the SFAM module (USR-248, ×2)**

| Model | FLOPs | Params | PSNR (dB) | SSIM | UIQM |
|---|---|---|---|---|---|
| FSCIN-FRB | 13.04 G | 0.29 M | 28.77 | 0.73 | 2.64 |
| **FSCIN (this thesis)** | 30.70 G | 0.55 M | **29.81** | **0.80** | **2.70** |

As Table 3.5 shows, FSCIN improves PSNR by 1.04 dB and SSIM by 0.07 compared with FSCIN-FRB,
and improves UIQM by 0.06, comprehensively verifying the significant gain that SFAM brings to image fidelity, structural quality and perceptual effect. Although FSCIN's FLOPs (30.70 G) are higher than those of FSCIN-FRB (13.04 G), the substantial performance improvement fully justifies this additional computational cost, and also corroborates the clear superiority of the frequency–spatial coupled design scheme over independent frequency-block processing.

**(2) Verification of the effectiveness of the multi-modal loss function.** On the UFO-120 dataset at ×2 magnification, the constituent terms of the loss function are ablated item by item; the results are shown in Table 3.6. The experiment starts from a baseline of L1 loss alone (Type 1), and separately tests the individual effect of the adversarial loss (Type 2), the texture loss (Type 3) and the structural loss (Type 4). It can be seen that each individual loss brings a certain degree of improvement in PSNR or SSIM; when all four losses are used jointly (Type 5), the model achieves the best performance, with PSNR reaching 25.75 dB and SSIM 0.76, clearly better than any single-loss configuration. The above

--- p.51 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

41

results verify the complementary gain effect of the texture consistency constraint and the structural alignment constraint on different dimensions of image quality; the joint supervision of the two is an important guarantee for FSCIN achieving high-quality reconstruction.

**Table 3.6 Ablation experiment on the multi-modal loss function (UFO-120, ×2)**

| Configuration | ℒ₁ | ℒ_adv | ℒ_texture | ℒ_structure | PSNR (dB) | SSIM |
|---|---|---|---|---|---|---|
| Type 1 | ✓ | | | | 25.62 | 0.73 |
| Type 2 | | ✓ | | | 25.58 | 0.71 |
| Type 3 | | | ✓ | | 25.61 | 0.72 |
| Type 4 | | | | ✓ | 25.63 | 0.73 |
| **Type 5 (complete)** | ✓ | ✓ | ✓ | ✓ | **25.75** | **0.76** |

## 3.5 Chapter Summary

Addressing the underwater image super-resolution reconstruction task, this chapter has proposed the Frequency–Spatial Coupled Inference Network (FSCIN) to solve the problems of insufficient exploitation of frequency-domain information and the limited constraining power of loss functions. The network constructs a three-stage processing framework comprising low-level feature extraction, frequency–spatial collaborative feature enhancement and high-resolution image reconstruction; the function of each stage is clear and the coupling is reasonable, providing a good basis for the flexible replacement and extension of subsequent modules. The core spatial–frequency awareness module (SFAM) maps features into the frequency domain through the Fast Fourier Transform (FFT), models the amplitude spectrum and phase spectrum separately using a dual-branch Swin Transformer attention structure, and then restores them to the spatial domain through the inverse Fourier transform (IFFT), achieving deep fusion of frequency-domain global perception and spatial-domain local modelling. The joint loss function, which applies supervision separately to the texture layer and the structure layer, effectively improves the reconstruction accuracy of high-frequency detail and geometric edges through the coordinated action of gradient-domain texture constraints and structure-extractor constraints. Experimental results show that FSCIN achieves optimal or highly competitive quantitative metrics at multiple magnification factors on the two public benchmark datasets USR-248 and UFO-120, while also demonstrating clearer texture restoration capability and higher structural fidelity in terms of visual quality, providing a high-quality image pre-processing basis for the subsequent underwater object detection task. *(The content of this chapter has been published at The 5th International Conference on Applied Mathematics, Modeling and Computer Simulation.)*

--- p.52 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

42

# Chapter 4 An Underwater Image Object Detection Method Based on an Improved YOLOv8

## 4.1 Introduction

Underwater object detection is one of the core tasks of underwater visual perception systems, and has important application value in fields such as marine biological monitoring, autonomous navigation of underwater robots and marine resource exploration. However, the underwater imaging environment is complex: as light propagates through water it is jointly affected by multiple factors such as scattering, absorption and refraction, causing underwater images generally to suffer from degradation phenomena such as low contrast, colour shift and blurred edges. These visual defects severely constrain the ability of object detection algorithms to extract effective features.

From the perspective of this thesis's overall "enhancement–detection" framework, the FSCIN super-resolution reconstruction network proposed in Chapter 3 has already systematically improved image quality with respect to the above degradation problems: through frequency-domain/spatial-domain collaborative modelling it reconstructs originally low-quality underwater images into high-quality images with clearer texture, more accurate colour and more complete edge information, achieving an optimal PSNR of 30.04 dB at ×2 magnification on the USR-248 dataset and a reconstruction accuracy of 24.03 dB at ×8 magnification with only 2.45 GFLOPs, verifying the effectiveness and efficiency of the front-end enhancement module. The work of this chapter takes the sharpened images output by Chapter 3 as direct input, and builds an accurate underwater object detection model on the basis of these higher-quality images, realising the second stage of the complete processing chain "original image → super-resolution sharpening → clear image → object detection → detection result". Through this cascaded design, the object detection model can extract more effective target features from images with richer detail and higher contrast, thereby significantly improving the detection recall rate and localisation accuracy for tiny underwater targets.

At present, one-stage detection methods represented by YOLOv8 still face the following main limitations when applied directly to underwater scenes [39][43]: first, YOLOv8 performs feature extraction with convolutional neural networks at its core, and being limited by the local receptive field it struggles to model long-range dependency relationships in the image, with somewhat deficient capability for capturing global contextual information; second, the original C2f module has insufficient fine-grained feature representation capability for small targets, and detection accuracy for tiny targets (such as sea urchins and scallops) under low-visibility underwater conditions is limited; third, although PAN-FPN-type structures can enhance multi-scale information fusion [38], in complex underwater scenes the appearance differences, occlusion and background interference of targets at different scales still weaken the model's adaptive fusion capability, making it difficult to simultaneously accommodate the detection requirements of targets at different scales.

Addressing the above problems, this chapter proposes an improved YOLOv8 underwater image object detection model, designing a Fine-Grained Feature Extraction Module (FFEM) to replace the C2f module in the original YOLOv8. This module is composed collaboratively of three functional sub-modules: the Channel-Spatial Adaptive Enhancement Module (CAEM) precisely focuses on target edges and texture details through convolution and channel–spatial attention mechanisms; the Mamba-based global perception module (Visual SSM, VSSM) uses a visual state space model to model long-range dependencies and capture global contextual information; and the Multi-Scale Cross-Attention Fusion Module (MCFM) adaptively fuses the two feature streams through a dynamic weighting mechanism, outputting a

--- p.53 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

43

highly discriminative fine-grained feature representation. Experiments on the URPC2021 underwater object detection dataset show that, compared with the original YOLOv8, the improved model raises mAP50 by 1.8 percentage points (0.855 → 0.873) and raises small-target APs by 1.1 percentage points (0.166 → 0.177), verifying the effectiveness of this chapter's method in the second stage of the "enhancement–detection" cascaded framework.

The content of this chapter is arranged as follows: Section 4.2 introduces the related basic techniques; Section 4.3 details the overall architecture of the improved network and each functional module; Section 4.4 presents the experimental setup and result analysis; Section 4.5 analyses the influence of super-resolution reconstructed images on object detection performance; Section 4.6 is the chapter summary.

## 4.2 Related Techniques

### 4.2.1 The YOLOv8 Object Detection Network

The YOLO (You Only Look Once) family of algorithms is the representative approach in the current field of one-stage object detection. By modelling the detection task as a direct regression problem, it predicts target categories and bounding-box coordinates simultaneously within a single forward inference pass, achieving a good balance between detection speed and accuracy. YOLOv8 is a more recent version in this series, with a number of systematic improvements in network structure and training strategy.

In terms of the backbone network, YOLOv8 adopts a newly designed C2f module to replace the C3 module of the previous generation. The C2f module splits the input feature map into two branches — one passed through directly, the other undergoing deep feature extraction through multiple Bottleneck blocks — and finally concatenates and fuses all intermediate outputs, improving gradient flow while maintaining computational efficiency. In terms of feature fusion, YOLOv8 inherits the PAN-FPN structure, achieving bidirectional fusion of multi-scale features through a top-down semantic path and a bottom-up detail path, enhancing detection capability for targets at different scales. In terms of the detection head, YOLOv8 adopts a decoupled head design, processing the classification branch and the regression branch separately, reducing mutual interference between the two tasks and improving detection accuracy.

Although YOLOv8 performs excellently in general object detection tasks, its backbone network is dominated by local convolution operations and lacks the capability to explicitly model global dependency relationships; the C2f module has limited fine-grained feature representation capability when handling small underwater targets. It is therefore necessary to make targeted improvements to YOLOv8 for the image characteristics of underwater scenes, in order to improve its detection robustness in complex underwater environments.

*[Figure: YOLOv8 network structure diagram]*

**Figure 4.1 Schematic of the YOLOv8 network structure**

--- p.54 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

44

### 4.2.2 Attention Mechanisms

The core idea of the attention mechanism originates from the selective focusing characteristic of the human visual system towards regions of interest. In deep learning it is modelled as a process of applying dynamic weights to each position or each channel of a feature map, so as to guide the network to allocate more computational resources to regions richer in information.

Attention mechanisms differ in architecture, but their core process is consistent — all require three steps: squeeze, excitation and calibration. Given an input feature *X* ∈ *R^{H×W×C}*, where *H*, *W* and *C* respectively denote length, width and number of channels. First, the squeeze process is the process of extracting one or more statistics *S* from *X* according to channel region or spatial region. Channel attention mechanisms generally use a pooling operation to generate a single statistic, whereas spatial attention mechanisms generally use a 1×1 convolution operation to generate multiple statistics. Taking the channel attention mechanism as an example here, its formula is expressed as follows:

$$S = pool(X) \tag{4.1}$$

where *pool*(·) denotes the pooling operation.

Then, the excitation process mainly obtains the interdependency relationships between channel regions or spatial regions from the extracted statistic *S*, and produces an attention map *M* of different tensor dimensions, of size 1 × 1 × *C* (CA) or *H* × *W* × 1 (SA). This process can be implemented using multiple fully connected layers or multiple convolutional layers; its formula is expressed as follows:

$$M = fc_2(fc_1(S)) \tag{4.2}$$

where *fc*(·) represents a fully connected layer.

Finally, in order to recalibrate the input features, the generated attention map *M* must be normalised to between 0 and 1 through a Sigmoid activation function, and then multiplication is performed on *M* and *X* in a channel-wise or spatial-wise manner, thereby achieving recalibration of the input features; the process is expressed as follows:

$$\hat{X} = \sigma(M) \otimes X \tag{4.3}$$

where σ denotes the Sigmoid activation function. The symbol ⊗ denotes a pixel-level multiplication operation. *X̂* is the calibrated feature.

## 4.3 The Improved YOLOv8 Underwater Image Object Detection Model

### 4.3.1 Network Architecture Design

This chapter makes targeted improvements on the basis of the original YOLOv8 architecture, replacing the C2f module in the backbone network and neck network with the designed Fine-Grained Feature Extraction Module (FFEM), while the remaining structure is kept unchanged, as shown in Figure 4.2.

FFEM is composed of three functional sub-modules; the overall processing flow is shown in Figure 4.3. For an input feature map *X*, the module processes it in two parallel branches: CAEM extracts the edge and detail features of targets; VSSM captures global context and long-range dependency information. The outputs of the two branches undergo preliminary fusion through element-wise addition, giving the intermediate feature *X*′, which is then dynamically weighted and fused by MCFM, finally outputting the fine-grained feature FFEM. The above processing can be uniformly expressed as:

$$FFEM(X) = MCFM(X') = MCFM(CAEM(X) \oplus VSSM(X)) \tag{4.4}$$

--- p.55 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

45

where *MCFM*(·) denotes the multi-scale cross-attention fusion module, *CAEM*(·) denotes the channel–spatial adaptive enhancement module, *VSSM*(·) denotes the Mamba-based global perception module, ⊕ denotes element-wise addition, and *X*′ is the feature map after fusing the two outputs of *CAEM* and *VSSM*.

The core of this design idea is that the parallel processing of the local branch and the global branch enables the module to simultaneously account for the local fine-grained texture of underwater targets and cross-regional overall structural information; the complementary fusion of the two effectively compensates for the deficiencies of the original C2f module in global modelling and fine perception of small targets.

*[Figure: improved YOLOv8 network structure diagram]*

**Figure 4.2 Schematic of the improved YOLOv8 network structure**

*[Figure: FFEM overall structure — input X splits into CAEM branch and VSSM branch, summed into X′, then passed to MCFM]*

**Figure 4.3 Schematic of the overall structure of the fine-grained feature extraction module**

### 4.3.2 Channel–Spatial Adaptive Enhancement Module

The design objective of the Channel-Spatial Adaptive Enhancement Module (CAEM) is to precisely perceive local discriminative features of underwater targets such as edge contours and texture details, while suppressing noise interference introduced by factors such as water-flow disturbance and uneven illumination, so as to provide a high-quality local representation for the subsequent fusion stage. As shown in

--- p.56 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

46

Figure 4.4, the module collaboratively completes local feature extraction through two parallel branches, and then completes the final output through attention weighting.

**First branch (local detail extraction):** two cascaded 3×3 convolutional layers (with a ReLU activation in between) are used to extract the local spatial detail of the input feature map, giving the local feature *F_local*:

$$F_{local} = Conv_{3\times3}\left(ReLU(Conv_{3\times3}(X))\right) \tag{4.5}$$

where *Conv*(·) denotes convolution, its subscript denotes the convolution kernel size, and *ReLU*(·) denotes the ReLU activation function.

**Second branch (channel attention weight generation):** global average pooling is applied to the input feature map to compress the spatial dimensions, followed by two cascaded 1×1 convolutions (with a ReLU activation in between) and a final Sigmoid activation function, generating an attention weight vector α along the channel dimension, used to highlight feature channels with higher semantic relevance:

$$\alpha = \sigma\left(Conv_{1\times1}\left(ReLU\left(Conv_{1\times1}(AvgPool(X))\right)\right)\right) \tag{4.6}$$

where σ(·) denotes the sigmoid activation function and *AvgPool*(·) denotes global average pooling.

**Channel weighting and spatial attention enhancement:** the local feature *F_local* is multiplied element-wise with the channel weight α to obtain the channel-weighted local feature *F_fused*; a 7×7 convolution is then applied to *F_fused* followed by Sigmoid activation, generating the spatial attention map β used to locate the salient spatial regions where targets reside; finally *F_fused* is multiplied with β again, giving the module's final output:

$$F_{fused} = F_{local} \cdot \alpha \tag{4.7}$$

$$\beta = \sigma\left(Conv_{7\times7}(F_{fused})\right) \tag{4.8}$$

$$CAEM(X) = F_{fused} \cdot \beta \tag{4.9}$$

The combination of the above channel–spatial dual attention mechanism enables the module both to distinguish the importance of different semantic channels and to adaptively focus on target regions along the spatial dimension, effectively improving the perception accuracy for detail information of tiny underwater targets (such as sea urchins and clams).

*[Figure: channel–spatial adaptive enhancement module]*

**Figure 4.4 Channel–spatial adaptive enhancement module**

--- p.57 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

47

### 4.3.3 Multi-Scale Cross-Attention Fusion Module

After the outputs of the channel–spatial adaptive enhancement module and the Mamba-based global perception module are fused through element-wise addition, the fused feature *X*′ is obtained, which preliminarily integrates local texture detail with global contextual information, providing a complementary feature basis for the subsequent attention interaction.

The Multi-Scale Cross-Attention Fusion Module (MCFM) takes the fused feature *X*′ as input, and through three parallel branches and cross-scale attention interaction outputs the highly discriminative fine-grained feature *Y*, as shown in Figure 4.5.

**First branch (multi-scale asymmetric feature extraction):** two groups of asymmetric convolutions are applied to *X*′ in turn, extracting multi-scale features *F*₁ and *F*₂ under different receptive fields:

$$F_1 = Conv_{3\times1}\left(ReLU(Conv_{1\times3}(X'))\right) \tag{4.10}$$

$$F_2 = Conv_{5\times1}\left(ReLU(Conv_{1\times5}(X'))\right) \tag{4.11}$$

where the combination of 1×3 and 3×1 asymmetric convolutions approximately simulates the receptive field of a 3×3 convolution, while the combination of 1×5 and 5×1 covers a larger range of spatial dependency. After adding *F*₁ and *F*₂, a 1×1 convolution performs channel fusion, generating the multi-scale fused feature *F*₃:

$$F_3 = Conv_{1\times1}(F_1 + F_2) \tag{4.12}$$

**Second and third branches (key–value generation):** 1×1 convolutions are applied separately to *X*′ to independently generate the Key *K* and Value *V* required for attention computation:

$$K = Conv_{1\times1}(X') \tag{4.13}$$

$$V = Conv_{1\times1}(X') \tag{4.14}$$

**Cross-attention computation:** the multi-scale fused feature *F*₃ passes through a 1×1 convolution to generate the Query *Q*, which is multiplied element-wise with *K* and normalised by Softmax to generate the attention weight map *A*; *A* is then multiplied element-wise with *V* to obtain the attention-enhanced feature *F*₄:

$$Q = Conv_{1\times1}(F_3) \tag{4.15}$$

$$A = Softmax(Q \cdot K) \tag{4.16}$$

$$F_4 = A \cdot V \tag{4.17}$$

**Feature fusion output:** the attention-enhanced feature *F*₄ is added to the multi-scale fused feature *F*₃ to obtain the feature *Z*; *Z* is then channel-concatenated with *F*₃, and finally a 1×1 convolution outputs the fine-grained feature:

$$Z = F_3 + F_4 \tag{4.18}$$

$$Y = MCFM(X') = Conv_{1\times1}([F_3, Z]) \tag{4.19}$$

where [*F*₃, *Z*] denotes the channel concatenation operation on *F*₃ and *Z*.

--- p.58 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

48

By using the multi-scale fused feature *F*₃ as the Query and having *K*, *V* derived from the original features participate in the attention computation, the module achieves cross-scale information interaction between multi-scale features and the original features, dynamically allocating weights to features at different scales and enhancing the network's adaptive perception capability for multi-scale underwater targets.

*[Figure: multi-scale cross-attention fusion module structure]*

**Figure 4.5 Schematic of the structure of the multi-scale cross-attention fusion module**

### 4.3.4 Mamba-Based Global Perception Module

Because the receptive field of a traditional CNN is confined to a local neighbourhood, it is difficult to establish dependency relationships between distant pixels of an image within a single layer, and it lacks effective modelling capability for the global blur phenomenon in underwater images caused by scattering. The Mamba-based global perception module (VSSM) introduces a visual state space model, encoding long-range temporal and spatial dependencies with implicit state variables, overcoming the constraint of the convolutional local receptive field and being better suited to capturing the global contextual features of underwater images.

As shown in Figure 4.6, VSSM contains two parallel processing branches, and performs gated fusion of the two outputs through a Hadamard product.

**Main branch (global context extraction):** the input feature *X* first passes through a linear transformation (Linear) to adjust the distribution dimensions of the feature space; then it passes through a depthwise separable convolution (DWConv), which extracts local spatial information while maintaining lightweight computational characteristics; afterwards a SiLU activation function (i.e. the Swish function, *f*(*x*) = *x* · σ(*x*)) is used to introduce non-linear representational capability; next a two-dimensional state space model (2D-SSM) performs a serialised scan of the features, modelling global spatial dependencies in the horizontal and vertical directions with linear complexity; finally layer normalisation (LN) stabilises the feature distribution, yielding the global-perception intermediate feature *X*₁:

$$X_1 = LN\left(2D\text{-}SSM\left(SiLU\left(DWConv(Linear(X))\right)\right)\right) \tag{4.20}$$

**Gating branch (adaptive information screening):** a linear transformation and *SiLU* activation are applied in turn to the input feature *X*, generating the gating weight *X*₂:

$$X_2 = SiLU(Linear(X)) \tag{4.21}$$

--- p.59 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

49

**Gated fusion output:** the two outputs are fused through a Hadamard product (element-wise multiplication); the gating mechanism adaptively screens and retains the effective components of the global contextual information, and finally a linear transformation completes the adjustment of feature dimensions, giving the module output:

$$VSSM(X) = Linear(X_1 \odot X_2) \tag{4.22}$$

where "⊙" denotes the Hadamard product.

This design dynamically screens the global features extracted by the 2D-SSM through a gating mechanism, effectively filtering out interference from underwater background noise and improving feature robustness while maintaining global perception capability.

*[Figure: Mamba-based global perception module (VSSM) structure]*

**Figure 4.6 Schematic of the structure of the Mamba-based global perception module (VSSM)**

## 4.4 Experimental Results and Analysis

### 4.4.1 Experimental Data and Experimental Environment

This chapter carries out experimental verification on the URPC2021 underwater object detection dataset. This dataset was released by the 2021 China Underwater Robot Professional Competition and contains a total of 7,600 annotated underwater images, covering four typical classes of underwater target: **sea cucumber (holothurian), sea urchin (echinus), scallop and starfish**. The various target classes differ considerably in size, morphology, texture and background complexity, and can reasonably comprehensively reflect the detection challenges of real underwater scenes.

The dataset annotations use the YOLO format; each label file contains the target category index and normalised bounding-box coordinates. Before the experiments, the samples were uniformly inspected, filtering out images with severe blur, excessive occlusion or abnormal annotation, to ensure the usability of the training and test data. Finally, the training set (6,080 images) and test set (1,520 images) were split in a ratio of 8:2, and all model comparisons were completed under the same split.

To intuitively illustrate the image characteristics of the URPC2021 dataset, this thesis presents some typical sample images, as shown in Figure 4.7. The samples in the figure cover typical difficult scenarios such as low resolution, motion blur, colour shift and densely distributed small targets, and can illustrate the input-quality degradation and dense small-target distribution problems faced by this chapter's detection task.

--- p.60 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

50

*[Figure: sample images from the URPC2021 dataset]*

**Figure 4.7 Sample images from the URPC2021 dataset**

The experiments in this thesis were completed in a unified hardware and software environment. The hardware platform uses an Intel(R) Xeon(R) Platinum 8260 CPU @ 2.40 GHz with 90 GB of memory, and a GPU of 48 GB vGPU-48GB-350W; the software environment uses Ubuntu 22.04, Python 3.10.19, PyTorch 2.1.0, CUDA 11.8 and Ultralytics 8.4.24. The number of model training epochs is set to 300, the batch size is set to 16, and the input image size is uniformly adjusted to 640×640. The specific experimental environment configuration is shown in Table 4.1.

**Table 4.1 Experimental environment configuration**

| Environment item | Configuration |
|---|---|
| Python environment | Python 3.10.19 |
| Deep learning libraries | PyTorch 2.1.0, Ultralytics 8.4.24 |
| Model training environment | Ubuntu 22.04, CUDA 11.8, 48 GB vGPU |
| Training parameters | Epoch = 300, Batch Size = 16, Input Size = 640×640 |

### 4.4.2 Evaluation Metrics

This chapter uses standard evaluation metrics from the object detection field to evaluate model performance, including IoU, Precision, Recall, AP, mAP50, mAP50-95, and AP metrics for targets of different scales. The above metrics can comprehensively reflect model performance in terms of localisation accuracy, false-detection control, missed-detection control and multi-scale detection capability.

**Intersection over Union (IoU)** is used to measure the degree of overlap between the predicted box and the ground-truth box, and is the basis for judging whether a prediction is a hit. Its computational formula is:

$$IoU = \frac{S(B_{pred} \cap B_{gt})}{S(B_{pred} \cup B_{gt})} \tag{4.23}$$

where *B_pred* is the model's predicted box, *B_gt* is the ground-truth annotation box, *S*(·) denotes region area, ∩ denotes intersection, and ∪ denotes
union. The larger the IoU value, the higher the degree of overlap between the predicted box and the ground-truth box.

**Precision** denotes the proportion of genuine targets among the samples predicted to be targets; **Recall** denotes the proportion of all true targets that are correctly detected. The two respectively reflect the model's false-detection control capability and missed-detection control capability; their computational formulas are:

$$Precision = \frac{TP}{(TP + FP)} \tag{4.24}$$

$$Recall = \frac{TP}{(TP + FN)} \tag{4.25}$$

--- p.61 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

51

where *TP* is true positives, denoting the number of targets correctly detected; *FP* is false positives, denoting the number incorrectly detected as targets; and *FN* is false negatives, denoting the number of targets that genuinely exist but were not detected.

**AP (Average Precision)** is the area under the Precision–Recall curve, used to measure the comprehensive detection capability for a single class across different confidence thresholds. Its expression is:

$$AP = \int P(R)\,dR \tag{4.26}$$

where *R* denotes recall and *P*(*R*) denotes the precision corresponding to recall *R*. The higher the *AP* value, the better the balance achieved between precision and recall in the detection results for that class.

**mAP50** denotes the comprehensive metric obtained by averaging the AP of all classes at an IoU threshold of 0.50, and is commonly used to measure the overall detection accuracy of an object detection model. Its computational formula is:

$$mAP50 = \frac{(AP_1 + AP_2 + \cdots + AP_C)}{C} \tag{4.27}$$

**mAP50-95** denotes the average obtained by computing mAP separately at 10 IoU thresholds from 0.50 to 0.95 with a step of 0.05, and imposes stricter requirements on localisation accuracy than mAP50. Its computational formula is:

$$mAP50\text{-}95 = \frac{(mAP50 + mAP55 + \cdots + mAP95)}{10} \tag{4.28}$$

where *C* is the total number of target classes and *AP*₁ to *AP_C* respectively denote the average precision of each class. *AP_s*, *AP_m* and *AP_l* respectively denote the average precision for small, medium and large targets, where small targets have an area smaller than 32×32 pixels, medium targets have an area between 32×32 and 96×96 pixels, and large targets have an area greater than 96×96 pixels.

### 4.4.3 Experimental Design and Implementation

To verify the effectiveness of this chapter's improved method, comparative experiments were conducted with the original YOLOv8 as the baseline model, completing training and testing under the same dataset split and the same training hyperparameter settings, ensuring the fairness and reliability of the comparison results. The only difference between the two methods is that this chapter's method replaces the C2f module in the original YOLOv8 with the proposed fine-grained feature extraction module, while the remaining network components are kept identical.

In terms of training strategy, the standard stochastic gradient descent (SGD) optimiser is used in combination with a cosine annealing learning-rate schedule. Multiple data augmentation techniques are used during training, including random horizontal flipping, colour jitter (adjusting brightness, contrast and saturation) and Mosaic augmentation, in order to improve the model's generalisation capability under the variable conditions of underwater scenes.

### 4.4.4 Quantitative Analysis

Table 4.2 presents the quantitative comparison results between this chapter's improved method and the original YOLOv8 on the URPC2021 dataset. *(The original repeats this sentence.)* From the experimental results in Table 4.2 it can be seen that the improved model raises mAP50 from 0.855 to 0.873, and mAP50-95 from

--- p.62 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

52

0.516 to 0.530, indicating that the model maintains higher detection accuracy across different IoU thresholds. Small-target detection capability is clearly enhanced, with APs rising from 0.166 to 0.177; this is mainly attributable to the channel–spatial attention mechanism of CAEM within the FFEM module, which effectively focuses on target edges and details and improves localisation accuracy for small targets such as sea urchins and scallops. Large-target detection performance also improves, with APl rising from 0.664 to 0.675, showing that VSSM's effective modelling of global contextual information provides support for the complete perception of large targets. However, medium-target detection declines slightly, with APm falling from 0.402 to 0.391; this may be because the multi-scale convolution module has a certain scale bias in extracting medium-target features, which requires further optimisation. Overall, the improved model outperforms the original YOLOv8 in comprehensive detection accuracy and in small-target and large-target detection capability, providing a clear direction for subsequent model optimisation. Overall, this chapter's improved method achieves clear improvements in both comprehensive detection metrics and small-target accuracy, verifying the effectiveness of FFEM in the underwater object detection task. *(The original repeats this concluding sentence.)*

**Table 4.2 Comparison of detection performance on the URPC2021 dataset**

| Model | mAP50 | mAP50-95 | APs | APm | APl |
|---|---|---|---|---|---|
| YOLOv8 | 0.855 | 0.516 | 0.166 | 0.402 | 0.664 |
| **Improved YOLOv8** | **0.873** | **0.530** | **0.177** | 0.391 | **0.675** |

To investigate the difference in convergence between the YOLOv8 network models before and after improvement, this thesis conducted training and validation experiments on the original YOLOv8 and the improved YOLOv8 respectively under the same dataset split and the same hyperparameter settings; their training loss, validation loss and main evaluation metric curves are shown in Figure 4.8 and Figure 4.9. As the figures show, the bounding-box loss (BBox Loss), classification loss (Classification Loss) and distribution focal loss (DFL) of both models drop rapidly in the early stages of training and then gradually stabilise, indicating that the models can effectively complete feature learning and enter a converged state. Compared with the original YOLOv8, the improved model's training loss curve declines more smoothly overall; although the validation loss fluctuates slightly in the later stages, it remains stable overall, indicating that the improved structure does not introduce obvious training instability. From the trend of the evaluation metrics, Precision, Recall, mAP50 and mAP50-95 all rise rapidly in the early stages of training and gradually level off in the middle and later stages, indicating that detection performance gradually stabilises as training proceeds. The improved YOLOv8 is slightly better than the original model on final Precision, mAP50 and mAP50-95, indicating a certain improvement in target localisation and category discrimination. Overall, under the same dataset and hyperparameter conditions the improved YOLOv8 maintains good convergence stability and achieves a certain improvement in final detection accuracy, providing experimental evidence for its application in underwater object detection tasks.

--- p.63 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

53

*[Figure: loss curves for YOLOv8 training and validation]*

**Figure 4.8 Loss-function curves for YOLOv8 during training and validation**

*[Figure: loss curves for improved YOLOv8 training and validation]*

**Figure 4.9 Loss-function curves for the improved YOLOv8 during training and validation**

### 4.4.5 Qualitative Analysis

To further verify the actual detection performance of the improved YOLOv8 in complex underwater scenes, this section conducts a qualitative analysis based on representative samples from the URPC2021 validation set, from three perspectives: manual annotation, original YOLOv8 detection results, and improved YOLOv8 detection results. As shown in Figure 4.10, the left column of the figure shows the manual annotation results, the middle column shows the original YOLOv8 detection results, and the right column shows the improved YOLOv8 detection results; two groups of samples are selected for comparison for each of three types of typical difficult scene — low contrast with blurred edges, obvious colour cast with dense small targets, and complex background with occlusion-induced missed detections.

--- p.64 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

54

In underwater images with complex backgrounds and unclear target boundaries, the original YOLOv8 is easily disturbed by seabed texture, suspended particles in the water and uneven illumination, misjudging local background regions as targets or causing the detection box to deviate from the true target boundary. This shows that the fine-grained edge representation capability of the original C2f structure in degraded underwater images remains insufficient. After the improved model introduces CAEM, it can jointly highlight target edges, contours and texture regions through channel attention and spatial attention, causing the model to respond more concentratedly to real targets such as sea cucumbers, sea urchins, scallops and starfish, thereby reducing the risk of false detections caused by complex backgrounds.

In scenes with dense small targets or mutually occluding targets, the original YOLOv8 is relatively sensitive to sea urchin and scallop targets with blurred edges and small scale, and is prone to missed detections or low-confidence detection results. VSSM models long-range dependency relationships through a visual state space model, enabling the network to judge target regions in combination with the global context surrounding the target, compensating for the information deficiency of purely local convolution under occlusion and weak-texture conditions. Therefore, the improved model can maintain more stable target responses in dense small-target and partially occluded scenes.

For underwater targets with pronounced scale variation, MCFM further performs cross-scale fusion of local detail features and global contextual features, enabling the model both to attend to the texture detail of small targets and to maintain perception of the overall morphology of larger targets. In samples where low illumination, colour shift and motion blur coexist, this fusion mechanism helps reduce the judgement bias caused by single-scale features, making the detection box position fit the target contour more closely.

Taken together, the qualitative performance of the improved YOLOv8 is consistent with the quantitative results in Table 4.2. The improvements in mAP50, mAP50-95 and small-target AP show that FFEM not only improves overall detection accuracy but also strengthens the model's adaptability to underwater small targets and complex backgrounds. It can thus be seen that CAEM, VSSM and MCFM respectively improve the robustness of underwater object detection from the three aspects of local detail enhancement, global context modelling and multi-scale feature fusion.

--- p.65 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

55

*[Figure: side-by-side detection comparison grid]*

**Figure 4.10 Comparison of object detection results between the original YOLOv8 and the improved YOLOv8 on the URPC2021 validation set**

### 4.4.6 Ablation Experiments

To further analyse the independent contribution of each constituent sub-module of FFEM to the final detection performance, this section carries out ablation experiments on the URPC2021 dataset. Taking the original YOLOv8 (containing only the C2f module) as the baseline, CAEM, VSSM and MCFM are introduced in turn. The experimental results are shown in Table 4.3, and the heat-map visualisation results are shown in Figure 4.11.

The experimental results show that when CAEM is introduced alone, the heat map shows a clearly enhanced response in small-target regions, echoing the roughly 0.7-percentage-point improvement in mAP50 and roughly 0.5-percentage-point improvement in *AP_s* in the table, indicating that this module plays a significant role in detail perception and small-target detection. When VSSM is introduced alone, the overall heat-map response is more uniform, reflecting the effective modelling of global contextual information, which raises overall detection accuracy, although the improvement in small-target regions is smaller than with

--- p.66 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

56

CAEM. When CAEM and VSSM are used jointly, the heat map shows high response in both small-target and global regions, embodying the complementary synergistic effect of local detail and global information. After MCFM is added, the heat map shows a more prominent response for cross-scale features, and all metrics reach their optimal levels, verifying the key role of MCFM in enhancing the discriminative power of fine-grained features and improving overall performance.

**Table 4.3 Ablation results for each sub-module of the fine-grained feature extraction module**

| Model | CAEM | VSSM | MCFM | mAP50 | mAP50-95 | APs | APm | APl |
|---|---|---|---|---|---|---|---|---|
| YOLOv8 | | | | 0.855 | 0.516 | 0.166 | 0.402 | 0.664 |
| YOLOv8 + CAEM | ✓ | | | 0.862 | 0.521 | 0.171 | 0.399 | 0.667 |
| YOLOv8 + VSSM | | ✓ | | 0.861 | 0.522 | 0.169 | 0.404 | 0.670 |
| YOLOv8 + CAEM + VSSM | ✓ | ✓ | | 0.868 | 0.527 | 0.174 | 0.395 | 0.672 |
| **Improved YOLOv8** | ✓ | ✓ | ✓ | **0.873** | **0.530** | **0.177** | 0.391 | **0.675** |

*Note: the Baseline is the original YOLOv8; "✓" indicates that the sub-module is introduced in the corresponding experimental setting.*

*[Figure content: (a) YOLOv8 | (b) YOLOv8+CAEM | (c) YOLOv8+VSSM | (d) YOLOv8+CAEM+VSSM | (e) Improved YOLOv8]*

**Figure 4.11 Heat-map visualisation effects of the different modules**

## 4.5 Evaluation of Object Detection Performance on Super-Resolution Reconstructed Underwater Images

To quantitatively evaluate the actual gain that super-resolution reconstruction brings to underwater object detection performance, this section designs a set of cascaded comparison experiments of "down-sampling → super-resolution reconstruction → object detection" based on the URPC2021 test set; the overall flow is shown in Figure 4.12. Specifically, the original images in the URPC2021 test set are first passed through bicubic down-sampling (×4 factor) to generate corresponding low-resolution (LR) images, simulating the loss of detail caused by the limited resolution of underwater imaging equipment; the FSCIN proposed in Chapter 3 of this thesis is then used to perform super-resolution reconstruction on the LR images, obtaining high-quality reconstructed images; finally, the three groups of input — LR images, original-resolution images and FSCIN-reconstructed images — are fed separately into the two detection models YOLOv8 [43] and this thesis's improved YOLOv8, with recall and mean average precision (mAP@0.5) as the core evaluation metrics, so as to comprehensively measure the influence of SR reconstruction quality on downstream detection performance [68][69].

--- p.67 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

57

*[Figure: schematic of the FSCIN → improved YOLOv8 cascade]*

**Figure 4.12 Schematic of how FSCIN super-resolution reconstruction promotes improved-YOLOv8 underwater object detection**

Figure 4.13 shows the recall comparison results of the three schemes — direct detection on LR low-resolution images, direct detection at original resolution, and detection after FSCIN super-resolution reconstruction — on YOLOv8 and on the improved YOLOv8. From the figure it can be seen that: (1) direct LR detection achieves recall of only 69.8% and 71.4% on YOLOv8 and the improved YOLOv8 respectively, with low-resolution input severely constraining target retrieval capability; (2) original-resolution detection raises recall to 76.5% and 77.9% respectively, showing that restoring resolution has a clear positive effect on detection recall; (3) detection after FSCIN super-resolution reconstruction achieves the highest recall — 80.8% (YOLOv8) and 82.5% (improved YOLOv8) — improvements of 11.0 and 11.1 percentage points respectively over the LR baseline, strongly verifying the outstanding capability of FSCIN's frequency–spatial coupled design in restoring target detail. In addition, the improved YOLOv8 achieves higher recall than the original YOLOv8 under all three schemes, with the gap between the two stable at 1.4–1.7 percentage points, indicating a stable positive additive effect between the detection model's own fine-grained feature enhancement and SR pre-processing.

*[Figure: recall comparison bar chart]*

**Figure 4.13 Recall comparison for detection on LR, original-resolution and FSCIN-reconstructed images**

Figure 4.14 further presents the comparison results of the three schemes on the mAP@0.5 metric. The overall trend is consistent with recall: direct LR detection achieves mAP of only 74.5% (YOLOv8) and 76.2% (improved YOLOv8) on the two models;

--- p.68 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

58

original-resolution detection raises these to 81.8% and 83.2%; and detection after FSCIN reconstruction establishes a leading position with the best mAP of 85.8% (YOLOv8) and 87.7% (improved YOLOv8), improvements of 11.3 and 11.5 percentage points respectively over the LR baseline. It is worth noting that the mAP@0.5 of FSCIN combined with the improved YOLOv8 (87.7%) already exceeds the detection accuracy of the improved YOLOv8 on the original URPC2021 images (87.3%, see Table 4.2), showing that reconstructed images enhanced by FSCIN super-resolution can provide the object detection model with richer discriminative features than the original images, further verifying the synergistic advantage of the "enhancement–detection" cascaded framework.

*[Figure: mAP@0.5 comparison bar chart]*

**Figure 4.14 mAP@0.5 comparison for detection on LR, original-resolution and FSCIN-reconstructed images**

To further verify the actual gain of super-resolution reconstruction for detection performance at the visual level, Figure 4.15 takes three representative underwater scenes from the DUO dataset as examples, showing a comparison of three columns of results: direct detection on LR low-resolution images, direct detection at original resolution, and detection after FSCIN super-resolution reconstruction. The three scenes cover different detection difficulties: normal density (Scene 1, scallop ×5 + sea cucumber ×2, 7 targets in total), high density (Scene 2, scallop ×14 + sea cucumber ×13, 27 targets in total) and all four classes (Scene 3, scallop + sea urchin + starfish + sea cucumber, 18 targets in total). From the figure it can be intuitively seen that: (1) because the LR images are severely limited in resolution, the number of detection boxes is smallest and confidences are generally low (0.42–0.56), with a large number of targets missed in the high-density scene; (2) detection performance on original-resolution images improves somewhat, with both the number detected and the confidence (0.58–0.76) rising, but some missed detections still occur in dense-target and blurred-edge scenes; (3) after FSCIN reconstruction, the detection boxes cover all true targets with none omitted, and confidence rises significantly to 0.80–0.94 — all 7 targets in Scene 1 are detected, all 27 targets in Scene 2 are completely detected, and the 18 targets in Scene 3 cover all four classes of scallop, sea urchin, starfish and sea cucumber. The above qualitative comparison corroborates the quantitative results of Section 4.4.5, intuitively demonstrating the significant improvement that FSCIN super-resolution reconstruction brings to the completeness of object detection in underwater scenes of different densities and multiple classes [70][71].

--- p.69 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

59

*[Figure: detection comparison before and after super-resolution reconstruction]*

**Figure 4.15 Comparison of underwater object detection results before and after super-resolution reconstruction**

Synthesising the above quantitative and qualitative analyses, the following three conclusions can be drawn: (1) super-resolution reconstruction has a significant promoting effect on underwater object detection performance — direct LR detection has the lowest recall and mAP, while both metrics for detection after FSCIN super-resolution reconstruction lead by a large margin, and the higher the SR reconstruction quality, the more pronounced the improvement in downstream detection performance; (2) FSCIN's frequency–spatial coupled design has a clear advantage in restoring target edges, textures and local contrast, and its reconstruction results can provide higher-quality input features for the detection network, a point that is especially prominent in small-target and dense scenes; (3) there is a complementary synergistic effect between SR pre-processing and detection model improvement — FSCIN reduces the impact of underwater degradation at the input-quality level, while FFEM enhances the model's perception capability for underwater targets at the feature-extraction level, and the performance gain of using the two in combination is greater than the sum of the gains from using each individually. It should be noted that super-resolution reconstruction is not simply image enlargement; its core lies in restoring genuine high-frequency information by learning the mapping relationship from LR to HR. If the reconstruction process introduces artefacts or over-sharpening, it may instead interfere with the detection model's judgement. Therefore, FSCIN's design places particular emphasis on the texture–structure joint loss constraining genuine detail, effectively avoiding the above risk [72].

In summary, through systematic cascaded comparison experiments, this section has verified the significant promoting effect of FSCIN super-resolution reconstruction on underwater object detection along three dimensions: recall, mAP and qualitative visualisation. The quantitative results show that the combined scheme of FSCIN + improved YOLOv8 achieves 82.5% recall and 87.7% mAP@0.5 under ×4 down-sampling-and-reconstruction conditions on the URPC2021 dataset, improvements of 11.1 and 11.5 percentage points respectively over the LR baseline; the qualitative results show that in three

--- p.70 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

60

scene groups of differing density from the DUO dataset, the detection boxes after FSCIN reconstruction can cover all true targets, a qualitative improvement over LR and original-resolution detection. The above results fully demonstrate the effectiveness and practicality of this thesis's cascaded framework of "super-resolution enhancement first, object detection second".

## 4.6 Chapter Summary

Addressing problems such as YOLOv8's insufficient global modelling capability and limited small-target feature representation in the underwater image object detection task, this chapter has proposed an underwater image object detection model based on an improved YOLOv8, replacing the original C2f module with the designed FFEM. The main work can be summarised in the following three aspects:

**1. Design of the channel–spatial adaptive enhancement module.** Local spatial detail of targets is extracted through cascaded 3×3 convolutions, while a dual weighting mechanism of channel attention (based on global average pooling and 1×1 convolution) and spatial attention (based on 7×7 convolution) is introduced, enabling the module to adaptively focus on target edge and texture regions, effectively suppressing interference from underwater background noise and significantly improving localisation accuracy for tiny targets.

**2. Design of the Mamba-based global perception module.** By introducing a two-dimensional state space model (2D-SSM), global spatial dependency relationships in the image are modelled with linear complexity, breaking through the inherent limitation of the convolutional neural network's local receptive field; combined with the local spatial perception of depthwise separable convolution, the non-linear representation of the SiLU activation function, and the adaptive information screening of the gated fusion mechanism, this effectively captures global contextual features in underwater scenes and strengthens the model's adaptability to the global blur problem of underwater images.

**3. Design of the multi-scale cross-attention fusion module.** Asymmetric convolution combinations are used to extract spatial features at different scales, and local features and global features are dynamically weighted and fused through a cross-scale attention interaction mechanism, achieving efficient integration of multi-scale discriminative features.

Experiments on the URPC2021 underwater object detection dataset show that, compared with the original YOLOv8, this chapter's improved method raises mAP50 by 1.8 percentage points and small-target APs by 1.1 percentage points, effectively verifying the comprehensive improvement the proposed method brings to underwater object detection performance. Combined with the pre-processing results of the FSCIN super-resolution reconstruction module in Chapter 3, the organic combination of the two lays a solid technical foundation for building a complete underwater visual perception system. *(The content of this chapter has been filed as an invention patent, "An Improved YOLOv8 Underwater Image Object Detection Method, Apparatus, Medium and Program", which has currently entered the substantive examination stage.)*

--- p.71 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

61

# Chapter 5 Conclusions and Outlook

## 5.1 Conclusions

This thesis has focused on two core problems in underwater vision systems — image super-resolution reconstruction and object detection — proposing two improved deep-learning-based methods and verifying their effectiveness through systematic experiments on public datasets. The main research results are summarised as follows.

**(1) The Frequency–Spatial Coupled Inference Network (FSCIN).** Addressing the problem that existing super-resolution methods model only in the spatial domain and make insufficient use of frequency-domain priors, the FSCIN network was proposed. At the module design level, the core contribution is the spatial–frequency awareness module (SFAM): after mapping features into the frequency domain through FFT, a dual-branch Swin Transformer attention structure adaptively enhances the amplitude spectrum and phase spectrum separately, and then IFFT restores them to the spatial domain, achieving deep fusion of frequency-domain global perception and spatial-domain local modelling. At the loss function level, a texture–structure joint loss was proposed which, through the coordinated action of gradient-domain texture constraints and structure-extractor structural constraints, provides a more targeted supervisory signal for the recovery of high-frequency detail and geometric edges. On the two benchmark datasets USR-248 and UFO-120, FSCIN achieved optimal or highly competitive PSNR, SSIM and UIQM metrics at multiple magnification factors, while also demonstrating clearer texture restoration capability and more accurate structural fidelity in terms of visual quality.

**(2) The improved YOLOv8 underwater object detection model.** Addressing the limitations of the original YOLOv8's C2f module in global dependency modelling and fine-grained small-target feature representation, FFEM was designed as a replacement component. CAEM precisely focuses on target edge contours and texture details through a channel–spatial dual attention mechanism, effectively suppressing interference from underwater background noise; VSSM introduces a two-dimensional state space model to model global spatial dependencies in the image with linear complexity, breaking through the inherent limitation of the convolutional network's local receptive field; MCFM extracts multi-scale features through asymmetric convolution and performs cross-scale attention interaction, adaptively integrating the two complementary feature streams. On the URPC2021 dataset, the improved model raises mAP50 by 1.8 percentage points and small-target APs by 1.1 percentage points compared with the original YOLOv8.

**(3) The overall technical framework.** This thesis organically connects the FSCIN super-resolution reconstruction module with the improved YOLOv8 object detection module, constructing a cascaded processing framework of "super-resolution enhancement first, object detection second", providing a complete technical solution for underwater visual perception systems.

Taken together, the FSCIN super-resolution reconstruction method and the improved YOLOv8 object detection method proposed in this thesis form a complementary technical route — FSCIN improves the perceptual quality and texture detail of images from the frequency-domain dimension, providing higher-quality input for the improved YOLOv8; the improved YOLOv8, through fine-grained feature extraction and global perception modelling, enhances detection robustness for tiny underwater targets. The organic combination of the two constitutes a complete enhancement–perception technical chain oriented towards underwater visual scenes, laying a foundation for subsequent engineering implementation.

--- p.72 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

62

## 5.2 Outlook

Although the methods proposed in this thesis have achieved certain results, several directions remain worth exploring further:

**(1) Lightweighting and real-time deployment.** At present FSCIN has 30.70 G FLOPs at ×2 magnification, which still places a certain pressure on embedded underwater platforms with limited computing power (such as AUVs and ROVs). In future, model compression techniques such as knowledge distillation, network pruning and quantisation could be explored to reduce inference overhead while maintaining reconstruction quality, promoting the engineering implementation of the method in real equipment.

**(2) End-to-end multi-task joint optimisation.** This thesis designs super-resolution reconstruction and object detection as cascaded independent
modules. However, there is an intrinsic semantic association between the two tasks, and a joint training framework could further improve overall performance through inter-task gradient sharing and complementary supervision. In future, an end-to-end multi-task network could be designed to explore collaborative optimisation strategies for the two tasks.

**(3) Generalisation capability for compound degradation scenarios.** The datasets in this thesis mainly simulate bicubic down-sampling and Gaussian noise degradation, whereas real underwater scenes often simultaneously exhibit multiple compound degradation types such as motion blur, non-uniform illumination and occlusion by plankton. In future, richer underwater degradation datasets should be constructed and models designed that are more robust to complex mixed degradation.

**(4) Deeper exploration of frequency-domain modelling mechanisms.** The SFAM in this thesis adopts an amplitude–phase dual-branch strategy and has already achieved good results. In future, the introduction of multi-scale frequency analysis tools such as the wavelet transform and Gabor filters could be further explored, or an adaptive frequency selection mechanism designed, so as to model the frequency characteristics of underwater images more precisely.

**(5) Larger-scale and more diverse object detection datasets.** URPC2021 covers only four classes of underwater target and cannot fully reflect the diversity of real underwater ecosystems. In future, annotated data of more classes and larger scale could be collected, combined with generative adversarial networks to synthesise underwater degraded images for data augmentation, further improving the model's inter-class discriminative capability and cross-scene generalisation capability.

**(6) Fusion with cutting-edge generative techniques.** Diffusion models have demonstrated powerful generative capability in the field of image restoration; in future, attempts could be made to introduce diffusion priors into the underwater image super-resolution framework, exploring their potential to further improve perceptual quality.

--- p.73 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

63

# REFERENCES

[1] Dong C, Loy C C, He K, et al. Image super-resolution using deep convolutional networks[J]. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2016, 38(2): 295-307.

[2] Kim J, Lee J K, Lee K M. Accurate image super-resolution using very deep convolutional networks[A]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition[C]. Las Vegas: IEEE, 2016: 1646-1654.

[3] Lim B, Son S, Kim H, et al. Enhanced deep residual networks for single image super-resolution[A]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition Workshops[C]. Honolulu: IEEE, 2017: 136-144.

[4] Zhang Y, Tian Y, Kong Y, et al. Residual dense network for image super-resolution[A]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition[C]. Salt Lake City: IEEE, 2018: 2472-2481.

[5] Zhang Y, Li K, Li K, et al. Image super-resolution using very deep residual channel attention networks[A]. Proceedings of the European Conference on Computer Vision[C]. Munich: Springer, 2018: 286-301.

[6] Goodfellow I, Pouget-Abadie J, Mirza M, et al. Generative adversarial nets[A]. Advances in Neural Information Processing Systems[C]. Montreal: MIT Press, 2014: 2672-2680.

[7] Ledig C, Theis L, Huszár F, et al. Photo-realistic single image super-resolution using a generative adversarial network[A]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition[C]. Honolulu: IEEE, 2017: 4681-4690.

[8] Wang X, Yu K, Wu S, et al. ESRGAN: Enhanced super-resolution generative adversarial networks[A]. Proceedings of the European Conference on Computer Vision Workshops[C]. Munich: Springer, 2018: 1-9.

[9] Zhao Ran, Yuan Jiabin, Fan Lili. A medical ultrasound image super-resolution reconstruction method based on video multi-frame fusion[J]. Computer Science, 2023, 50(7): 143-151. *(in Chinese)*

[10] Ran Wenbing, Liang Yongchao, Qin Qin, et al. Medical image super-resolution reconstruction based on generative adversarial networks and attention mechanisms[J]. Intelligent Computer and Applications, 2023, 13(1): 136-141. *(in Chinese)*

[11] Zhao Huiyan, Li Yunhe. Super-resolution analysis of Sentinel-2 remote sensing images based on generative adversarial networks[J]. Journal of Computer Applications, 2022, 42(z1): 298-304. *(in Chinese)*

--- p.74 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

64

[12] Zhang Yan, Wang Tao, Xu Qing, et al. Super-resolution reconstruction of HBE satellite remote sensing images based on the HMRF prior model[J]. Geomatics and Information Science of Wuhan University, 2007, 32(7): 589-592. *(in Chinese)*

[13] Yang Aiping, Zheng Jia, Wang Jian, et al. Underwater image restoration based on colour distortion removal and the dark channel prior[J]. Journal of Electronics & Information Technology, 2015, 37(11): 2580-2586. *(in Chinese)*

[14] Yang Aiping, Tian Xin, Yang Bingwang, et al. Single underwater image sharpening based on multi-feature fusion[J]. Journal of Tianjin University (Science and Technology), 2018, 51(10): 1031-1041. *(in Chinese)*

[15] Islam M J, Enan S S, Luo P, et al. Underwater image super-resolution using deep residual multipliers[A]. 2020 IEEE International Conference on Robotics and Automation[C]. Paris: IEEE, 2020: 900-906.

[16] Islam M J, Luo P, Sattar J. Simultaneous enhancement and super-resolution of underwater imagery for improved visual perception[J/OL]. arXiv, 2020[2024-03-01]. https://arxiv.org/abs/2002.01155.

[17] Zhang Y, Yang S, Sun Y, et al. Attention-guided multi-path cross-CNN for underwater image super-resolution[J]. Signal, Image and Video Processing, 2022, 16(1): 155-163.

[18] Ren T, Xu H, Jiang G, et al. Reinforced Swin-Convs Transformer for simultaneous underwater sensing scene image enhancement and super-resolution[J]. IEEE Transactions on Geoscience and Remote Sensing, 2022, 60: 1-16.

[19] Sharma P, Bisht I, Sur A. Wavelength-based attributed deep neural network for underwater image restoration[J]. ACM Transactions on Multimedia Computing, Communications and Applications, 2023, 19(1): 1-23.

[20] Chen Z, Liu C, Zhang K, et al. Underwater-image super-resolution via range-dependency learning of multiscale features[J]. Computers and Electrical Engineering, 2023, 110: 108756.

[21] Chen X, Wei S, Yi C, et al. Progressive attentional learning for underwater image super-resolution[A]. Proceedings of the 13th International Conference on Intelligent Robotics and Applications[C]. Kuala Lumpur: Springer, 2020: 233-243.

[22] Cherian A K, Poovammal E. A novel AlphaSRGAN for underwater image super resolution[J]. Computers, Materials & Continua, 2021, 69(2): 1537-1552.

[23] Pramanick A, Sur A, Saradhi V V. Harnessing multi-resolution and multi-scale attention for underwater image restoration[J]. The Visual Computer, 2025. DOI:10.1007/s00371-025-03866-0.

--- p.75 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

65

[24] Liu S, Ding Y, Tian N, et al. Decouple-to-Fuse: Saliency guided Dual-Branch Framework for Underwater Image Enhancement and Super Resolution[J]. Information Fusion, 2026, 135: 104448. DOI:10.1016/j.inffus.2026.104448.

[25] Wu H, Wang H, Zhang Y, et al. An attempt at underwater image lightweight super-resolution using transformer and frequency-domain learning[J]. Frontiers in Marine Science, 2026, 13: 1762772. DOI:10.3389/fmars.2026.1762772.

[26] Dharejo F A, Ganapathi I I, Zawish M, et al. SwinWave-SR: Multi-scale lightweight underwater image super-resolution[J]. Information Fusion, 2024, 103: 102127.

[27] Chen Y, Niu K, Zeng Z, et al. A wavelet based deep learning method for underwater image super resolution reconstruction[J]. IEEE Access, 2020, 8: 117759-117769.

[28] Wang C, Jiang J, Zhong Z, et al. Spatial-frequency mutual learning for face super-resolution[A]. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition[C]. Vancouver: IEEE, 2023: 22356-22366.

[29] Zhou F, Chen Q, Liu B, et al. Structure and texture-aware image decomposition via training a neural network[J]. IEEE Transactions on Image Processing, 2020, 29: 3458-3473.

[30] Liu Z, Lin Y, Cao Y, et al. Swin Transformer: Hierarchical vision transformer using shifted windows[A]. Proceedings of the IEEE/CVF International Conference on Computer Vision[C]. Montreal: IEEE, 2021: 9992-10002.

[31] Liang J, Cao J, Sun G, et al. SwinIR: Image restoration using Swin Transformer[A]. Proceedings of the IEEE/CVF International Conference on Computer Vision Workshops[C]. Montreal: IEEE, 2021: 1833-1844.

[32] Wang D, Sun Z. Frequency domain based learning with Transformer for underwater image restoration[A]. Trends in Artificial Intelligence[C]. Cham: Springer, 2022, 13629: 218-232.

[33] Shen Z, Xu H, Luo T, et al. UDAformer: Underwater image enhancement based on dual attention Transformer[J]. Computers & Graphics, 2023, 111: 77-88.

[34] Peng L, Zhu C, Bian L. U-Shape Transformer for underwater image enhancement[J]. IEEE Transactions on Image Processing, 2023, 32: 3066-3079.

[35] Girshick R, Donahue J, Darrell T, et al. Rich feature hierarchies for accurate object detection and semantic segmentation[A]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition[C]. Columbus: IEEE, 2014: 580-587.

[36] Girshick R. Fast R-CNN[A]. Proceedings of the IEEE International Conference on Computer Vision[C]. Santiago: IEEE, 2015: 1440-1448.

--- p.76 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

66

[37] Ren S, He K, Girshick R, et al. Faster R-CNN: Towards real-time object detection with region proposal networks[J]. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2017, 39(6): 1137-1149.

[38] Lin T Y, Dollár P, Girshick R, et al. Feature pyramid networks for object detection[A]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition[C]. Honolulu: IEEE, 2017: 2117-2125.

[39] Jia J, Fu M, Liu X, et al. Underwater object detection based on improved EfficientDet[J]. Remote Sensing, 2022, 14(18): 4487. DOI:10.3390/rs14184487.

[40] Redmon J, Divvala S, Girshick R, et al. You only look once: Unified, real-time object detection[A]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition[C]. Las Vegas: IEEE, 2016: 779-788.

[41] Bochkovskiy A, Wang C Y, Liao H Y M. YOLOv4: Optimal speed and accuracy of object detection[J/OL]. arXiv, 2020[2024-03-01]. https://arxiv.org/abs/2004.10934.

[42] Jocher G, Stoken A, Chaurasia A, et al. ultralytics/yolov5: v6.0 - YOLOv5n 'Nano' models, Roboflow integration, TensorFlow export, OpenCV DNN support[EB/OL]. Zenodo, 2021. DOI:10.5281/zenodo.5563715.

[43] Jocher G, Chaurasia A, Qiu J. Ultralytics YOLOv8[EB/OL]. Ultralytics, 2023[2024-03-01]. https://github.com/ultralytics/ultralytics.

[44] Liu W, Anguelov D, Erhan D, et al. SSD: Single shot multibox detector[A]. Proceedings of the European Conference on Computer Vision[C]. Amsterdam: Springer, 2016: 21-37.

[45] Lin T Y, Goyal P, Girshick R, et al. Focal loss for dense object detection[A]. Proceedings of the IEEE International Conference on Computer Vision[C]. Venice: IEEE, 2017: 2980-2988.

[46] Hu J, Shen L, Sun G. Squeeze-and-excitation networks[A]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition[C]. Salt Lake City: IEEE, 2018: 7132-7141.

[47] Woo S, Park J, Lee J Y, et al. CBAM: Convolutional block attention module[A]. Proceedings of the European Conference on Computer Vision[C]. Munich: Springer, 2018: 3-19.

[48] Gong R, Xu J, Zheng Z, et al. YOLO-Starfish: fish object detection learning complex underwater features[J]. Scientific Reports, 2026, 16: 13964. DOI:10.1038/s41598-026-44187-z.

--- p.77 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

67

[49] Gang Y, Li T, Li S, et al. YOLO-MFD: a multi-scale feature and dynamic head framework for prefabricated shoreline underwater object detection[J]. Scientific Reports, 2026, 16: 10971. DOI:10.1038/s41598-026-45591-1.

[50] Dosovitskiy A, Beyer L, Kolesnikov A, et al. An image is worth 16×16 words: Transformers for image recognition at scale[A]. International Conference on Learning Representations[C]. Vienna: ICLR, 2021.

[51] Carion N, Massa F, Synnaeve G, et al. End-to-end object detection with Transformers[A]. Proceedings of the European Conference on Computer Vision[C]. Glasgow: Springer, 2020: 213-229.

[52] Zhu X, Su W, Lu L, et al. Deformable DETR: Deformable Transformers for end-to-end object detection[A]. International Conference on Learning Representations[C]. Virtual: ICLR, 2021.

[53] Gu A, Goel K, Ré C. Efficiently modeling long sequences with structured state spaces[A]. International Conference on Learning Representations[C]. Virtual: ICLR, 2022.

[54] Gu A, Dao T. Mamba: Linear-time sequence modeling with selective state spaces[J/OL]. arXiv, 2024[2024-03-01]. https://arxiv.org/abs/2312.00752.

[55] Rumelhart D E, Hinton G E, Williams R J. Learning representations by back-propagating errors[J]. Nature, 1986, 323(6088): 533-536.

[56] LeCun Y, Boser B, Denker J S, et al. Backpropagation applied to handwritten zip code recognition[J]. Neural Computation, 1989, 1(4): 541-551.

[57] He K, Zhang X, Ren S, et al. Deep residual learning for image recognition[A]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition[C]. Las Vegas: IEEE, 2016: 770-778.

[58] Kim J, Lee J K, Lee K M. Deeply-recursive convolutional network for image super-resolution[A]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition[C]. Las Vegas: IEEE, 2016: 1637-1645.

[59] Huang G, Liu Z, Van Der Maaten L, et al. Densely connected convolutional networks[A]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition[C]. Honolulu: IEEE, 2017: 4700-4708.

[60] Tong T, Li G, Liu X, et al. Image super-resolution using dense skip connections[A]. Proceedings of the IEEE International Conference on Computer Vision[C]. Venice: IEEE, 2017: 4799-4807.

[61] Vaswani A, Shazeer N, Parmar N, et al. Attention is all you need[A]. Advances in Neural Information Processing Systems[C]. Long Beach: MIT Press, 2017: 5998-6008.

--- p.78 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

68

[62] Long J, Shelhamer E, Darrell T. Fully convolutional networks for semantic segmentation[C]//Proceedings of the IEEE conference on computer vision and pattern recognition. 2015: 3431-3440.

[63] Shi W, Caballero J, Huszár F, et al. Real-time single image and video super-resolution using an efficient sub-pixel convolutional neural network[C]//Proceedings of the IEEE conference on computer vision and pattern recognition. 2016: 1874-1883.

[64] Cheng Guangquan, Cheng Lizhi. Wavelet-based direction-adaptive image interpolation[J]. Journal of Electronics & Information Technology, 2009, 31(2): 265-269. *(in Chinese)*

[65] Huynh-Thu Q, Ghanbari M. Scope of validity of PSNR in image/video quality assessment[J]. Electronics Letters, 2008, 44(13): 800-801.

[66] Wang Z, Bovik A C, Sheikh H R, et al. Image quality assessment: From error visibility to structural similarity[J]. IEEE Transactions on Image Processing, 2004, 13(4): 600-612.

[67] Panetta K, Gao C, Agaian S. Human-visual-system-inspired underwater image quality measures[J]. IEEE Journal of Oceanic Engineering, 2016, 41(3): 541-551.

--- p.79 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

69

*(blank page)*

--- p.80 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

70

# ACKNOWLEDGEMENTS

As I lay down my pen on this thesis, early summer is just arriving outside my window. Counting it up, this is the eighteenth year of my studies.

I was born into a registered low-income household. Throughout eighteen years of schooling, support from the state and from my school has been there from beginning to end — grants arriving on time, tuition waivers actually implemented, living allowances disbursed. These seemingly procedural arrangements meant, for a child from a poor family, not having to worry about tuition at the start of every term, not having to weigh classes against making a living over and over again. I know well that being able to sit calmly in a classroom and finish these eighteen years of study rests on the strength of far too many people lifting me up. I hold that kindness in my heart.

I thank my parents. You are not highly educated and cannot articulate grand principles, but from childhood to now you have never once said to me, "Stop studying." In the hardest years at home, you carried all the pressure yourselves, and what you left for me was only one sentence: "You just study." Now that I am about to walk out of the school gate, looking back on the road I have travelled I have gradually come to understand that the bitterness you swallowed and the hardships you hid in those years were far, far more than I could imagine. This debt is too heavy for me to repay; I can only walk every step ahead well, so that you feel these years of sacrifice were worth it.

The writing of this graduation thesis has been, for me, a difficult and profound trial. Here, I wish to express my deepest gratitude and apologies to my supervisor, **Teacher Wang Li**. From topic selection to final draft, the thesis went through several revisions, and each draft I submitted came back covered in dense annotations. More than once I felt ashamed — the logic not rigorous enough, the expression not precise enough, the data analysis not solid enough. But Teacher Wang never rebuked me; she simply pushed the thesis back and said calmly, "Revise it again." Thinking about it now, it was precisely these repeated "revise it agains" that gradually made me understand what rigour is and what solidity is. Teacher Wang, thank you for your strictness, and thank you even more for your patience. What you taught me by word and example was far more than how to write a thesis — it was a fundamental attitude towards scholarship and towards doing things.

I thank every teacher who has taught me over these eighteen years. My primary school teachers taught me to read and count; my middle school English teacher did not give up on me even when I came last in exam after exam, but instead gave me special care; my university lecturers gave everything they had from the lectern. You may not remember every student, but the students remember you. It was your lessons one by one, your corrections one by one, your reminders one by one, that taught me from an ignorant child to who I am today.

For five years, my girlfriend **Chen Shuzhuo** has been by my side throughout. These five years happen to span my entire university career, and happen to be the most anxious and most confused stretch of my life. She has seen me at a loss in front of the computer, seen me silent all day because a project was stuck, and seen me pacing back and forth in self-doubt. She could not solve all my confusions, but she did not leave. Her companionship has been quiet and enduring, like a lamp that never goes out. Such affection I can only repay by treating her earnestly for the rest of my life.

Writing to this page means my time as a student is drawing to a close. It would be false to say I am not confused. This identity has been with me for eighteen years, and once set down the road ahead is not yet clear. But I am not afraid because of that. Eighteen years were not easy, and since I have walked all the way here,

--- p.81 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

71

it must mean I have something in me after all — perhaps not talent, but a kind of resilience that gets back up no matter how many times it falls. I believe that the late nights endured, the sweat shed and the grievances swallowed will, at some moment in the future, settle into the confidence to go forward.

I thank every teacher, classmate and friend I met along these eighteen years. It was the tireless teaching from the lectern, the days and nights bent over desks side by side in classrooms, the few casual words of encouragement in corridors, that paved, bit by bit, the road beneath my feet. Some people may have passed through only briefly, but I remember every kindness of those moments. I also thank the teachers who led me through the door in class, the classmates who patted me on the shoulder in the corridor, and the strangers who showed me kindness without thinking about it. You may not have noticed, but every small illumination has made me the better person I am today.

Graduation is not the end of the gathering, but carrying all that light with me to somewhere further away.

Carrying this weighty gratitude, I am willing to become a young person who is warm and steadfast, ordinary yet not mediocre, and genuinely useful to this country and this society.

The road is still long, but with gratitude in my heart, every step beneath my feet has somewhere it came from.

--- p.82 ---

*Research on Underwater Image Super-Resolution Reconstruction and Object Detection Methods Based on Deep Learning*

72

# APPENDIX

## Appendix A Research Achievements Obtained During the Bachelor's Degree

[1] **Li Wang, Bixuan Wang, Jun Zhu, Zhaoxin Yue, Xin Liu, Kaixuan Li.** Frequency-Spatial Coupled Inference Network for Underwater Image Super-Resolution[A]. The 5th International Conference on Applied Mathematics, Modeling and Computer Simulation (AMMCS)[C]. 2025: 1-7.

[2] **Li Kaixuan, Wang Li, Chen Shuzhuo, Yin Zihang, Zhu Jun.** An Improved YOLOv8 Underwater Image Object Detection Method, Apparatus, Medium and Program[P]. Chinese invention patent, application number: **202510291747.5**, 2025-03-12.

[3] **Nanjing Vocational University of Industry Technology; Li Kaixuan, Wang Li, Chen Shuzhuo, Zhu Jun, Yin Zihang.** Deep-Learning-Based Underwater Image Sharpening and Object Detection Platform[Z]. Computer software copyright, registration number: **2025SR0806055**, 2025-05-16.

[4] **Nanjing Vocational University of Industry Technology; Li Kaixuan, Ma Yanqin, Chen Shuzhuo, Shi Jun, Sun Xinxuan, Wang Beibei, Sun Jin.** Detection System for Non-Motor-Vehicle Riders Not Wearing Helmets for Smart City Application Scenarios[Z]. Computer software copyright, registration number: **2024SR0749167**, 2024-05-31.

## Appendix B Research Projects Led or Participated In During the Bachelor's Degree

1. **Principal investigator**, *Research on Deep-Learning-Based Underwater Image Sharpening and Object Detection Methods*, 2024 Jiangsu Province Vocational College Student Innovation and Entrepreneurship Cultivation Programme Project, project number: **GX-2024-0017**.

2. **Participant**, *Research on PCB Surface Defect Detection Based on Template Matching*, 2022 university-level College Student Innovation and Entrepreneurship Training Programme general project.

## Appendix C Main Awards Received During the Bachelor's Degree

1. Third prize, the 20th National Higher Vocational Colleges "Invention Cup" College Student Patent Innovation and Entrepreneurship Competition, *Research on Deep-Learning-Based Underwater Image Sharpening and Object Detection Methods*, Li Kaixuan, Chen Shuzhuo, Wang Bo, Zhou Qiaoyu.

2. Award of excellence, the "Guoji Cup" First Industrial Intelligent Agent Competition, *Intelligent Underwater Image Processing and Industrial Application Verification*, Wang Li, Zeng Tao, Guo Changrui, Yin Zihang, Zhu Yunxi, Li Kaixuan, Chen Shuzhuo.

3. Third prize, the 2022 iCAN College Student Innovation and Entrepreneurship Competition Jiangsu–Zhejiang regional qualifier, *"Smart Sky Eye" — Intelligent Monitoring and Recognition System for Objects Thrown from Height*, Peng Xu, Li Kaixuan, Ou Wen, Hu Jinghao, Wang Jian.

--- p.83 ---

*Nanjing Vocational University of Industry Technology — Graduation Design (Thesis)*

73

4. Third prize, the 17th National Higher Vocational Colleges "Invention Cup" College Student Patent Innovation and Entrepreneurship Competition, *An Intelligent Grasping Method for Mobile Robots Based on Monocular Vision Guidance*, Li Kaixuan, Chen Shuzhuo, Wang Jian, Li Ruixian, Qian Feiyu.

5. Third prize, the 6th Jiangsu Province Intelligent (Virtual) Instrument Competition, *Tai Chi AI-Assisted Training System*, Ou Wen, Li Kaixuan, Yao Zhifeng, Wang Yang, Peng Xu.

6. 2023 Nanjing Vocational University of Industry Technology College Student Summer Social Practice Outstanding Team (team leader of the "IT Intern Programme Practice Team").

7. National Encouragement Scholarship, academic year 2024-2025.

8. Huang Yanpei Outstanding Student Academic Scholarship.

9. Pengyuan Qihang Scholarship.

10. Merit Student; Outstanding Student Cadre; Advanced Individual in Spiritual Civilisation; Advanced Individual in Social Service; Advanced Individual in Self-Reliance; Advanced Individual in Professional Study; Outstanding Volunteer; First Prize, Professional Study Master.

---

*End of document — 83 pages translated.*
