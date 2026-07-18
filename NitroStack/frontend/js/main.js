import { api } from './api.js';
import { AGENT_ORDER, WORKFLOW_DELAY_MS } from './config.js';
import { addMarkers, drawRoute, initializeMap } from './map.js';
import { $, addTimelineEvent, renderAgents, renderOrganizations, setMission, setMissionState, setProgress, setStartButton, showSummary, toast } from './ui.js';

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
let agentData = [];
function time() { return new Intl.DateTimeFormat('en-IN', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Asia/Kolkata' }).format(new Date()); }
function initialAgents() { return AGENT_ORDER.map(key => ({ agent: `${key === 'communications' ? 'Comms' : key[0].toUpperCase() + key.slice(1)} Agent`, icon: '◌', status: 'READY', action: 'Awaiting Mission Commander' })); }
renderAgents(initialAgents());

document.querySelectorAll('.scenario').forEach(button => button.addEventListener('click', () => { if (button.dataset.scenario !== 'flood') { toast('Scenario coming soon'); return; } document.querySelectorAll('.scenario').forEach(item => item.classList.remove('active')); button.classList.add('active'); }));
$('startMission').addEventListener('click', startMission);
$('report').addEventListener('click', downloadReport);

async function startMission() {
  setStartButton(true); $('summaryCard').hidden = true; $('report').disabled = true; $('timelineList').innerHTML = ''; agentData = [];
  try {
    const mission = await api.startMission(); setMission(mission); initializeMap(mission.coordinates); setMissionState(`Mission active · ${mission.id}`); setProgress(0, AGENT_ORDER.length);
    addTimelineEvent({ number: 1, time: time(), title: 'Mission started', detail: `Mission Commander activated for ${mission.location}` });
    for (const [index, key] of AGENT_ORDER.entries()) {
      const current = initialAgents(); agentData.forEach((data, completedIndex) => current[completedIndex] = data); current[index] = { agent: `${key === 'communications' ? 'Comms' : key[0].toUpperCase() + key.slice(1)} Agent`, icon: '◌', status: 'WORKING', action: 'Retrieving operational response…' }; renderAgents(current);
      const data = await api.getAgent(key); await sleep(WORKFLOW_DELAY_MS); agentData.push(data); renderAgents([...agentData, ...initialAgents().slice(index + 1)]); renderOrganizations(agentData); setProgress(index + 1, AGENT_ORDER.length);
      if (data.mapMarkers) addMarkers(data.mapMarkers); if (data.route) drawRoute(data.route);
      addTimelineEvent({ number: index + 2, time: time(), title: data.action, detail: data.recipients ? `Alert sent to: ${data.recipients.join(', ')}` : data.description });
    }
    const summary = await api.getSummary(); showSummary(summary); setMissionState('Mission plan generated · response coordinated'); $('timelineStatus').textContent = 'Live response plan complete'; toast('Mission plan generated');
  } catch (error) { setMissionState('Mission interrupted · retry required'); toast('Unable to complete mission. Please retry.'); console.error(error); }
  finally { setStartButton(false); }
}
async function downloadReport() { const report = await api.getReport(); const url = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' })); const link = document.createElement('a'); link.href = url; link.download = `sentinelos-incident-report-${new Date().toISOString().slice(0, 10)}.json`; link.click(); URL.revokeObjectURL(url); toast('Incident report downloaded'); }
