let map;
let routeLayer;
const colors = { incident: '#ff7180', hospital: '#65dda0', shelter: '#b693ff' };

// City coordinates mapping
const CITY_COORDINATES = {
    chennai: [13.0827, 80.2707],
    mumbai: [19.0760, 72.8777],
    kochi: [9.9312, 76.2673],
    delhi: [28.6139, 77.2090],
    bangalore: [12.9716, 77.5946]
};

export function getCoordinatesForLocation(locationName) {
    if (!locationName) return CITY_COORDINATES.chennai;
    const key = String(locationName).trim().toLowerCase();
    for (const [city, coords] of Object.entries(CITY_COORDINATES)) {
        if (key.includes(city)) return coords;
    }
    return CITY_COORDINATES.chennai; // Default fallback
}

export function initializeMap(coordinates = [13.0827, 80.2707]) {
    if (!window.L) return;
    if (map) map.remove();

    map = L.map('map', { zoomControl: false, attributionControl: true }).setView(coordinates, 12);
    L.control.zoom({ position: 'bottomright' }).addTo(map);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

export function setMapLocation(locationName) {
    const coords = getCoordinatesForLocation(locationName);
    if (map) {
        map.setView(coords, 12);
    } else {
        initializeMap(coords);
    }
}

export function addMarkers(markers = []) {
    if (!map) return;
    markers.forEach(marker => L.circleMarker(marker.coordinates, {
        radius: 8,
        color: colors[marker.type] || '#50dfda',
        fillColor: colors[marker.type] || '#50dfda',
        fillOpacity: 0.85,
        weight: 2
    }).addTo(map).bindPopup(marker.label));
}

export function drawRoute(points) {
    if (!map || !points) return;
    if (routeLayer) routeLayer.remove();
    routeLayer = L.polyline(points, {
        color: '#50dfda',
        weight: 4,
        opacity: 0.9,
        dashArray: '7 8'
    }).addTo(map);
    map.fitBounds(routeLayer.getBounds(), { padding: [35, 35] });
}