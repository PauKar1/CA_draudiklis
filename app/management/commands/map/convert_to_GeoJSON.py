import geopandas as gpd

gpk_file_path = 'C:/Users/pauli/PycharmProjects/AAA_draudiklis/app/management/commands/map/natural_earth_vector.gpkg'
gdf = gpd.read_file(gpk_file_path, layer='ne_110m_admin_0_countries')

geojson_file_path = 'C:/Users/pauli/PycharmProjects/AAA_draudiklis/app/management/commands/map/countries.geojson'
gdf.to_file(geojson_file_path, driver='GeoJSON')

print(f'GeoJSON file saved to {geojson_file_path}')
