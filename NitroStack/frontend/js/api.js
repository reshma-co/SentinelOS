import { API_BASE_URL } from './config.js';

const scenario = {
  mission: { id: 'IN-26-0718', title: 'Monsoon flooding: response in motion', description: 'SentinelOS is connecting independent response organizations, prioritizing critical needs, and coordinating a single field-ready action plan.', location: 'Kochi, Kerala', riskLevel: 'HIGH', agencies: 6, affectedPopulation: 500, coordinates: [9.9312, 76.2673] },
  weather: { agent: 'Weather Agent', icon: '☁', status: 'COMPLETED', action: 'Flood forecast confirmed', organization: 'Weather Department', description: '180 mm rainfall recorded. Heavy rain expected over the next 4 hours.', metric: '180 mm', metricLabel: 'rainfall recorded', mapMarkers: [{ type: 'incident', label: 'Flood incident · Zone A', coordinates: [9.935, 76.274] }] },
  hospital: { agent: 'Hospital Agent', icon: '✚', status: 'COMPLETED', action: 'Medical capacity confirmed', organization: 'City Hospitals', description: 'Amrita Hospital confirmed critical-care capacity and ambulance availability.', metric: '12', metricLabel: 'beds available', mapMarkers: [{ type: 'hospital', label: 'Amrita Hospital · 12 beds, 3 ICU', coordinates: [9.966, 76.281] }] },
  police: { agent: 'Police Agent', icon: '⌁', status: 'ALERT', action: 'Safe route validated', organization: 'Police Control', description: '3 flooded roads are closed. MC Road is cleared as the safe evacuation corridor.', metric: '1', metricLabel: 'safe evacuation route', route: [[9.935, 76.274], [9.942, 76.265], [9.951, 76.258]] },
  volunteers: { agent: 'Volunteer Agent', icon: '♡', status: 'COMPLETED', action: 'Shelter team mobilized', organization: 'Volunteer Network', description: '38 volunteers mobilized. ABC School is ready to receive evacuees.', metric: '38', metricLabel: 'volunteers mobilized', mapMarkers: [{ type: 'shelter', label: 'ABC School shelter · capacity 600', coordinates: [9.951, 76.258] }] },
  transport: { agent: 'Transport Agent', icon: '▣', status: 'COMPLETED', action: 'Rescue fleet dispatched', organization: 'Transport Control', description: '12 rescue boats and 8 buses are available. Rescue team has been dispatched.', metric: '18 min', metricLabel: 'rescue team ETA' },
  communications: { agent: 'Comms Agent', icon: '◉', status: 'COMPLETED', action: 'Evacuation alert sent', organization: 'Emergency Communications', description: 'Flood alert sent to Zone A residents and partner response organizations.', metric: '4', metricLabel: 'organizations notified', recipients: ['Kochi Police Control', 'Amrita Hospital', 'Volunteer Network', 'Transport Control'] },
  summary: { title: 'Unified flood response plan', items: ['Evacuate Zone A residents through MC Road to ABC School.', 'Deploy 12 rescue boats, 8 buses, and 5 ambulances to the high-risk zone.', 'Rescue team arrival estimated in 18 minutes; alerts sent to 4 response organizations.'] }
};

async function request(path, options) { const response = await fetch(`${API_BASE_URL}${path}`, options); if (!response.ok) throw new Error(`API ${response.status}`); return response.json(); }
export const api = {
  async startMission() { try { return await request('/mission/start', { method: 'POST' }); } catch { return scenario.mission; } },
  async getAgent(key) { try { return await request(`/${key}`); } catch { return scenario[key]; } },
  async getSummary() { try { return await request('/mission/summary'); } catch { return scenario.summary; } },
  async getReport() { try { return await request('/mission/report'); } catch { return { generatedAt: new Date().toISOString(), ...scenario }; } }
};
