import numpy as np
import argparse
import logging
from VERSUS.sphericalvoids import SphericalVoids

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def parse_args():
    parser = argparse.ArgumentParser(description="Run spherical void-finding on simulated or survey data")
    parser.add_argument('--data', help="Array or path to data positions")
    parser.add_argument('--random', help="Array or path to random positions")
    parser.add_argument('--data_weights', help="Array of weights for data positions")
    parser.add_argument('--random_weights', help="Array of weights for random positions")
    parser.add_argument('--columns', help="Data column headers to read positions (XYZ/rdz)")
    parser.add_argument('--mesh', default=None, 
                        help="Array or path to density mesh. If not None and data also provided, save to path provided (True for default path).")
    parser.add_argument('--cells_per_r_sep', type=float, default=2., 
                        help="Number of mesh cells per average galaxy separation. Used to set cellsize.")
    parser.add_argument('--reconstruct', required=False, type=str, default=None, 
                        help="Type of reconstruction ('disp', 'rsd' or 'disp+rsd'), growth rate and bias. Defaults to no reconstruction.")
    parser.add_argument('--recon_args', required=False, nargs='+', default=[0.8, 2.], 
                        help="Reconstruction arguments - 'f','bias','los','smoothing_radius','recon_pad','engine'.")
    parser.add_argument('--mesh_args', required=False, nargs='+', help="Provide cellsize, boxsize, boxcenter and box-like.")
    parser.add_argument('--radii', type=float, default=[0.], nargs='+', help="List of void radii to search for")
    parser.add_argument('--void_delta', type=float, default=-0.8, help="Maximum overdensity to be classified as void")
    parser.add_argument('--void_overlap', type=float, default=0., help="Volume fraction of allowed void overlap")
    parser.add_argument('--save_fn', type=str, default=None, help="Path to save output (void positions & radii). Defaults to 'output/'.")
    parser.add_argument('--threads', type=int, default=0, 
                        help="Number of threads used for multi-threaded processes. Defaults to maximum available.")

    args = parser.parse_args()
    if args.data is None and args.mesh is None:
        parser.error("Either --data or --mesh must be provided.")

    if args.mesh_args is not None: args.mesh_args = dict(zip(['cellsize','boxsize','boxcenter','box_like'], args.mesh_args))
    if args.reconstruct is not None: 
        recon_keys = ['f','bias','los','smoothing_radius','recon_pad','engine'][:len(args.recon_args)]
        args.recon_args = dict(zip(recon_keys, args.recon_args))

    return args

def main():
    args = parse_args()

    VF = SphericalVoids(data_positions=args.data, data_weights=args.data_weights,                                                                                           random_positions=args.random, random_weights=args.random_weights, data_cols=args.columns,
                        delta_mesh=args.mesh, mesh_args=args.mesh_args, save_mesh=True if args.mesh == 'True' else args.mesh,
                        cells_per_r_sep=args.cells_per_r_sep, reconstruct=args.reconstruct, recon_args=args.recon_args)

    # VF.run_voidfinding(np.array(args.radii, dtype=np.float32), void_delta=args.void_delta, void_overlap=args.void_overlap, threads=args.threads)
    VF.run_voidfinding(args.radii, void_delta=args.void_delta, void_overlap=args.void_overlap, threads=args.threads)

    if args.save_fn is None:
        from pathlib import Path
        path = "output/"
        Path("output").mkdir(parents=True, exist_ok=True)
    else:
        path = args.save_fn + '_'
    logger.info(f"Saving output to {path}*")
    np.save(path + "void_positions.npy", VF.void_position)
    np.save(path + "void_radii.npy", VF.void_radius)
    np.save(path + "void_vsf.npy", VF.void_vsf)


if __name__ == "__main__":
    main()
