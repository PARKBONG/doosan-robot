import os 
import datetime
from typing import Any, List, Optional

import open3d as o3d
import numpy as np

from Config import Config

class DataCollector:
    def __init__(self, cfg: Config):
        """
        Initializes the DataCollector with the given configuration.
        
        Args:
            cfg: Configuration object containing settings for data collection.
        """
        self.cfg: Config = cfg

        self._create_dir()

    def _create_dir(self) -> None:
        """
        Creates a directory for saving results if it does not already exist.
        The directory is structured as ./result/YYMMDD/HHMMSS/.
        """
        self.current_dir: str = os.path.dirname(os.path.abspath(__file__))
        now: datetime.datetime = datetime.datetime.now()
        date_str: str = now.strftime("%y%m%d")
        time_str: str = now.strftime("%H%M%S")
        self.save_dir: str = os.path.join(self.current_dir, "result", date_str, time_str)
        os.makedirs(self.save_dir, exist_ok=True)

    def save(self, data: List[np.ndarray]) -> str:
        """
        Saves the collected data to an auto-generated file path:
        ./result/YYMMDD/HHMMSS/fileindex.npy
        """

        if not len(data):
            print("point cloud data is EMPTY!")
            
        existing: List[str] = [f for f in os.listdir(self.save_dir) if f.endswith('.npy')]
        file_index: int = len(existing)
        file_path: str = os.path.join(self.save_dir, f"{file_index}.npy")
        np.save(file_path, np.array(data, dtype=object), allow_pickle=True)
        print(f"Saved list of arrays to '{file_path}'")
        return file_path
    
    # def visualize_latest_pcd(self):
    #     latest_path = self._search_latest()
    #     if latest_path is None:
    #         print("No saved point cloud file found.")
    #         return
    #     pcd_list = np.load(latest_path, allow_pickle=True)
    #     if len(pcd_list) == 0:
    #         print("No point cloud data to visualize.")
    #         return
    #     all_points = np.concatenate(pcd_list, axis=0)
    #     if all_points.size == 0:
    #         print("All point arrays are empty.")
    #         return
    #     pcd = o3d.geometry.PointCloud()
    #     pcd.points = o3d.utility.Vector3dVector(all_points)
    #     o3d.visualization.draw_geometries([pcd], window_name=f"Visualized from {latest_path}")

    # def _search_latest(self) -> Optional[str]:
    #     """
    #     Search for the latest saved npy file in result/YYMMDD/HHMMSS/fileindex.npy structure.
    #     Returns the full file path, or None if not found.
    #     """
    #     result_dir = os.path.join(self.current_dir, "result")
    #     if not os.path.exists(result_dir):
    #         return None
    #     # Find latest date
    #     date_dirs = sorted([d for d in os.listdir(result_dir) if os.path.isdir(os.path.join(result_dir, d))], reverse=True)
    #     for date_dir in date_dirs:
    #         date_path = os.path.join(result_dir, date_dir)
    #         # Find latest time
    #         time_dirs = sorted([d for d in os.listdir(date_path) if os.path.isdir(os.path.join(date_path, d))], reverse=True)
    #         for time_dir in time_dirs:
    #             time_path = os.path.join(date_path, time_dir)
    #             # Find latest file index
    #             npy_files = sorted([f for f in os.listdir(time_path) if f.endswith('.npy')], key=lambda x: int(x.split('.')[0]), reverse=True)
    #             if npy_files:
    #                 return os.path.join(time_path, npy_files[0])
    #     print("No directories exist at /result")
    #     return None
    