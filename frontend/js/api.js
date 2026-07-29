import { API_BASE_URL } from './config.js';

async function request(path, options) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  if (!response.ok) {
    throw new Error(`API Error ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

export const api = {
  /**
   * Triggers the Mission Commander orchestrator.
   */
  async startMission(scenario, location = 'Chennai', description = 'Severe emergency reported in the area.') {
    const payload = {
      location,
      severity: 'high',
      incident_description: `${scenario.toUpperCase()}: ${description}`
    };

    return await request('/mission/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  },

  /**
   * Retrieves mission status from backend storage.
   */
  async getMissionStatus(missionId) {
    return await request(`/mission/${missionId}/status`);
  }
};