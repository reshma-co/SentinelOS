import { api } from './api.js';
import { AGENT_ORDER, WORKFLOW_DELAY_MS } from './config.js';
import { addMarkers, drawRoute, initializeMap } from './map.js';
import { $, addTimelineEvent, renderAgents, renderOrganizations, setMission, setMissionState, setProgress, setStartButton, showSummary, toast } from './ui.js';

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const scenarioNames = {
  flood: 'Flood Emergency',
  earthquake: 'Earthquake Response',
  chemical: 'Chemical Leak',
  power: 'Power Outage'
};

let agentData = [];
let selectedScenario = 'flood';

function time() {
  return new Intl.DateTimeFormat('en-IN', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Asia/Kolkata' }).format(new Date());
}

function agentTitle(key) {
  return `${key === 'communications' ? 'Comms' : key[0].toUpperCase() + key.slice(1)} Agent`;
}

function initialAgents() {
  return AGENT_ORDER.map(key => ({ agent: agentTitle(key), icon: 'o', status: 'READY', action: 'Awaiting Mission Commander' }));
}

renderAgents(initialAgents());

document.querySelectorAll('.scenario').forEach(button => button.addEventListener('click', () => {
  selectedScenario = button.dataset.scenario || 'flood';
  document.querySelectorAll('.scenario').forEach(item => item.classList.remove('active'));
  button.classList.add('active');
  $('selectedName').textContent = scenarioNames[selectedScenario] || 'Emergency Mission';
  setStartButton(false, selectedScenario);
}));

$('startMission').addEventListener('click', startMission);
$('report').addEventListener('click', downloadReport);

async function startMission() {
  setStartButton(true, selectedScenario);
  $('summaryCard').hidden = true;
  $('report').disabled = true;
  $('timelineList').innerHTML = '';
  agentData = [];
  try {
    const mission = await api.startMission(selectedScenario);
    setMission(mission);
    initializeMap(mission?.coordinates || [9.9312, 76.2673]);
    setMissionState(`Mission active - ${mission?.id || 'coordination running'}`);
    setProgress(0, AGENT_ORDER.length);
    addTimelineEvent({ number: 1, time: time(), title: 'Mission started', detail: `Mission Commander activated for ${mission?.location || 'selected location'}` });
    for (const [index, key] of AGENT_ORDER.entries()) {
      const current = initialAgents();
      agentData.forEach((data, completedIndex) => current[completedIndex] = data);
      current[index] = { agent: agentTitle(key), icon: 'o', status: 'WORKING', action: 'Retrieving operational response...' };
      renderAgents(current);
      const data = await api.getAgent(key, selectedScenario);
      await sleep(WORKFLOW_DELAY_MS);
      agentData.push(data);
      renderAgents([...agentData, ...initialAgents().slice(index + 1)]);
      renderOrganizations(agentData);
      setProgress(index + 1, AGENT_ORDER.length);
      if (data?.mapMarkers) addMarkers(data.mapMarkers);
      if (data?.route) drawRoute(data.route);
      addTimelineEvent({
        number: index + 2,
        time: time(),
        title: data?.action || `${agentTitle(key)} completed`,
        detail: data?.recipients ? `Alert sent to: ${data.recipients.join(', ')}` : (data?.description || 'Response generated')
      });
    }
    const summary = await api.getSummary();
    showSummary(summary);
    setMissionState('Mission plan generated - response coordinated');
    $('timelineStatus').textContent = 'Live response plan complete';
    toast('Mission plan generated');
  } catch (error) {
    setMissionState('Mission interrupted - retry required');
    toast('Unable to complete mission. Please retry.');
    console.error(error);
  } finally {
    setStartButton(false, selectedScenario);
  }
}

async function downloadReport() {
  const report = await api.getReport();
  const url = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = `sentinelos-incident-report-${new Date().toISOString().slice(0, 10)}.json`;
  link.click();
  URL.revokeObjectURL(url);
  toast('Incident report downloaded');
}
