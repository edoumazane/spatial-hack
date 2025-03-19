import pandas as pd
import napari
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Input file')
    parser.add_argument('n_planes', type=int, help='Number of polygons to display', default=100)
    return parser.parse_args()

def get_geometry_properties(df, z_column='center_z'):
    polygons = []
    indices = []
    for i in range(0, len(df)):
        polygons_item = list(df.geometry.iloc[i].exterior.simplify(tolerance=2).coords)
        if z_column:
            z = df[z_column].iloc[i]
            polygons.append([tuple(x) + (z,) for x in polygons_item])
        else:
            polygons.append([tuple(x) for x in polygons_item])
        indices.append(df.iloc[i].name)
    return polygons, indices

def main():
    args = parse_args()
    df = pd.read_pickle(args.input)
    v = napari.Viewer()
    polygons, indices = get_geometry_properties(df.head(args.n_planes))
    v.add_shapes(polygons, shape_type='polygon', edge_color='green', face_color='blue', opacity=0.5)
    napari.run()

if __name__ == '__main__':
    main()
