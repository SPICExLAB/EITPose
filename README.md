# EITPose
This is a research repository for [EITPose: Wearable and Practical Electrical Impedance Tomography for Continuous Hand Pose Estimation]() (CHI 2024). It contains the following:

- EITPose Firmware file (tested with Teensyduino2.0)
- EITPose Hardware file
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


![](https://github.com/NU-SPICE-LAB/EITPose/blob/main/media/media1.gif?raw=true)
![](https://github.com/NU-SPICE-LAB/EITPose/blob/main/media/media2.gif?raw=true)

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
## Disclaimer

```
THE PROGRAM IS DISTRIBUTED IN THE HOPE THAT IT WILL BE USEFUL, BUT WITHOUT ANY WARRANTY. IT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW THE AUTHOR WILL BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
```
