const $ = id => document.getElementById(id);
const value = (input, fallback) => input ?? fallback;

export function renderAgents(agents) {
  $('agentGrid').innerHTML = agents.map(item => {
    const status = value(item?.status, 'READY');
    return `<article class="card agent"><div class="agent-top"><span class="agent-icon">${value(item?.icon, 'o')}</span><span class="status ${status.toLowerCase()}">${status}</span></div><div class="agent-name">${value(item?.agent, 'Response Agent')}</div><div class="agent-action">${value(item?.action, 'Awaiting Mission Commander')}</div></article>`;
  }).join('');
}

export function renderOrganizations(agents) {
  $('organizationGrid').innerHTML = agents.map((item, index) => `<article class="card org"><div class="org-title"><i style="background:${['var(--cyan)','var(--green)','var(--amber)','var(--violet)','var(--blue)','var(--red)'][index]}"></i>${value(item?.organization, 'Response Organization')}</div><p>${value(item?.description, 'Operational response generated.')}</p><div class="metric">${value(item?.metric, 'Ready')} <small>${value(item?.metricLabel, 'status')}</small></div></article>`).join('');
}

export function addTimelineEvent({ time, title, detail, number }) {
  const event = document.createElement('div');
  event.className = 'event';
  event.innerHTML = `<div class="dot">${String(value(number, 0)).padStart(2, '0')}</div><b>${value(title, 'Mission update')}</b><p>${value(detail, 'Response update received')}<br>${value(time, '--:--')} IST</p>`;
  $('timelineList').append(event);
}

export function setMission(mission = {}) {
  const location = value(mission?.location, 'Selected location');
  const riskLevel = value(mission?.riskLevel, 'UNKNOWN');
  const agencies = value(mission?.agencies, 6);
  $('selectedLocation').textContent = location;
  $('missionTitle').textContent = value(mission?.title, 'Emergency response mission');
  $('missionDescription').textContent = value(mission?.description, 'Mission Commander is coordinating response organizations.');
  $('riskLevel').textContent = riskLevel;
  $('riskBadge').textContent = `RISK LEVEL: ${riskLevel}`;
  $('agencyCount').textContent = agencies;
  $('agentsOnline').textContent = `0/${agencies}`;
  $('mapTitle').textContent = `${location} operations area`;
}

export function setProgress(completed, total) {
  $('tasksComplete').textContent = value(completed, 0);
  $('agentsOnline').textContent = `${value(completed, 0)}/${value(total, 6)}`;
}

export function setMissionState(message) {
  $('missionState').textContent = value(message, 'Mission ready');
}

export function showSummary(summary = {}) {
  const items = Array.isArray(summary?.items) && summary.items.length ? summary.items : ['Mission response generated.'];
  $('summaryCard').hidden = false;
  $('summaryTitle').textContent = value(summary?.title, 'Unified emergency response plan');
  $('summaryList').innerHTML = items.map(item => `<li>${item}</li>`).join('');
  $('report').disabled = false;
}

export function toast(message) {
  const target = $('toast');
  target.textContent = value(message, 'Update received');
  target.classList.add('show');
  setTimeout(() => target.classList.remove('show'), 3000);
}

export function setStartButton(running, scenario = 'flood') {
  const labels = {
    flood: 'Start flood mission',
    earthquake: 'Start earthquake mission',
    chemical: 'Start chemical leak mission',
    power: 'Start power outage mission'
  };
  $('startMission').disabled = running;
  $('startMission').textContent = running ? 'Mission in progress...' : value(labels[scenario], 'Start mission');
}

export { $ };
