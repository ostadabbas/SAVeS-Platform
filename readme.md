# SAVeS: Scoping Autnonomous Vehicle Simulation Platform
This is a evaluation platform designed to help researchers to easily test and compare various datasets generated from simulation and their real-world counterparts on the selected algorithms.
Currently, our platform supports the following geometric SLAM based algorithms and learning-based models via scripts and step-to-step guides:

|Geometric-based Algorithms|Learning-based Models|
|--------------------------|---------------------|
|A-LOAM [⇱](https://github.com/HKUST-Aerial-Robotics/A-LOAM)                    |GeoNet [⇱](https://github.com/yzcjtr/GeoNet)               |
|LeGO-LOAM [⇱](https://github.com/RobustFieldAutonomyLab/LeGO-LOAM)                |AdaBins [⇱](https://github.com/shariqfarooq123/AdaBins)             |
|ORBSLAM3 [⇱](https://github.com/UZ-SLAMLab/ORB_SLAM3)                 |DPT [⇱](https://github.com/isl-org/DPT)                 |

We provide scripts to process following datasets, with more supports coming along the way:

|Real-world Datasets       |Synthetic Datasets   |
|--------------------------|---------------------|
|nuScenes [⇱](https://www.nuscenes.org/)                  |GTA V - PreSIL [⇱](https://uwaterloo.ca/waterloo-intelligent-systems-engineering-lab/projects/precise-synthetic-image-and-lidar-presil-dataset-autonomous)     |
|KITTI [⇱](https://www.cvlibs.net/datasets/kitti/eval_odometry.php)                    |CARLA [⇱](https://carla.org/)               |

We are also providing guides on evaluating the results. For depth task, the proposed evaluation metrics are as follows. Note that $y_i$ represents pixel’s depth in ground truth, while $y_i^\*$ represents corresponding predicted depth; $y_i>0,y_i^\*>0, d_i=\log y_i-\log y_i^\*$.
* Scale Invariant logarithmic error:\
$$D(y,y^\*)=\frac{1}{n}\sum_{i}d_i^2-\frac{1}{n^2}(\sum_{i}d_i)^2$$
where\
$$d_i=\log y_i-\log y_i^\*$$
* Relative squared error:\
$$D(y,y^\* )=\sqrt{\dfrac{1}{n}\sum_{i}(\dfrac{y_i-y_i^\*}{y_i})^2}$$
* Relative absolute error:\
$$D(y,y^\* )=\dfrac{1}{n}\sum_{i}\dfrac{|y_i-y_i^\*|}{y_i}$$
* Root mean squared error of the inverse depth:\
$$D(y,y^\* )=\sqrt{\dfrac{1}{n}\sum_{i}(\dfrac{1}{y_i}-\dfrac{1}{y_i^\*})^2}$$

For odometry task, we use three metrices: APE(m), APE(%) and RPE(m).
* Absolute Pose Error (m): At any timestamp i, absolute relative pose
    $$E_i=P_{est,i} \ominus P_{ref,i}=P_{ref,i}^{-1}P_{est,i}$$
where $P_{ref,i}$ and $P_{est,i}$ are poses, and $\ominus$ is invert positional operator to calculate relative pose.
Hence, we calculate $APE_i$ by applying L2-norm to the translation part of $E_i$, and the output result is the mean of all participating frames:
$$APE=\dfrac{1}{n}\sum_i{\|trans(E_i)\|}$$
* Absolute Pose Error (\%): this indicator measures the ratio of the APE to the length of the trajectory. Since we only aligned the origin of the trajectory, the longer the vehicle travels without loop closure, the higher the drift accumulates. The percentage eliminates the difference of traveling distance.
* Relative Pose Error (m): RPE reflects local consistency of the trajectory, which compares the pose transition between 2 consecutive frames between estimation and reference:\
$$E_{i,j}=\delta_{est_{i,j}}\ominus\delta_{ref_{i,j}}=(P_{ref,i}^{-1} P_{ref,j})^{-1}(P_{est,i}^{-1}P_{est,j})$$
Similarly, out output is
$$RPE=\dfrac{1}{n-1}\sum_{i,j=i+1}{\|trans(E_{i,j})\|}$$
$\|trans(\bullet)\|$
stands for Euclidean Distance.

Here are some demo images that our platform can achieve:
![linked](https://github.com/ostadabbas/SAVeS-Platform/blob/master/Demo%20Images/linked.png)
<!-- This paltform is under development.  -->

How to use the geometric generation and analysis tool (Ubuntu 18.04):
1. Setup ROS Melodic according to the instruction[⇱](http://wiki.ros.org/melodic/Installation/Ubuntu)
2. Setup A-LOAM according to instruction[⇱](https://github.com/HKUST-Aerial-Robotics/A-LOAM)
3. Download LeGO-LOAM[⇱](https://github.com/RobustFieldAutonomyLab/LeGO-LOAM)
4. Modify src/LeGO-LOAM/include/utility.h for your desired lidar and loop closure configuration. For CARLA and KITTI dataset, use Ouster-64 configuration. Set ```useCloudRing``` to ```false``` and uncomment line 159 in imageProjection.cpp.
5. Replace mapOptmization.cpp with the one provided from the link (link currently under construction) and use installation instruction on their website to install.
6. Download pre-made ROS bag files or use your own bag (link currently under construction)
7. In your desired location, run the following command:
```bash
git clone https://github.com/ostadabbas/SAVeS-Platform/
cd SAVeS-Platform
pip install -r requirements.txt
```
8. Use
```bash
python3 geometric_ui.py
```
for trajectory generation, and 
```bash
python3 geo_analysis_ui.py
```
for result analysis.
