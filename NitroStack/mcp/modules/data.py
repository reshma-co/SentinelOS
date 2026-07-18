from __future__ import annotations

from datetime import UTC, datetime


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


WEATHER_PROFILES = {
    "chennai": {
        "location": "Chennai",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "conditions": "Heavy monsoon rain with localized waterlogging",
        "temperature_c": 28.4,
        "rainfall_mm": 86.0,
        "wind_speed_kmph": 32.0,
        "forecast_summary": "More intense showers likely over low-lying coastal zones for the next 6 hours.",
        "high_risk_zones": ["Velachery", "Mudichur", "Tambaram", "Adyar river belt"],
    },
    "mumbai": {
        "location": "Mumbai",
        "latitude": 19.076,
        "longitude": 72.8777,
        "conditions": "Continuous rain with gusty coastal winds",
        "temperature_c": 27.2,
        "rainfall_mm": 72.0,
        "wind_speed_kmph": 38.0,
        "forecast_summary": "Urban flooding possible near underpasses and coastal arterial roads.",
        "high_risk_zones": ["Sion", "Kurla", "Hindmata", "Andheri subway"],
    },
    "bengaluru": {
        "location": "Bengaluru",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "conditions": "Cloudy with intermittent thunderstorms",
        "temperature_c": 23.8,
        "rainfall_mm": 34.0,
        "wind_speed_kmph": 18.0,
        "forecast_summary": "Moderate showers may affect traffic corridors and lake-adjacent wards.",
        "high_risk_zones": ["Bellandur", "Mahadevapura", "Hebbal", "Silk Board"],
    },
}


HOSPITALS = [
    {
        "id": "HSP-CHN-001",
        "name": "Sentinel General Hospital",
        "location": "Chennai Central",
        "distance_km": 3.2,
        "emergency_capabilities": ["trauma", "flood rescue", "pediatrics", "critical care"],
        "available_beds": 42,
        "icu_total": 30,
        "icu_occupied": 22,
        "status": "operational",
    },
    {
        "id": "HSP-CHN-002",
        "name": "Nexa Multispecialty Center",
        "location": "Velachery",
        "distance_km": 7.8,
        "emergency_capabilities": ["trauma", "orthopedics", "critical care"],
        "available_beds": 18,
        "icu_total": 18,
        "icu_occupied": 16,
        "status": "high-load",
    },
    {
        "id": "HSP-MUM-001",
        "name": "Harbor Emergency Institute",
        "location": "Mumbai",
        "distance_km": 4.6,
        "emergency_capabilities": ["trauma", "burns", "critical care"],
        "available_beds": 27,
        "icu_total": 24,
        "icu_occupied": 19,
        "status": "operational",
    },
]


AMBULANCES = [
    {"id": "AMB-101", "location": "Chennai Central", "status": "available", "eta_minutes": 9, "radius_km": 10},
    {"id": "AMB-118", "location": "Velachery", "status": "available", "eta_minutes": 14, "radius_km": 8},
    {"id": "AMB-207", "location": "Mumbai", "status": "available", "eta_minutes": 11, "radius_km": 12},
    {"id": "AMB-305", "location": "Tambaram", "status": "assigned", "eta_minutes": 22, "radius_km": 7},
]


MEDICAL_TEAMS = [
    {"id": "MED-T01", "specialization": "trauma", "hospital_id": "HSP-CHN-001", "status": "ready"},
    {"id": "MED-T02", "specialization": "critical care", "hospital_id": "HSP-CHN-002", "status": "ready"},
    {"id": "MED-T03", "specialization": "flood rescue", "hospital_id": "HSP-CHN-001", "status": "ready"},
]


ROADS = [
    {"name": "Anna Salai", "status": "open", "risk": "LOW", "travel_time_minutes": 18},
    {"name": "OMR", "status": "restricted", "risk": "MODERATE", "travel_time_minutes": 34},
    {"name": "Velachery Main Road", "status": "blocked", "risk": "HIGH", "travel_time_minutes": None},
    {"name": "GST Road", "status": "open", "risk": "LOW", "travel_time_minutes": 26},
    {"name": "Eastern Express Highway", "status": "open", "risk": "LOW", "travel_time_minutes": 22},
]


TRAFFIC_REPORTS = [
    {
        "id": "TRF-001",
        "location": "Velachery Main Road",
        "reason": "flooding",
        "severity": "HIGH",
        "status": "active",
        "timestamp": "2026-07-17T08:20:00+00:00",
    },
    {
        "id": "TRF-002",
        "location": "OMR",
        "reason": "slow traffic near waterlogged stretch",
        "severity": "MODERATE",
        "status": "active",
        "timestamp": "2026-07-17T08:45:00+00:00",
    },
]


POLICE_UNITS = [
    {"id": "POL-U01", "location": "Chennai Central", "officers": 8, "status": "available", "eta_minutes": 12},
    {"id": "POL-U02", "location": "Velachery", "officers": 6, "status": "available", "eta_minutes": 10},
    {"id": "POL-U03", "location": "Tambaram", "officers": 10, "status": "available", "eta_minutes": 18},
]


VEHICLES = [
    {
        "id": "VEH-BOAT-01",
        "type": "rescue boat",
        "location": "Velachery",
        "availability": "available",
        "capacity": "8 people",
        "radius_km": 12,
    },
    {
        "id": "VEH-BUS-04",
        "type": "bus",
        "location": "Tambaram",
        "availability": "available",
        "capacity": "42 people",
        "radius_km": 20,
    },
    {
        "id": "VEH-TRUCK-09",
        "type": "truck",
        "location": "Chennai Central",
        "availability": "available",
        "capacity": "4 tons relief cargo",
        "radius_km": 25,
    },
    {
        "id": "VEH-ERV-12",
        "type": "emergency response vehicle",
        "location": "Adyar",
        "availability": "available",
        "capacity": "6 responders",
        "radius_km": 15,
    },
]
