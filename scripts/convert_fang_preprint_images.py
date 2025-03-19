from pathlib import Path
import spatialdata as sd
from spatialdata.models import Image3DModel
import argparse
import numpy as np
from tqdm import tqdm
from sklearn.decomposition import NMF
import matplotlib.pyplot as plt
from skimage import filters

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=str, default="mouse_cortex_100um")
    return parser.parse_args()


# Open existing dataset
dataset = parse_args().dataset

data_dir = "/data/etienne.doumazane/st/Fang_preprint/"
data_dir = Path(data_dir)
path = data_dir / f"{dataset}_expression_boundaries.zarr"

sdata = sd.read_zarr(path)
sdata
# Compute dimensions of the image
# Compute the translation to apply to the coordinates
translate_x, translate_y = np.floor(sdata["expression"].obs[["min_x", "min_y"]].min()).astype(int)
translate_x, translate_y
# Compute the shape of the image
shape_x, shape_y = np.ceil((sdata["expression"].obs[["max_x", "max_y"]] - np.array([translate_x, translate_y])).max()).astype(int)
shape_x, shape_y
# z dimension
translate_z = int(np.floor(sdata["expression"].obs["center_z"].min()).astype(int))
shape_z = int(np.ceil((sdata["expression"].obs["center_z"] - translate_z).max()).astype(int))
translate_z, shape_z
# expected size if isometric 1 um voxels
shape_x * shape_y * shape_z * 2 / 1e6
sdata["expression"].obs["x"].min()
sdata["expression"].obs["min_x"].min()

sdata["expression"].obs
# Compute the voxel coordinates
sdata["expression"].obs["voxel_x"] = ((sdata["expression"].obs["center_x"] - translate_x) / 1.63).astype(int)
sdata["expression"].obs["voxel_y"] = ((sdata["expression"].obs["center_y"] - translate_y) / 1.63).astype(int)
sdata["expression"].obs["voxel_z"] = ((sdata["expression"].obs["center_z"] - translate_z) / 2.5).astype(int)
# Create a "tissue" image
# Bin the data
voxels = sdata["expression"].obs.groupby(["voxel_x", "voxel_y", "voxel_z"]).size()
voxels.value_counts()
voxels_df = voxels.to_frame().reset_index().rename(columns={0: "count"})
voxels_df
coords = voxels_df[["voxel_z", "voxel_y", "voxel_x"]].values.T
print(coords.shape)
coords = tuple(coords)
# compute the shape of the image
shape = (int(np.ceil(shape_z / 2.5))), int(np.ceil(shape_y / 1.63)), int(np.ceil(shape_x / 1.63))
shape
# Create the image
arr = np.zeros(shape, dtype=np.uint16)
arr[coords] = voxels_df["count"].values
gaussian = filters.gaussian(arr, sigma=(1,5,5))
# plt.hist(gaussian.ravel(), bins=100);
# plt.imshow(gaussian[12])
# plt.imshow(np.clip(gaussian[12, 750:1000, 750:1000]*1e9, 2, 8))

# Save to adata store
sdata["tissue"] = Image3DModel.parse(np.expand_dims(gaussian * 1e9, axis=0), dims="czyx")
## Compute a "markers" image = 10 channels
# -> simulate multiplexed immunolabeling data
facto = NMF(n_components=10).fit_transform(sdata["expression"].X[:,:-10])
coords_obs = tuple(sdata["expression"].obs[['voxel_z', 'voxel_y', 'voxel_x']].values.T)
gaussians = []
for k in tqdm(range(10)):
    arr = np.zeros(shape, dtype=np.float32)
    arr.flat = facto[:, k]
    gaussian = filters.gaussian(arr, sigma=(1,5,5))
    gaussians.append(gaussian)
sdata[f"markers"] = Image3DModel.parse(np.stack(gaussians), dims="czyx")
sdata
# Save the resulting dataset
sdata.write(data_dir / "derived" / f"{dataset}_expression_boundaries_images.zarr")
