## Script to generate test data

- from PKL to Geopandas, saved as PARQUET
- from CSVs to ZARR (Anndata)
- together as ZARR
- pseudo channel one = "DAPI":
  - voxelize all points to 3 x 3 x 3
  - gaussian blur with sigma = 1
  - resample to 0.8 x 0.8 x 2.5
  - gaussian blur with sigma = 2
  - add noise
- pseudo channel two and 3 = "mk1" and "mk2":
  - voxelize all channels to 3 x 3 x 3 (if not too big) or 5 x 5 x 5
  - run NMF with a few components
  - select relevant conponents:
    - mk1 would be regional
    - mk2 would be cell specific
  - Then process so that we have 0.8 x 0.8 x 2.5 images
- save all channels as a TIFF

In the end we have:
- a table (MERFISH)
- cell segmentations (planes)
- 3 channels of "pseudo-Lightsheet" data

## Script to convert to one spatialdata ZARR file
Use the spatialdata API to create the layers

## Create a labels layer with cell IDs
- If possible, use plane wise function of spatialdata
- Save to ZARR

## Create Meshes for cell segmentations
- Save as VTK (dynamically)

## Perform visualization

Use napari to visualize the data:
- Load the ZARR file
- Load VTK file
- Display:
  - Point layer
  - 3 Image layers
  - Labels layer
  - Mesh layer
- Note: always use "scale" so that we always see the real units
- Color points using the var counts

## Crop image ?

- In napari, display cropped data with real coordinates

## Manual annotation of big regions and post-processing

- two ways to annotate:
  - using the labels layer
    - Create a new labels layer (downsampled to 2.5 x 5 x 5)
    - Label few planes, based on regional markers
  - using the shapes layer
    - Create a new shapes layer
    - Draw polygons around regions
    - (optional) raterize, with spatialdata API
- Interpolation:
  1. 2.5D labels -> 3D labels -> 3D mesh
    - Interpolate labels layer (with Lorenzo's function)
    - Save to ZARR
    - Create mesh (with VEDO?)
    - Save to VTK
  2. 2.5D polygons -> 3D mesh -> 3D labels
    - Interpolate polygons (with VEDO)
    - Save to VTK
    - Rasterize (with VEDO?)
    - Save to ZARR
  3. 2.5D polygons -> 3D mesh -> 3D polygons -> 3D labels
    - Same two steps as above:
      - Interpolate  polygons (with VEDO)
      - Save to VTK
    - Cut for each plane (with VEDO) to obtain polygons
    - Save to ZARR
    - Rasterize (with spatialdata API)
    - Save to ZARR

## Napari widget to handle visualization

## Napari widget to handle annotation

## Slicing

- Display a plane
- Rotate the view
- Cut the shapes to obtain polygons

## Napari widget for slicing / projection
