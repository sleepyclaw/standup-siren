const form = document.querySelector('#settings-form');
const nextTriggerEl = document.querySelector('#nextTrigger');
const meetingTimeEl = document.querySelector('#meetingTime');
const offsetSecondsEl = document.querySelector('#offsetSeconds');

const defaultSettings = {
  meetingTime: '10:00',
  offsetSeconds: 10,
  launchOnLogin: false,
};

let settings = { ...defaultSettings };

function nextTriggerText(meetingTime, offsetSeconds) {
  const now = new Date();
  const [hours, minutes] = meetingTime.split(':').map(Number);
  const next = new Date(now);
  next.setHours(hours, minutes, 0, 0);
  next.setSeconds(next.getSeconds() - Number(offsetSeconds || 0));
  if (next <= now) next.setDate(next.getDate() + 1);
  return next.toLocaleString();
}

function render() {
  meetingTimeEl.value = settings.meetingTime;
  offsetSecondsEl.value = settings.offsetSeconds;
  document.querySelector('#launchOnLogin').checked = settings.launchOnLogin;
  nextTriggerEl.textContent = nextTriggerText(settings.meetingTime, settings.offsetSeconds);
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  settings = {
    meetingTime: meetingTimeEl.value,
    offsetSeconds: Number(offsetSecondsEl.value),
    launchOnLogin: document.querySelector('#launchOnLogin').checked,
  };
  nextTriggerEl.textContent = nextTriggerText(settings.meetingTime, settings.offsetSeconds);
  alert('MVP scaffold only: persistence and playback wiring come next.');
});

document.querySelector('#testSound').addEventListener('click', () => {
  alert('Test sound wiring comes next.');
});

render();
