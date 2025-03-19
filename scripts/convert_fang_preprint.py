from pathlib import Path
import pandas as pd
import anndata as ad
import geopandas as gpd
import spatialdata as sd
from spatialdata import SpatialData
from spatialdata.models import ShapesModel, TableModel
import argparse
from fico_utils import utils

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=str, default="mouse_cortex_100um")
    return parser.parse_args()

# Open Expression data
data_dir = "/data/etienne.doumazane/st/Fang_preprint/"
data_dir = Path(data_dir)

output_dir = data_dir / "derived"
output_dir.mkdir(exist_ok=True)

args = parse_args()
dataset = args.dataset
utils.timestamp_info(f"Converting dataset {dataset}")

path = data_dir / f"{dataset}/ExportPartitionedBarcodes/barcodes_per_feature.csv"
expression = pd.read_csv(path, index_col=0)

path = data_dir / f"{dataset}/ExportCellMetadata3D/feature_metadata.csv"
obs_features = pd.read_csv(path, index_col=0)


# Create and save object as ZARR
adata = ad.AnnData(expression)
utils.timestamp_info(adata)
utils.timestamp_info(adata.obs)
assert adata.obs.index.equals(obs_features.index)
adata.obs = obs_features
utils.timestamp_info(adata)
sdata = SpatialData.init_from_elements({
    "expression": TableModel.parse(adata),
    })
path = output_dir / f"{dataset}_expression.zarr"
sdata.write(path)
path = output_dir / f"{dataset}_expression.zarr"
sdata = sd.read_zarr(path)
utils.timestamp_info(sdata)

# Open Cell Boundaries
path = data_dir / f"{dataset}/ExportCellBoundaries/feature_boundaries.pkl"
cell_boundaries = pd.read_pickle(path)
cell_boundaries.reset_index(inplace=True, drop=True)
assert isinstance(cell_boundaries, gpd.GeoDataFrame)
utils.timestamp_info(cell_boundaries)

# Save Cell Boundaries as parquet
path = output_dir / f"{dataset}_cell_boundaries.parquet"
cell_boundaries.to_parquet(path)
path = output_dir / f"{dataset}_cell_boundaries.parquet"
cell_boundaries = gpd.read_parquet(path)
assert isinstance(cell_boundaries, gpd.GeoDataFrame)
utils.timestamp_info(cell_boundaries)

# Save Cell Boundaries and Expression data together in ZARR format
sdata = SpatialData.init_from_elements({
    "cell_boundaries": ShapesModel.parse(cell_boundaries),
    "expression": TableModel.parse(adata),
    })
path = output_dir / f"{dataset}_expression_boundaries.zarr"
sdata.write(path)
path = output_dir / f"{dataset}_expression_boundaries.zarr"
sdata = sd.read_zarr(path)
utils.timestamp_info(sdata)
