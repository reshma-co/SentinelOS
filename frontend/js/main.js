import { api } from './api.js';
import { WORKFLOW_DELAY_MS } from './config.js';
import { addMarkers, drawRoute, initializeMap } from './map.js';
import { $, addTimelineEvent, renderAgents, renderOrganizations, setMission, setMissionState, setProgress, setStartButton, showSummary, toast } from './ui.js';

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

const scenarioNames = {
  flood: 'Flood Emergency',
  earthquake: 'Earthquake Response',
  chemical: 'Chemical Leak',
  power: 'Power Outage'
};

// City Coordinate Lookup
const cityCoordinates = {
  chennai: [13.0827, 80.2707],
  kochi: [9.9312, 76.2673],
  bengaluru: [12.9716, 77.5946],
  bangalore: [12.9716, 77.5946],
  mumbai: [19.0760, 72.8777],
  delhi: [28.6139, 77.2090]
};

function getCoordinates(locationName) {
  if (!locationName) return cityCoordinates.chennai;
  const key = String(locationName).trim().toLowerCase();
  for (const [city, coords] of Object.entries(cityCoordinates)) {
    if (key.includes(city)) return coords;
  }
  return cityCoordinates.chennai; // Fallback
}

let selectedScenario = 'flood';
let currentMission = null; // Holds the active UnifiedMissionResponse

function time() {
  return new Intl.DateTimeFormat('en-IN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'Asia/Kolkata'
  }).format(new Date());
}

// Event Listeners for Scenario Selector
document.querySelectorAll('.scenario').forEach(button => {
  button.addEventListener('click', () => {
    selectedScenario = button.dataset.scenario || 'flood';
    document.querySelectorAll('.scenario').forEach(item => item.classList.remove('active'));
    button.classList.add('active');
    $('selectedName').textContent = scenarioNames[selectedScenario] || 'Emergency Mission';
    setStartButton(false, selectedScenario);
  });
});

$('startMission').addEventListener('click', startMission);
$('report').addEventListener('click', downloadReport);

async function startMission() {
  setStartButton(true, selectedScenario);
  $('summaryCard').hidden = true;
  $('report').disabled = true;
  $('timelineList').innerHTML = '';
  currentMission = null;

  try {
    // 1. Call real backend orchestrator
    const missionData = await api.startMission(selectedScenario);
    currentMission = missionData; // Store for report download

    // 2. Setup map dynamically using the location returned by backend
    const coords = getCoordinates(missionData.location);
    setMission(missionData);
    initializeMap(coords);
    setMissionState(`Mission Active - ID: ${missionData.mission_id}`);

    // 3. Process organizational responses
    const orgResponses = missionData.organization_responses || [];
    setProgress(0, orgResponses.length);

    addTimelineEvent({
      number: 1,
      time: time(),
      title: 'Mission Commander Dispatched',
      detail: `Emergency Type: ${missionData.emergency_type} | Location: ${missionData.location}`
    });

    // 4. Step-by-step UI animation from backend response
    for (const [index, resp] of orgResponses.entries()) {
      await sleep(WORKFLOW_DELAY_MS);

      setProgress(index + 1, orgResponses.length);

      addTimelineEvent({
        number: index + 2,
        time: time(),
        title: `${resp.organization.toUpperCase()} Response Active`,
        detail: resp.summary
      });
    }

    // Update agent organization status cards
    renderOrganizations(orgResponses);

    // 5. Render final summary card
    showSummary({
      final_summary: missionData.final_summary,
      priority_actions: missionData.priority_actions,
      resource_allocation: missionData.resource_allocation
    });

    setMissionState('Mission Plan Completed');
    $('timelineStatus').textContent = 'Live response plan complete';
    $('report').disabled = false; // Enable report download
    toast('Mission plan generated successfully');

  } catch (error) {
    setMissionState('Mission Interrupted');
    toast('Unable to complete mission. Check backend server.');
    console.error('Mission Execution Error:', error);
  } finally {
    setStartButton(false, selectedScenario);
  }
}

function downloadReport() {
  if (!currentMission) {
    toast('No active mission report to download');
    return;
  }

  const blob = new Blob([JSON.stringify(currentMission, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `sentinelos-report-${currentMission.mission_id}.json`;
  link.click();
  URL.revokeObjectURL(url);
  toast('Incident report downloaded');
}