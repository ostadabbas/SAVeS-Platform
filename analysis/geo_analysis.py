from evo.core import metrics
from evo.tools import file_interface
import matplotlib.pyplot as plt
from evo.tools import plot
import copy
import numpy as np
import os
import time


def geo_ts_align(gt_file,gt_ts,pred_ts):
    gt_ts_arr = np.loadtxt(gt_ts)
    pred_ts_arr = np.loadtxt(pred_ts)
    with open(gt_file, 'r') as f:
        gt_lines = f.readlines()
    # for each ts in pred, find the close one in gt
    new_gt_lines = []
    for idx, pred_ts_entry in enumerate(pred_ts_arr):
        semi_res = np.abs(gt_ts_arr-pred_ts_entry)
        to_gt_idx = np.argmin(semi_res)
        new_gt_lines.append(gt_lines[to_gt_idx])
    chk_pth = os.path.join(".","extracted","ts_align_temp")
    if not os.path.exists(chk_pth):
        os.makedirs(chk_pth)
    temp_file = "{}_gt_align.txt".format(time.strftime("%Y%m%d-%H%M%S"))
    with open(os.path.join(chk_pth,temp_file),"w") as f:
        for line in new_gt_lines:
            f.write(line)
    return os.path.join(chk_pth,temp_file)

def geo_ana(gt_file,pred_file,do_rpe,do_ape,do_align,do_plot,do_ts,gt_ts=None,pred_ts=None):
    if do_ts:
        gt_file = geo_ts_align(gt_file,gt_ts,pred_ts)
    pose_relation = metrics.PoseRelation.translation_part
    delta = 1
    delta_unit = metrics.Unit.frames
    traj_ref = file_interface.read_kitti_poses_file(gt_file)
    traj_est = file_interface.read_kitti_poses_file(pred_file)
    scene_len = traj_ref.get_infos()["path length (m)"]
    result = {"scene_length(m)":scene_len}    
    if not (do_rpe or do_ape):
        return (False,"Please select at least one metric!")
    traj_est_aligned = copy.deepcopy(traj_est)
    if do_align:
        # traj_est_aligned.align_origin(traj_ref)
        traj_est_aligned.align(traj_ref,n=10)
    data = (traj_ref, traj_est_aligned)
    if do_plot:
        fig = plt.figure()
        traj_by_label = {
            "estimate (aligned)": traj_est_aligned,
            "reference": traj_ref
        }
        plot.trajectories(fig, traj_by_label, plot.PlotMode.xyz)
        plt.show()
    try:
        if do_ape:
            ape_metric = metrics.APE(pose_relation)
            ape_metric.process_data(data)
            result['ape_mean'] = ape_metric.get_statistic(metrics.StatisticsType.mean)
            result['ape_std'] = ape_metric.get_statistic(metrics.StatisticsType.std)
        if do_rpe:
            rpe_metric = metrics.RPE(pose_relation=pose_relation, delta=delta, delta_unit=delta_unit, all_pairs=False)
            rpe_metric.process_data(data)
            result['rpe_mean'] = rpe_metric.get_statistic(metrics.StatisticsType.mean)
            result['rpe_std'] = rpe_metric.get_statistic(metrics.StatisticsType.std)
        return (True,result)
    except Exception as e:
        return (False,e)
