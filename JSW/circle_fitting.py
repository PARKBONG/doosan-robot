from Config import Config
from Robot_Interface import RobotInterface
from Gocator_Interface import GocatorInterface
from Data_Collector import DataCollector
from Data_Visualizer import DataVisualizer
from Robot_Planner import RobotPlanner

###############################################################################
# Before running this script, ensure that the following ROS nodes are running:
# 1. $ robot
# 2. roslaunch gocator_profile read_depth.launch
###############################################################################

cfg = Config()

robot = RobotInterface(cfg)
go = GocatorInterface(cfg)
dc = DataCollector(cfg)
planner = RobotPlanner(cfg)

# robot.move_home_pose()
# input("Press Enter to continue after the robot is in the home position...")

go.start() # enable the gocator ros topic publisher
print("waiting for the pcd collection... ")
planner.sleep(5.0)
# pcd, robot = go.get_current_data() # pcd: (N,3) numpy array, robot: EE SE3 pose 
pcd_list = go.stop() # list

### above is my code -- see main.py for more details
### below are your circle fitting methods

# ===========================================================================
# from Circle_Estimator import CircleEstimator
# circle = CircleEstimator(pcd)  # pcd: (N,3) numpy array
# result_df = circle.fit_and_report(do_plot=True)  # do_plot=True면 자동 시각화
# print(result_df)

import matplotlib.pyplot as plt
import numpy as np

# write a code that fits a circle to the point cloud data
z_max_list = np.array([np.max(pcd[:,2]) for pcd in pcd_list])


# draw plot that x has index and y has z-coordinates
plt.plot(z_max_list, marker='o', linestyle='None')
plt.title('Z-coordinates of Point Cloud Data')
plt.xlabel('Index')
plt.ylabel('Z-coordinate')
plt.grid()
plt.show()  
# set title as z mean and std
plt.title(f'Z-coordinates of Point Cloud Data (Mean: {np.mean(z_max_list):.6f}, Std: {np.std(z_max_list):.6f})')