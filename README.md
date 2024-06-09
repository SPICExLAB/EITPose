# EITPose
This is a research repository for [EITPose: Wearable and Practical Electrical Impedance Tomography for Continuous Hand Pose Estimation]() (CHI 2024). It contains the following:

![](https://github.com/SPICExLAB/EITPose/blob/main/media/media1.gif?raw=true)
![](https://github.com/SPICExLAB/EITPose/blob/main/media/media2.gif?raw=true)

- Datasets for the 3 evaluations described in the paper: 
    - EIT/hand pose within sessions, across sessions, across users
    - EIT/hand pose within sessions across a long period of time
    - EIT/hand gesture within sessions and across users
- Data Visualizer for the provided datasets
- Evaluation experiments:
    - MPJPE Within Session
    - MPJPE Cross Session
    - MPJPE Cross User
    - MPJPE Longitudinal
    - Gesture Classification Within Session
    - Gesture Classification Cross User

## File Structure
```
EITPose
|- src
    |- analysis
        |- evaluation
            |- experiment_mpjpe_within_session.py: MPJPE within session
            |- experiment_mpjpe_cross_session.py: MPJPE cross session
            |- experiment_mpjpe_cross_user.py: MPJPE cross user
            |- experiment_mpjpe_longitudinal.py: MPJPE within session during longitudinal study
            |- experiment_cls_within_session.py: Gesture classification within session
            |- experiment_cls_cross_user.py: Gesture Classification cross user
            |- experiment_results: folder containing output of experiments
        |- models - models used during evaluation
        |- preprocessing - helper files
    |- data
        |- processed_gesture_data: dataset with matched EIT data and labeled gestures
        |- processed_longitudinal_data: dataset with matched EIT data and hand poses during the longitudinal study
        |- processed_pose_data: dataset with matched EIT data and hand poses during cross session and cross user study
    |- data_visualizer
        |- DataComparator.py: GUI application to visualize various datasets
```

## Demos

### Data Visualizer
Change Directories to the correct folder:
```bash
cd ./EITPose/src/data_visualizer
```
Run the Visualizer:
```bash
python DataComparator.py
```
Select "Load File" and choose the desired data file to visualize (see "Available Datasets" below).\
Hit the "Play" button or move the slider timeline to examine the data changing over time.

### Evaluation
Change Directories to the evaluation folder:
```bash
cd ./EITPose/src/analysis/evaluation
```
Run one of the evaluations. For example to evaluate the Mean Per Joint Positional Error (MPJPE) within session:
```bash
python experiment_mpjpe_within_session.py
```
Outputs will be saved to EITPose/src/analysis/evaluation/experiment_results/


## Available Datasets
- EITPose/src/data/processed_pose_data: EIT/hand pose within sessions, across sessions, across users
- EITPose/src/data/processed_longitudinal_data: EIT/hand pose within sessions across a long period of time
- EITPose/src/data/processed_gesture_data: EIT/hand gesture within sessions and across users

### Models
No models have been uploaded because they are quite large for certain experiment configurations. However, the given experiments can produce the models by setting the "save_model" parameter to True and running the experiment.

## System Requirements
This was written in python3 (3.8.16) using sci-kit learning as the main ML libraries. This was developed in a Windows environment, but should run in Mac and Linux too. The environment.yml file here can be used to initialize a conda environment:
```bash
conda env create -f environment.yml
```
\
If you are not using Anaconda, you can also use pip to install the required python libraries:
```bash
pip install -r requirements.txt
```

## Reference

Alexander Kyu, Hongyu Mao, Junyi Zhu, Mayank Goel, and Karan Ahuja. 2024. EITPose: Wearable and Practical Electrical Impedance Tomography for Continuous Hand Pose Estimation. In Proceedings of the CHI Conference on Human Factors in Computing Systems (CHI '24). Association for Computing Machinery, New York, NY, USA, Article 402, 1–10. 

[Read or Download the paper here.](https://doi.org/10.1145/3613904.3642663)


BibTex Reference:
```
@inproceedings{10.1145/3613904.3642663,
author = {Kyu, Alexander and Mao, Hongyu and Zhu, Junyi and Goel, Mayank and Ahuja, Karan},
title = {EITPose: Wearable and Practical Electrical Impedance Tomography for Continuous Hand Pose Estimation},
year = {2024},
isbn = {9798400703300},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3613904.3642663},
doi = {10.1145/3613904.3642663},
abstract = {Real-time hand pose estimation has a wide range of applications spanning gaming, robotics, and human-computer interaction. In this paper, we introduce EITPose, a wrist-worn, continuous 3D hand pose estimation approach that uses eight electrodes positioned around the forearm to model its interior impedance distribution during pose articulation. Unlike wrist-worn systems relying on cameras, EITPose has a slim profile (12 mm thick sensing strap) and is power-efficient (consuming only 0.3 W of power), making it an excellent candidate for integration into consumer electronic devices. In a user study involving 22 participants, EITPose achieves with a within-session mean per joint positional error of 11.06 mm. Its camera-free design prioritizes user privacy, yet it maintains cross-session and cross-user accuracy levels comparable to camera-based wrist-worn systems, thus making EITPose a promising technology for practical hand pose estimation.},
booktitle = {Proceedings of the CHI Conference on Human Factors in Computing Systems},
articleno = {402},
numpages = {10},
keywords = {Electrical Impedance Tomography, Extended Reality, Hand Gesture, Hand Pose, Input, Interaction Technique, Natural User Interfaces},
location = {<conf-loc>, <city>Honolulu</city>, <state>HI</state>, <country>USA</country>, </conf-loc>},
series = {CHI '24}
}
```

## Disclaimer

```
THE PROGRAM IS DISTRIBUTED IN THE HOPE THAT IT WILL BE USEFUL, BUT WITHOUT ANY WARRANTY. IT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW THE AUTHOR WILL BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
```
