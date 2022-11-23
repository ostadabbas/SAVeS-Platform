from evo.core import metrics
from evo.tools import file_interface
import matplotlib.pyplot as plt
from evo.tools import plot

def geo_ana(gt_file,pred_file,do_rpe,do_ape,do_align,do_plot):
    traj_ref = file_interface.read_kitti_poses_file(gt_file)
    traj_est = file_interface.read_kitti_poses_file(pred_file)
    scene_len = traj_ref.get_infos()["path length (m)"]
    result = {"scene_length(m)":scene_len}    
    if not (do_rpe or do_ape):
        print("Please select at least one metric!")
        return False
    traj_est_aligned = copy.deepcopy(traj_est)
    if do_align:
        traj_est_aligned.align_origin(traj_ref)
    data = (traj_ref, traj_est_aligned)
    if do_plot:
        fig = plt.figure()
        traj_by_label = {
            "estimate (aligned)": traj_est_aligned,
            "reference": traj_ref
        }
        plot.trajectories(fig, traj_by_label, plot.PlotMode.xyz)
        plt.show()

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
    return result
