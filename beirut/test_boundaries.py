from pyrosm import OSM

osm = OSM("lebanon-251104.osm.pbf")
boundaries = osm.get_boundaries()
print(boundaries[["name", "admin_level"]].head(20))
