from pyrosm import OSM
import geopandas as gpd

# --- Configuration ---
PBF_PATH = "lebanon-251104.osm.pbf"
STREETS_OUT = "beirut_streets.geojson"
POIS_OUT = "beirut_pois.geojson"

print("⏳ Loading OSM map data for Lebanon...")
osm = OSM(PBF_PATH)

print("📍 Locating Beirut boundary...")
beirut_area = osm.get_boundaries(name="محافظة بيروت")

if beirut_area is None or beirut_area.empty:
    raise ValueError("❌ Could not find 'Beirut' in the OSM dataset.")

print("✅ Found Beirut boundary")

# 1️⃣ Streets
print("🚗 Extracting street (road) network...")
streets = osm.get_network(
    network_type="driving",
    bbox=beirut_area.total_bounds
)
streets = streets[["name", "highway", "geometry"]].dropna(subset=["name"])
streets.to_file(STREETS_OUT, driver="GeoJSON")
print(f"💾 Saved {len(streets)} streets → {STREETS_OUT}")

# 2️⃣ POIs
print("🏢 Extracting Points of Interest (POIs)...")
custom_filter = {
    "amenity": ["hotel", "hospital", "pharmacy", "police", "fire_station"],
    "shop": ["supermarket", "mall", "convenience", "department_store"],
    "tourism": ["hotel", "museum"],
}
pois = osm.get_pois(custom_filter=custom_filter, bounding_box=beirut_area.total_bounds)
pois = pois[["name", "amenity", "shop", "tourism", "geometry"]].dropna(subset=["geometry"])
pois.to_file(POIS_OUT, driver="GeoJSON")
print(f"💾 Saved {len(pois)} POIs → {POIS_OUT}")

print("🎉 Extraction complete.")
