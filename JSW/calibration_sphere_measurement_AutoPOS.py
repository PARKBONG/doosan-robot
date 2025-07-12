
import rospy
import os
import threading, time
import sys
import math
import pandas as pd
import numpy as np

sys.dont_write_bytecode = True
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__),"../common/imp")) ) # get import path : DSR_ROBOT.py 

# for single robot 
ROBOT_ID     = "dsr01"
ROBOT_MODEL  = "m1509"
import DR_init
DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL
from DSR_ROBOT import *

Calibration_sphere_pos = [500, 26, 75]
Gocator_height = 74.5

# Gocator Clearance Distance: 95~125
# 구 기준 30도씩 측정

def pose_calculation():
    pose_calculated = []
    for i in range(7):
        Gocator_distance_range = 105 + 5*i

        for i in range(5):
            degrees = 30*i

            if degrees == 0:
                pose_new = [Calibration_sphere_pos[0], Calibration_sphere_pos[1], 
                           Calibration_sphere_pos[2] + Gocator_distance_range + Gocator_height, 
                           180, 
                           -180, 
                           180]
                pose_calculated.append(pose_new)
            else:
                for circle in range(12):
                    radius = (Gocator_distance_range + Gocator_height)*np.sin(np.radians(degrees))
                    x = Calibration_sphere_pos[0]-radius*np.cos(np.radians(circle*30))
                    y = Calibration_sphere_pos[1]+radius*np.sin(np.radians(circle*30))
                    z = Calibration_sphere_pos[2] + Gocator_distance_range*np.cos(np.radians(degrees)) + Gocator_height

                    vx = Calibration_sphere_pos[0] - x
                    vy = Calibration_sphere_pos[1] - y
                    vz = Calibration_sphere_pos[2] - z

                    psi = np.arctan2(vy, vx) + 0.1
                    theta = np.arccos(vz/np.sqrt(vx**2 + vy**2 + vz**2))
                    phi = psi
                    pose_new = [x, y, z, np.degrees(psi), np.degrees(theta), np.degrees(phi)]    
                    pose_calculated.append(pose_new)
                
    # print(pos_calculated)
    return pose_calculated

if __name__ == "__main__":
    pose_calculated = pose_calculation()
    Measurement = 0
    Record_Robot_joint = []


    while True:
        user_input = input("PRESS ENTER FOR NEXT MOTION, 종료 시 'done' 입력")

        if user_input.lower() == "done":
            break

        print("Robot Motion ")
        print("Pose Calculated", pose_calculated[Measurement])
        movel(pose_calculated[Measurement], vel=50, acc=100)
        Measurement += 1

        # Solution_space = get_current_solution_space()
        Robot_joint = get_current_posj()
        print("Robot Joint Values: ", Robot_joint)
        Record_Robot_joint.append(Robot_joint)

    df = pd.DataFrame(Record_Robot_joint)
    save_dir = "/home/sms/Virtual_Commisioning"
    save_path = os.path.join(save_dir, "Robot_Jointvalues.xlsx")
    df.to_excel(save_path, index = False)
    


# -2.702666759490967, 56.17147445678711, 98.23128509521484, 0.32633545994758606, -154.40231323242188, 3.1199002265930176]
