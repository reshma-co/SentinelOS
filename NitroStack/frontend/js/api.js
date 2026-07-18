import { API_BASE_URL } from './config.js';

const fallbackScenario = {
  mission: {
    id: 'IN-26-0718',
    title: 'Emergency response mission',
    description: 'SentinelOS is connecting response organizations and coordinating a field-ready action plan.',
    location: 'Kochi, Kerala',
    riskLevel: 'HIGH',
    agencies: 6,
    affectedPopulation: 500,
    coordinates: [9.9312, 76.2673]
  },
  weather: { agent: 'Weather Agent', icon: 'o', status: 'COMPLETED', action: 'Environmental risk checked', organization: 'Weather Department', description: 'Weather and environmental conditions reviewed.', metric: 'Ready', metricLabel: 'feed active' },
  hospital: { agent: 'Hospital Agent', icon: 'o', status: 'COMPLETED', action: 'Medical capacity checked', organization: 'City Hospitals', description: 'Emergency medical capacity reviewed.', metric: 'Ready', metricLabel: 'triage active' },
  police: { agent: 'Police Agent', icon: 'o', status: 'COMPLETED', action: 'Public safety response checked', organization: 'Police Control', description: 'Traffic and perimeter safety response reviewed.', metric: 'Ready', metricLabel: 'unit active' },
  volunteers: { agent: 'Volunteer Agent', icon: 'o', status: 'COMPLETED', action: 'Shelter team checked', organization: 'Volunteer Network', description: 'Volunteer and shelter support reviewed.', metric: 'Ready', metricLabel: 'team active' },
  transport: { agent: 'Transport Agent', icon: 'o', status: 'COMPLETED', action: 'Transport response checked', organization: 'Transport Control', description: 'Evacuation route and fleet response reviewed.', metric: 'Ready', metricLabel: 'route active' },
  communications: { agent: 'Comms Agent', icon: 'o', status: 'COMPLETED', action: 'Alert response checked', organization: 'Emergency Communications', description: 'Emergency alerts prepared for response partners.', metric: 'Ready', metricLabel: 'channels active' },
  summary: { title: 'Unified emergency response plan', items: ['Coordinate responding organizations.', 'Prioritize public safety actions.', 'Keep emergency alerts active.'] }
};

async function request(path, options) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  if (!response.ok) throw new Error(`API ${response.status}`);
  return response.json();
}

export const api = {
  async startMission(scenario) {
    try {
      return await request('/mission/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario })
      });
    } catch {
      return { ...fallbackScenario.mission, scenario };
    }
  },
  async getAgent(key, scenario) {
    try {
      return await request(`/${key}?scenario=${encodeURIComponent(scenario || 'flood')}`);
    } catch {
      return fallbackScenario[key];
    }
  },
  async getSummary() {
    try {
      return await request('/mission/summary');
    } catch {
      return fallbackScenario.summary;
    }
  },
  async getReport() {
    try {
      return await request('/mission/report');
    } catch {
      return { generatedAt: new Date().toISOString(), ...fallbackScenario };
    }
  }
};
