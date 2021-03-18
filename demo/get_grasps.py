import sys
sys.path.append('/home/zibo/6dof-graspnet')
import grasp_estimator
import numpy as np
import argparse
from utils import utils


def make_parser():
    parser = argparse.ArgumentParser(
        description='6-DoF GraspNet Demo, get grasps from my own point cloud .npy file',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--grasp_sampler_folder', type=str,
                        default='checkpoints/vae_pretrained/')
    parser.add_argument('--grasp_evaluator_folder', type=str,
                        default='checkpoints/evaluator_pretrained/')
    parser.add_argument('--refinement_method', choices={"gradient", "sampling"},
                        default='sampling')
    parser.add_argument('--refine_steps', type=int, default=25)
    parser.add_argument('--pc_path', type=str, default='demo/data/pccylinder.npy', help='point cloud .npy file path')
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.8,
        help=
        "When choose_fn is something else than all, all grasps with a score given by the evaluator notwork less "
        "than the threshold are removed"
    )
    parser.add_argument(
        '--choose_fn',
        choices={
            "all", "better_than_threshold", "better_than_threshold_in_sequence"
        },
        default='better_than_threshold',
        help=
        "If all, no grasps are removed. If better than threshold, only the last refined grasps are considered while "
        "better_than_threshold_in_sequence consideres all refined grasps "
    )

    parser.add_argument('--target_pc_size', type=int, default=1024)
    parser.add_argument('--num_grasp_samples', type=int, default=150)
    parser.add_argument(
        '--generate_dense_grasps',
        action='store_true',
        help=
        "If enabled, it will create a [num_grasp_samples x num_grasp_samples] dense grid of latent space values and "
        "generate grasps from these."
    )

    parser.add_argument(
        '--batch_size',
        type=int,
        default=15,
        help=
        "Set the batch size of the number of grasps we want to process and can fit into the GPU memory at each forward"
        " pass. The batch_size can be increased for a GPU with more memory."
    )
    parser.add_argument('--npy_save_path', type=str, default='demo/data/grasps.npy')
    parser.add_argument('--txt_save_path', type=str, default='demo/data/grasps.txt')
    opts, _ = parser.parse_known_args()
    return parser


def main():
    """
    need to specify save path: save_path_npy and save_path_txt
    :return:
    """
    args = make_parser().parse_args()
    grasp_sampler_args = utils.read_checkpoint_args(args.grasp_sampler_folder)
    grasp_sampler_args.is_train = False
    grasp_evaluator_args = utils.read_checkpoint_args(
        args.grasp_evaluator_folder)
    grasp_evaluator_args.continue_train = True
    estimator = grasp_estimator.GraspEstimator(grasp_sampler_args,
                                               grasp_evaluator_args, args)

    point_cloud = np.load(args.pc_path)
    generated_grasps, generated_scores = estimator.generate_and_refine_grasps(
        point_cloud)

    # save_path_npy = 'demo/data/grasp_pose_6dof1024cylinder_whole.npy'
    # save_path_txt = 'demo/data/grasp_pose_6dof1024cylinder_whole.txt'

    grasp_pose_score = {'grasp': np.array(generated_grasps), 'score': np.array(generated_scores)}
    np.save(args.npy_save_path, grasp_pose_score)
    print('successfully saved %s', args.npy_save_path)
    with open(args.txt_save_path, 'w') as w:
        for pose, score in zip(generated_grasps, generated_scores):
            w.write(str(pose))
            w.write('   ')
            w.write(str(score) + '\n')
            w.flush()
    print('successfully saved %s', save_path_txt)


if __name__ == '__main__':
    main()
