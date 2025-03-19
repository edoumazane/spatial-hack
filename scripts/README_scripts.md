

[Preprint](https://raw.githubusercontent.com/elifesciences/enhanced-preprints-data/master/data/90029/v1/90029-v1.pdf)

[Analysis software](https://github.com/r3fang/MERlin)

[MERFISH data generated in this study is available](https://www.dropbox.com/sh/noc3alfrv09c2xr/AADPJ6NJKArbJOm-oEz5jHdFa?dl=0/)


This data collection contains single-cell transcriptomics datasets acquired using 3D MERFISH in a **100um-thick mouse cortex** section and a **200um-thick mouse hypothalamus** section collected by the Xiaowei Zhuang Lab at Harvard University and Howard Hughes Medical Institute.


The dataset contains a total of two MERFISH experiments, which include **1) 250-gene measurement in a 100-um thick section of the mouse cortex (mouse_cortex_100um); 2) a 155-gene measurement in a 200um thick section of mouse hypothalamus (mouse_hypothalamus_200um).**


Each folder contains the following folder/files:
ExportBarcodes/barcodes.csv: Decoded RNA spot location (global_x,global_y,global_z) in the unit of microns and their gene identity.
ExportBarcodes/feature_boundaries.pkl: a pickle file contains the boundaries of each segmented cell represented as polygon stored in a shapely file format.
ExportCellMetadata3D/feature_metadata.csv: Segmented cell coordinates and cells’ meta data.
ExportPartitionedBarcodes/barcodes_per_feature.csv: Cell-by-gene matrix.
seurat_obj.rds: a seurat object that contains cell-by-gene matrix, cell metadata and cluster identifies for each cell. 




```bash 
mkdir -p /data/etienne.doumazane/st/Fang_preprint/mouse_hypothalamus_200um && cd $_ 
mv ~/Downloads/mouse_hypothalamus_200um.zip .
unzip mouse_hypothalamus_200um.zip
rm mouse_hypothalamus_200um.zip

mkdir -p /data/etienne.doumazane/st/Fang_preprint/mouse_cortex_100um && cd $_ 
mv ~/Downloads/mouse_cortex_100um.zip .
unzip mouse_cortex_100um.zip 
rm mouse_cortex_100um.zip

cd ..
tree
du -sh .
```
```bash
.
├── [4.0K]  mouse_cortex_100um
│   ├── [3.2K]  analysis.R
│   ├── [  41]  ExportBarcodes
│   │   ├── [4.5G]  barcodes.csv
│   │   └── [ 88M]  tmp.csv
│   ├── [  36]  ExportCellBoundaries
│   │   └── [5.5G]  feature_boundaries.pkl
│   ├── [  34]  ExportCellMetadata3D
│   │   └── [ 14M]  feature_metadata.csv
│   ├── [  38]  ExportPartitionedBarcodes
│   │   └── [ 77M]  barcodes_per_feature.csv
│   ├── [ 63M]  seurat.rds
│   └── [ 19M]  seurat.v2.rds
└── [ 159]  mouse_hypothalamus_200um
    ├── [  34]  ExportBarcodes
    │   └── [6.1G]  barcodes.csv
    ├── [  44]  ExportCellBoundaries
    │   └── [ 11G]  feature_boundaries.pkl
    ├── [  42]  ExportCellMetadata3D
    │   └── [ 27M]  feature_metadata.csv
    ├── [  46]  ExportPartitionedBarcodes
    │   └── [131M]  barcodes_per_feature.csv
    └── [118M]  seurat.rds


11G	mouse_cortex_100um
18G	mouse_hypothalamus_200um
```


- install data-fetcher-r
cd ~/code/renier/fico-project/data-fetcher/Fang_preprint
conda env create -f environment_r.yaml
conda activate data-fetcher-r

- install fico-utils
cd ~/code/renier/fico-project/fico-utils
conda activate data-fetcher-r
pip install -e .

- install r-packages
screen -d -RR install_r_packages
cd ~/code/renier/fico-project/data-fetcher/Fang_preprint
conda activate data-fetcher-r
python ~/code/renier/fico-project/data-fetcher/Fang_preprint/install_rpackages.py --packages_list ~/code/renier/fico-project/data-fetcher/Fang_preprint/rpackages.txt > install_rpackages.log 2>&1



- install fang-preprint
cd ~/code/renier/fico-project/data-fetcher/Fang_preprint
conda env create -f environment.yaml
conda activate fang-preprint

- install fico-utils
cd ~/code/renier/fico-project/fico-utils
conda activate fang-preprint
pip install -e .


