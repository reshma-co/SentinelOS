from __future__ import annotations

import os
from uuid import uuid4

import requests

from .data import (
    AMBULANCES,
    HOSPITALS,
    MEDICAL_TEAMS,
    POLICE_UNITS,
    ROADS,
    TRAFFIC_REPORTS,
    VEHICLES,
    WEATHER_PROFILES,
    utc_now,
)


def _contains(value: str, query: str) -> bool:
    return query.lower() in value.lower() or value.lower() in query.lower()


class WeatherService:
    def forecast(
        self,
        location: str,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> dict:
        if (
            os.getenv("WEATHER_USE_OPEN_METEO", "false").lower() == "true"
            and latitude
            and longitude
        ):
            live = self._open_meteo_forecast(location, latitude, longitude)
            if live:
                return live

        profile = WEATHER_PROFILES.get(location.lower(), WEATHER_PROFILES["chennai"])
        return {
            "location": profile["location"],
            "current_conditions": profile["conditions"],
            "temperature_c": profile["temperature_c"],
            "rainfall_mm": profile["rainfall_mm"],
            "wind_speed_kmph": profile["wind_speed_kmph"],
            "forecast_summary": profile["forecast_summary"],
            "timestamp": utc_now(),
            "data_source": "mock_weather_profiles",
            "high_risk_zones": profile["high_risk_zones"],
            "coordinates": {
                "latitude": latitude or profile["latitude"],
                "longitude": longitude or profile["longitude"],
            },
        }

    def flood_prediction(
        self,
        location: str,
        rainfall_mm: float | None = None,
        forecast_rainfall_mm: float | None = None,
        drainage_capacity: str = "moderate",
        river_level: str = "normal",
        soil_saturation: str = "moderate",
        incident_description: str = "",
        emergency_type: str | None = None,
    ) -> dict:
        forecast = self.forecast(location)
        desc = (incident_description or emergency_type or "").lower()

        # Dynamic branching based on emergency/scenario type
        if "earthquake" in desc or "seismic" in desc:
            return {
                "location": forecast["location"],
                "flood_risk_level": "LOW",
                "seismic_hazard_level": "HIGH",
                "reasoning": [
                    "Seismic activity detected; structural integrity risk.",
                    "Aftershock probability: 65% in next 12 hours.",
                    "No immediate flood or heavy rainfall impedance.",
                ],
                "rainfall_information": {
                    "observed_or_forecast_mm": forecast["rainfall_mm"],
                    "score": 0,
                },
                "recommended_precautions": [
                    "Monitor for secondary aftershocks",
                    "Ensure structural stability of temporary shelters",
                    "Keep clear of compromised or damaged buildings",
                ],
                "affected_high_risk_zones": forecast["high_risk_zones"],
                "timestamp": utc_now(),
            }
        elif "chemical" in desc or "leak" in desc:
            return {
                "location": forecast["location"],
                "flood_risk_level": "LOW",
                "hazmat_hazard_level": "CRITICAL",
                "reasoning": [
                    f"Wind speed: {forecast['wind_speed_kmph']} km/h",
                    "Plume dispersion risk evaluated.",
                ],
                "rainfall_information": {
                    "observed_or_forecast_mm": forecast["rainfall_mm"],
                    "score": 0,
                },
                "recommended_precautions": [
                    "Monitor downwind plume dispersal corridors",
                    "Issue immediate air quality and shelter-in-place advisories",
                    "Establish hazmat containment and exclusion perimeters",
                ],
                "affected_high_risk_zones": forecast["high_risk_zones"],
                "timestamp": utc_now(),
            }
        elif "power" in desc or "outage" in desc or "grid" in desc:
            return {
                "location": forecast["location"],
                "flood_risk_level": "LOW",
                "grid_hazard_level": "HIGH",
                "reasoning": [
                    "Grid blackouts affecting municipal services and traffic control.",
                    "Backup power systems recommended for critical infrastructure.",
                ],
                "rainfall_information": {
                    "observed_or_forecast_mm": forecast["rainfall_mm"],
                    "score": 0,
                },
                "recommended_precautions": [
                    "Deploy emergency generators to field hospitals",
                    "Maintain priority power lines for communications",
                    "Stage emergency traffic officers at key unlit intersections",
                ],
                "affected_high_risk_zones": forecast["high_risk_zones"],
                "timestamp": utc_now(),
            }

        # Default Flood Calculation Logic
        rainfall = rainfall_mm if rainfall_mm is not None else forecast_rainfall_mm
        rainfall = rainfall if rainfall is not None else forecast["rainfall_mm"]
        score = rainfall
        if drainage_capacity.lower() == "poor":
            score += 20
        if river_level.lower() in {"high", "overflowing"}:
            score += 25
        if soil_saturation.lower() == "high":
            score += 15

        if score >= 115:
            level = "CRITICAL"
        elif score >= 80:
            level = "HIGH"
        elif score >= 45:
            level = "MODERATE"
        else:
            level = "LOW"

        precautions = {
            "LOW": ["Monitor rainfall updates", "Keep storm drains clear"],
            "MODERATE": [
                "Pre-position response teams",
                "Warn residents in low-lying wards",
            ],
            "HIGH": [
                "Open relief shelters",
                "Prepare evacuation transport",
                "Block unsafe roads",
            ],
            "CRITICAL": [
                "Begin evacuation in high-risk zones",
                "Deploy boats and medical teams",
                "Issue public alerts",
            ],
        }[level]

        return {
            "location": forecast["location"],
            "flood_risk_level": level,
            "reasoning": [
                f"Rainfall signal: {rainfall} mm",
                f"Drainage capacity: {drainage_capacity}",
                f"River level: {river_level}",
                f"Soil saturation: {soil_saturation}",
            ],
            "rainfall_information": {
                "observed_or_forecast_mm": rainfall,
                "score": score,
            },
            "recommended_precautions": precautions,
            "affected_high_risk_zones": forecast["high_risk_zones"],
            "timestamp": utc_now(),
        }

    def weather_resource(self) -> dict:
        return {
            "source": "mock_weather_profiles",
            "records": list(WEATHER_PROFILES.values()),
            "timestamp": utc_now(),
        }

    def _open_meteo_forecast(
        self, location: str, latitude: float, longitude: float
    ) -> dict | None:
        try:
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,wind_speed_10m,rain",
                    "hourly": "rain",
                    "forecast_days": 1,
                },
                timeout=float(os.getenv("WEATHER_API_TIMEOUT_SECONDS", "5")),
            )
            response.raise_for_status()
            payload = response.json()
            current = payload.get("current", {})
            return {
                "location": location,
                "current_conditions": "Live Open-Meteo current weather",
                "temperature_c": current.get("temperature_2m"),
                "rainfall_mm": current.get("rain", 0),
                "wind_speed_kmph": current.get("wind_speed_10m"),
                "forecast_summary": "Live forecast fetched from Open-Meteo.",
                "timestamp": current.get("time") or utc_now(),
                "data_source": "open-meteo",
                "high_risk_zones": [],
                "coordinates": {"latitude": latitude, "longitude": longitude},
            }
        except requests.RequestException:
            return None


class HospitalService:
    def find_hospital(
        self, location: str, emergency_type: str | None = None, radius_km: float = 10
    ) -> dict:
        matches = []
        loc_clean = location.lower()
        for hospital in HOSPITALS:
            hosp_loc = hospital["location"].lower()
            capability_match = (
                not emergency_type
                or emergency_type.lower()
                in " ".join(hospital["emergency_capabilities"]).lower()
            )

            # Strict Location Matching: Filter out cross-city matches (e.g. Mumbai when location is Chennai)
            is_same_city = _contains(hosp_loc, loc_clean) or loc_clean in {
                "nearby",
                "current",
                "all",
            }

            if capability_match and is_same_city:
                matches.append(hospital)

        return {
            "location": location,
            "matching_hospitals": matches,
            "count": len(matches),
            "data_source": "mock_hospital_database",
        }

    def check_icu(self, hospital_id_or_name: str) -> dict:
        for hospital in HOSPITALS:
            if hospital_id_or_name.lower() in {
                hospital["id"].lower(),
                hospital["name"].lower(),
            }:
                available = hospital["icu_total"] - hospital["icu_occupied"]
                return {
                    "hospital_id": hospital["id"],
                    "hospital_name": hospital["name"],
                    "total_icu_beds": hospital["icu_total"],
                    "occupied_icu_beds": hospital["icu_occupied"],
                    "available_icu_beds": available,
                    "status": "available" if available > 2 else "near-capacity",
                }
        raise ValueError(f"No hospital found for '{hospital_id_or_name}'")

    def find_ambulance(self, location: str, radius_km: float = 10) -> dict:
        loc_clean = location.lower()
        matches = [
            amb
            for amb in AMBULANCES
            if amb["status"] == "available"
            and (
                _contains(amb["location"].lower(), loc_clean)
                or loc_clean in {"nearby", "current", "all"}
            )
        ]
        return {
            "location": location,
            "available_ambulances": matches,
            "count": len(matches),
            "data_source": "mock_ambulance_locations",
        }

    def allocate_medical_team(
        self,
        incident_location: str,
        emergency_severity: str,
        required_specialization: str | None = None,
    ) -> dict:
        required = (required_specialization or "trauma").lower()
        team = next(
            (
                team
                for team in MEDICAL_TEAMS
                if team["status"] == "ready" and required in team["specialization"]
            ),
            MEDICAL_TEAMS[0],
        )
        hospital = next(h for h in HOSPITALS if h["id"] == team["hospital_id"])
        return {
            "allocation_id": f"MED-ALLOC-{uuid4().hex[:8].upper()}",
            "assigned_team": team,
            "hospital": {"id": hospital["id"], "name": hospital["name"]},
            "incident_location": incident_location,
            "severity": emergency_severity.upper(),
            "status": "assigned",
            "estimated_arrival_minutes": 16
            if emergency_severity.lower() in {"high", "critical"}
            else 24,
        }

    def resources(self) -> dict:
        return {
            "hospital_database": HOSPITALS,
            "ambulance_locations": AMBULANCES,
            "bed_capacity": [self.check_icu(h["id"]) for h in HOSPITALS],
        }


class PoliceService:
    def find_safe_route(
        self, origin: str, destination: str, blocked_roads: list[str] | None = None
    ) -> dict:
        blocked = {road.lower() for road in (blocked_roads or [])}
        active_blocked = {
            r["location"].lower()
            for r in TRAFFIC_REPORTS
            if r["status"] == "active" and r["severity"] in {"HIGH", "CRITICAL"}
        }
        blocked.update(active_blocked)
        candidates = [
            road
            for road in ROADS
            if road["status"] != "blocked" and road["name"].lower() not in blocked
        ]
        best = (
            min(candidates, key=lambda road: road["travel_time_minutes"] or 999)
            if candidates
            else ROADS[0]
        )
        alt = candidates[1] if len(candidates) > 1 else None
        return {
            "origin": origin,
            "destination": destination,
            "recommended_safe_route": [origin, best["name"], destination],
            "alternative_route": [origin, alt["name"], destination] if alt else None,
            "blocked_roads_avoided": sorted(blocked),
            "estimated_travel_minutes": best["travel_time_minutes"],
            "data_source": "mock_road_database",
        }

    def report_road_block(
        self,
        road_location: str,
        reason: str,
        severity: str,
        description: str | None = None,
    ) -> dict:
        report = {
            "id": f"TRF-{uuid4().hex[:8].upper()}",
            "location": road_location,
            "reason": reason,
            "severity": severity.upper(),
            "description": description,
            "status": "active",
            "timestamp": utc_now(),
        }
        TRAFFIC_REPORTS.append(report)
        return {
            "report_id": report["id"],
            "location": road_location,
            "status": "active",
            "timestamp": report["timestamp"],
        }

    def assign_officers(
        self, incident_location: str, required_number_of_officers: int, priority: str
    ) -> dict:
        unit = next(
            (
                unit
                for unit in POLICE_UNITS
                if unit["status"] == "available"
                and unit["officers"] >= required_number_of_officers
            ),
            POLICE_UNITS[0],
        )
        return {
            "assignment_id": f"POL-ASSIGN-{uuid4().hex[:8].upper()}",
            "assigned_unit": unit,
            "incident_location": incident_location,
            "status": "assigned",
            "priority": priority.upper(),
            "estimated_arrival_minutes": unit["eta_minutes"],
        }

    def resources(self) -> dict:
        return {"road_database": ROADS, "traffic_reports": TRAFFIC_REPORTS}


class TransportService:
    def find_rescue_vehicle(
        self,
        location: str,
        vehicle_type: str = "rescue",
        radius_km: float = 15,
        incident_description: str = "",
    ) -> dict:
        loc_clean = location.lower()
        desc = incident_description.lower()

        # Dynamic vehicle type override if generic or mismatched
        if "earthquake" in desc or "seismic" in desc or "collapse" in desc:
            wanted = "truck"  # Clearance / heavy rescue equipment
        elif "chemical" in desc or "hazmat" in desc:
            wanted = "bus"  # Evacuation transport
        elif "flood" in desc or "water" in desc:
            wanted = "boat"  # Rescue boats
        else:
            wanted = vehicle_type.lower()

        matches = [
            vehicle
            for vehicle in VEHICLES
            if vehicle["availability"] == "available"
            and wanted in vehicle["type"].lower()
            and (
                _contains(vehicle["location"].lower(), loc_clean)
                or loc_clean in {"nearby", "current", "all"}
            )
        ]

        # Fallback to any available vehicle in that city if specific type is missing
        if not matches:
            matches = [
                vehicle
                for vehicle in VEHICLES
                if vehicle["availability"] == "available"
                and (
                    _contains(vehicle["location"].lower(), loc_clean)
                    or loc_clean in {"nearby", "current", "all"}
                )
            ]

        return {
            "location": location,
            "vehicle_type": wanted,
            "available_rescue_vehicles": matches,
            "count": len(matches),
        }

    def route_planning(
        self,
        origin: str,
        destination: str,
        vehicle_type: str,
        blocked_roads: list[str] | None = None,
    ) -> dict:
        route = PoliceService().find_safe_route(origin, destination, blocked_roads)
        warnings = []
        if "boat" in vehicle_type.lower():
            warnings.append(
                "Use only waterlogged or flood-access corridors for boat deployment."
            )
        if "bus" in vehicle_type.lower() or "truck" in vehicle_type.lower():
            warnings.append(
                "Avoid narrow or blocked streets; stage along main arterial roads."
            )
        return {
            "origin": origin,
            "destination": destination,
            "vehicle_type": vehicle_type,
            "recommended_route": route["recommended_safe_route"],
            "alternative_route": route["alternative_route"],
            "estimated_travel_minutes": route["estimated_travel_minutes"],
            "restrictions_or_warnings": warnings,
            "blocked_roads_avoided": route["blocked_roads_avoided"],
        }

    def vehicle_resource(self) -> dict:
        return {"vehicle_database": VEHICLES, "timestamp": utc_now()}
