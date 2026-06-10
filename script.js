const initialSubjects = [
  {
    id: "c08",
    code: "C08 A",
    name: "Arquiteturas de Computadores",
    professor: "Prof. Henrique",
    classes: 64,
    absenceLimit: 20,
    absences: {
      Fev: { pri: 0, lab: 0, jus: 0 },
      Mar: { pri: 0, lab: 0, jus: 0 },
      Abr: { pri: 0, lab: 0, jus: 0 },
      Mai: { pri: 2, lab: 0, jus: 0 },
      Jun: { pri: 0, lab: 0, jus: 0 },
      Jul: { pri: 0, lab: 0, jus: 0 }
    },
    grades: [
      { type: "NP1", value: 75, released: true },
      { type: "NP2", value: null, released: false },
      { type: "NP3", value: null, released: false }
    ]
  },
  {
    id: "c216",
    code: "C216",
    name: "Sistemas Distribuidos",
    professor: "Profa. Mariana",
    classes: 38,
    absenceLimit: 15,
    absences: {
      Fev: { pri: 2, lab: 0, jus: 0 },
      Mar: { pri: 3, lab: 0, jus: 0 },
      Abr: { pri: 2, lab: 2, jus: 0 },
      Mai: { pri: 2, lab: 0, jus: 0 },
      Jun: { pri: 2, lab: 0, jus: 0 },
      Jul: { pri: 0, lab: 0, jus: 0 }
    },
    grades: [
      { type: "LE1", value: 55, released: true },
      { type: "LE2", value: 88, released: true },
      { type: "LE3", value: 72, released: true },
      { type: "NP1", value: 72, released: true },
      { type: "NP2", value: null, released: false },
      { type: "NP3", value: null, released: false }
    ]
  },
  {
    id: "c318",
    code: "C318",
    name: "Topicos Especiais II",
    professor: "Prof. Andre",
    classes: 42,
    absenceLimit: 10,
    absences: {
      Fev: { pri: 0, lab: 0, jus: 0 },
      Mar: { pri: 1, lab: 0, jus: 0 },
      Abr: { pri: 0, lab: 0, jus: 0 },
      Mai: { pri: 1, lab: 0, jus: 0 },
      Jun: { pri: 0, lab: 0, jus: 0 },
      Jul: { pri: 0, lab: 0, jus: 0 }
    },
    grades: [
      { type: "ATV1", value: 100, released: true },
      { type: "ATV2", value: 85, released: true },
      { type: "ATV3", value: 85, released: true },
      { type: "NP1", value: 90, released: true },
      { type: "ATV4", value: 0, released: true },
      { type: "NP2", value: null, released: false }
    ]
  },
  {
    id: "p108",
    code: "P108 L2",
    name: "Otimizacao II",
    professor: "Prof. Carlos",
    classes: 46,
    absenceLimit: 12,
    absences: {
      Fev: { pri: 1, lab: 0, jus: 0 },
      Mar: { pri: 1, lab: 1, jus: 0 },
      Abr: { pri: 1, lab: 0, jus: 0 },
      Mai: { pri: 1, lab: 1, jus: 0 },
      Jun: { pri: 0, lab: 0, jus: 0 },
      Jul: { pri: 0, lab: 0, jus: 0 }
    },
    grades: [
      { type: "NP1", value: 68, released: true },
      { type: "Projeto", value: 80, released: true },
      { type: "NP2", value: null, released: false }
    ]
  }
];

const defaultState = {
  selectedSubjectId: "c216",
  notifications: {
    enabled: false,
    grades: true,
    absences: true,
    risk: true,
    threshold: 2
  },
  subjects: initialSubjects,
  feed: [
    {
      type: "grade",
      title: "Nota NP1 publicada",
      body: "C08 A - Arquiteturas de Computadores: 75 pontos.",
      time: "Hoje, 08:42"
    },
    {
      type: "absence",
      title: "Falta lancada",
      body: "C216 - Sistemas Distribuidos recebeu 1 falta em Jun.",
      time: "Ontem, 18:10"
    },
    {
      type: "risk",
      title: "Risco de limite",
      body: "C216 esta a 2 faltas do limite previsto.",
      time: "Ontem, 18:10"
    }
  ]
};

const storageKey = "inatel-academic-notifications-v1";
const elements = {
  subjectSelect: document.querySelector("#subjectSelect"),
  permissionPanel: document.querySelector("#permissionPanel"),
  enableNotifications: document.querySelector("#enableNotifications"),
  settingsPanel: document.querySelector("#settingsPanel"),
  gradeToggle: document.querySelector("#gradeToggle"),
  absenceToggle: document.querySelector("#absenceToggle"),
  riskToggle: document.querySelector("#riskToggle"),
  riskThreshold: document.querySelector("#riskThreshold"),
  thresholdValue: document.querySelector("#thresholdValue"),
  riskBanner: document.querySelector("#riskBanner"),
  absenceMetric: document.querySelector("#absenceMetric"),
  absenceRemaining: document.querySelector("#absenceRemaining"),
  averageMetric: document.querySelector("#averageMetric"),
  gradeStatus: document.querySelector("#gradeStatus"),
  requiredMetric: document.querySelector("#requiredMetric"),
  requiredLabel: document.querySelector("#requiredLabel"),
  classesMetric: document.querySelector("#classesMetric"),
  absenceMeter: document.querySelector("#absenceMeter"),
  absenceMessage: document.querySelector("#absenceMessage"),
  gradesTable: document.querySelector("#gradesTable"),
  frequencyTable: document.querySelector("#frequencyTable"),
  notificationFeed: document.querySelector("#notificationFeed"),
  simulateGrade: document.querySelector("#simulateGrade"),
  simulateAbsence: document.querySelector("#simulateAbsence"),
  launchPanel: document.querySelector("#launchPanel"),
  closeLaunch: document.querySelector("#closeLaunch"),
  assessmentSelect: document.querySelector("#assessmentSelect"),
  gradeInput: document.querySelector("#gradeInput"),
  confirmGrade: document.querySelector("#confirmGrade"),
  resetDemo: document.querySelector("#resetDemo"),
  toast: document.querySelector("#toast"),
  drawer: document.querySelector("#drawer"),
  drawerBackdrop: document.querySelector("#drawerBackdrop"),
  menuButton: document.querySelector("#menuButton"),
  searchButton: document.querySelector("#searchButton"),
  appContent: document.querySelector("#appContent"),
  publishedLink: document.querySelector("#publishedLink")
};

let state = loadState();
let toastTimer = null;

initialize();

function initialize() {
  bindEvents();
  renderSubjects();
  syncNotificationControls();
  render();
  updatePublishedLink();
}

function bindEvents() {
  elements.subjectSelect.addEventListener("change", (event) => {
    state.selectedSubjectId = event.target.value;
    saveState();
    render();
  });

  elements.enableNotifications.addEventListener("click", enableNotifications);

  elements.gradeToggle.addEventListener("change", () => updateNotificationSetting("grades", elements.gradeToggle.checked));
  elements.absenceToggle.addEventListener("change", () => updateNotificationSetting("absences", elements.absenceToggle.checked));
  elements.riskToggle.addEventListener("change", () => updateNotificationSetting("risk", elements.riskToggle.checked));
  elements.riskThreshold.addEventListener("input", () => {
    state.notifications.threshold = Number(elements.riskThreshold.value);
    saveState();
    syncNotificationControls();
    render();
  });

  elements.simulateGrade.addEventListener("click", openLaunchPanel);
  elements.closeLaunch.addEventListener("click", closeLaunchPanel);
  elements.confirmGrade.addEventListener("click", publishGrade);
  elements.simulateAbsence.addEventListener("click", publishAbsence);
  elements.resetDemo.addEventListener("click", resetDemo);
  elements.menuButton.addEventListener("click", openDrawer);
  elements.drawerBackdrop.addEventListener("click", closeDrawer);
  elements.searchButton.addEventListener("click", () => {
    elements.subjectSelect.focus();
    showToast("Escolha uma disciplina para atualizar o dashboard.");
  });

  document.querySelectorAll("[data-nav]").forEach((button) => {
    button.addEventListener("click", () => navigate(button.dataset.nav));
  });
}

function renderSubjects() {
  elements.subjectSelect.innerHTML = state.subjects
    .map((subject) => `<option value="${subject.id}">${subject.code} - ${subject.name}</option>`)
    .join("");
  elements.subjectSelect.value = state.selectedSubjectId;
}

function render() {
  const subject = getSelectedSubject();
  const absenceTotal = getAbsenceTotal(subject);
  const remaining = subject.absenceLimit - absenceTotal;
  const absencePercent = clamp((absenceTotal / subject.absenceLimit) * 100, 0, 100);
  const gradeSummary = calculateGradeSummary(subject);

  elements.absenceMetric.textContent = `${absenceTotal}/${subject.absenceLimit}`;
  elements.absenceRemaining.textContent = remaining > 0 ? `${remaining} restantes` : "limite estourado";
  elements.averageMetric.textContent = gradeSummary.averageLabel;
  elements.gradeStatus.textContent = gradeSummary.status;
  elements.requiredMetric.textContent = gradeSummary.requiredLabel;
  elements.requiredLabel.textContent = gradeSummary.requiredCaption;
  elements.classesMetric.textContent = `${subject.classes} aulas ministradas`;
  elements.absenceMeter.style.width = `${absencePercent}%`;
  elements.absenceMeter.style.background = getAbsenceColor(remaining);
  elements.absenceMessage.textContent = getAbsenceMessage(subject, absenceTotal, remaining);

  renderRiskBanner(subject, remaining);
  renderGrades(subject);
  renderFrequency(subject);
  renderFeed();
  renderAssessmentOptions(subject);
}

function renderRiskBanner(subject, remaining) {
  const isRisk = remaining <= state.notifications.threshold;
  elements.riskBanner.classList.toggle("visible", true);
  elements.riskBanner.classList.toggle("safe", !isRisk);

  if (remaining < 0) {
    elements.riskBanner.classList.remove("safe");
    elements.riskBanner.textContent = `${subject.code}: limite de faltas excedido em ${Math.abs(remaining)} falta(s). Procure a secretaria academica.`;
    return;
  }

  if (isRisk) {
    elements.riskBanner.textContent = `${subject.code}: voce esta perto do limite. Restam ${remaining} falta(s) antes de estourar.`;
    return;
  }

  elements.riskBanner.textContent = `${subject.code}: frequencia dentro do limite. Ainda restam ${remaining} falta(s).`;
}

function renderGrades(subject) {
  elements.gradesTable.innerHTML = subject.grades
    .map((grade) => {
      const status = grade.released ? "Lancada" : "Pendente";
      const statusClass = grade.released ? "released" : "pending";
      const value = grade.released ? grade.value : "-";
      return `
        <tr>
          <td>${grade.type}</td>
          <td>${value}</td>
          <td><span class="status-chip ${statusClass}">${status}</span></td>
        </tr>
      `;
    })
    .join("");
}

function renderFrequency(subject) {
  elements.frequencyTable.innerHTML = Object.entries(subject.absences)
    .map(([month, values]) => {
      return `
        <tr>
          <td>${month}</td>
          <td>${formatAbsence(values.pri)}</td>
          <td>${formatAbsence(values.lab)}</td>
          <td>${formatAbsence(values.jus)}</td>
        </tr>
      `;
    })
    .join("");
}

function renderFeed() {
  elements.notificationFeed.innerHTML = state.feed
    .slice(0, 6)
    .map((item) => {
      return `
        <li class="${item.type}">
          <strong>${item.title}</strong>
          <span>${item.body}</span>
          <span>${item.time}</span>
        </li>
      `;
    })
    .join("");
}

function renderAssessmentOptions(subject) {
  elements.assessmentSelect.innerHTML = subject.grades
    .map((grade) => `<option value="${grade.type}">${grade.type}</option>`)
    .join("");

  const nextPending = subject.grades.find((grade) => !grade.released) || subject.grades[0];
  if (nextPending) {
    elements.assessmentSelect.value = nextPending.type;
  }
}

async function enableNotifications() {
  state.notifications.enabled = true;

  if ("Notification" in window && Notification.permission === "default") {
    try {
      await Notification.requestPermission();
    } catch (error) {
      console.warn("Notification permission was not resolved.", error);
    }
  }

  saveState();
  syncNotificationControls();
  addFeedItem("system", "Notificacoes ativadas", "O app vai avisar sobre notas, faltas e risco de limite.");
  showToast("Notificacoes academicas ativadas.");
}

function syncNotificationControls() {
  elements.gradeToggle.checked = state.notifications.grades;
  elements.absenceToggle.checked = state.notifications.absences;
  elements.riskToggle.checked = state.notifications.risk;
  elements.riskThreshold.value = state.notifications.threshold;
  elements.thresholdValue.textContent = state.notifications.threshold;
  elements.permissionPanel.style.display = state.notifications.enabled ? "none" : "flex";
  elements.settingsPanel.classList.toggle("visible", state.notifications.enabled);
}

function updateNotificationSetting(key, value) {
  state.notifications[key] = value;
  saveState();
  syncNotificationControls();
  showToast("Preferencia de notificacao atualizada.");
}

function openLaunchPanel() {
  elements.launchPanel.hidden = false;
  elements.launchPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
  elements.gradeInput.focus();
}

function closeLaunchPanel() {
  elements.launchPanel.hidden = true;
}

function publishGrade() {
  const subject = getSelectedSubject();
  const assessmentType = elements.assessmentSelect.value;
  const value = clamp(Number(elements.gradeInput.value), 0, 100);
  const assessment = subject.grades.find((grade) => grade.type === assessmentType);

  if (!assessment || Number.isNaN(value)) {
    showToast("Informe uma avaliacao e uma nota valida.");
    return;
  }

  assessment.value = Math.round(value);
  assessment.released = true;
  closeLaunchPanel();
  saveState();
  render();

  const body = `${subject.code} - ${subject.name}: ${assessment.type} = ${assessment.value} pontos.`;
  addFeedItem("grade", `Nota ${assessment.type} publicada`, body);

  if (state.notifications.enabled && state.notifications.grades) {
    notify("Nota publicada", body, "grade");
  } else {
    showToast("Nota publicada no dashboard.");
  }
}

function publishAbsence() {
  const subject = getSelectedSubject();
  const currentMonth = subject.absences.Jun ? "Jun" : Object.keys(subject.absences).at(-1);
  subject.absences[currentMonth].pri += 1;

  const total = getAbsenceTotal(subject);
  const remaining = subject.absenceLimit - total;
  const body = `${subject.code} - ${subject.name}: 1 falta lancada em ${currentMonth}. Total atual: ${total}/${subject.absenceLimit}.`;

  saveState();
  render();
  addFeedItem("absence", "Falta lancada", body);

  if (state.notifications.enabled && state.notifications.absences) {
    notify("Falta lancada", body, "absence");
  } else {
    showToast("Falta registrada no dashboard.");
  }

  if (remaining <= state.notifications.threshold) {
    const riskBody = remaining >= 0
      ? `${subject.code}: restam ${remaining} falta(s) antes do limite.`
      : `${subject.code}: limite excedido em ${Math.abs(remaining)} falta(s).`;
    addFeedItem("risk", "Alerta de frequencia", riskBody);

    if (state.notifications.enabled && state.notifications.risk) {
      notify("Alerta de frequencia", riskBody, "risk");
    }
  }
}

function notify(title, body, type) {
  if ("Notification" in window && Notification.permission === "granted") {
    new Notification(`App Inatel - ${title}`, { body });
  }

  const prefix = type === "risk" ? "Alerta" : "Aviso";
  showToast(`${prefix}: ${body}`);
}

function addFeedItem(type, title, body) {
  state.feed.unshift({
    type,
    title,
    body,
    time: "Agora"
  });
  saveState();
  renderFeed();
}

function resetDemo() {
  localStorage.removeItem(storageKey);
  state = structuredClone(defaultState);
  renderSubjects();
  syncNotificationControls();
  render();
  showToast("Demonstracao reiniciada.");
}

function navigate(target) {
  closeDrawer();
  document.querySelectorAll("[data-nav]").forEach((button) => {
    button.classList.toggle("active", button.dataset.nav === target);
  });

  if (target === "notifications") {
    if (!state.notifications.enabled) {
      showToast("Ative as notificacoes para ajustar os avisos.");
    }
    elements.permissionPanel.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }

  if (target === "docs") {
    document.querySelector("#documentation").scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }

  elements.appContent.scrollTo({ top: 0, behavior: "smooth" });
}

function openDrawer() {
  elements.drawer.classList.add("open");
  elements.drawer.setAttribute("aria-hidden", "false");
  elements.drawerBackdrop.hidden = false;
}

function closeDrawer() {
  elements.drawer.classList.remove("open");
  elements.drawer.setAttribute("aria-hidden", "true");
  elements.drawerBackdrop.hidden = true;
}

function getSelectedSubject() {
  return state.subjects.find((subject) => subject.id === state.selectedSubjectId) || state.subjects[0];
}

function getAbsenceTotal(subject) {
  return Object.values(subject.absences).reduce((total, month) => {
    return total + Number(month.pri || 0) + Number(month.lab || 0);
  }, 0);
}

function calculateGradeSummary(subject) {
  const np1 = subject.grades.find((grade) => grade.type === "NP1");
  const np2 = subject.grades.find((grade) => grade.type === "NP2");
  const releasedGrades = subject.grades.filter((grade) => grade.released && typeof grade.value === "number");
  const average = releasedGrades.length
    ? releasedGrades.reduce((sum, grade) => sum + grade.value, 0) / releasedGrades.length
    : null;

  if (np1?.released && !np2?.released) {
    const required = clamp(120 - np1.value, 0, 100);
    return {
      averageLabel: formatNumber(average),
      status: "Aguardando NP2",
      requiredLabel: formatNumber(required),
      requiredCaption: "Na NP2"
    };
  }

  if (np1?.released && np2?.released) {
    const semesterAverage = (np1.value + np2.value) / 2;
    if (semesterAverage >= 60) {
      return {
        averageLabel: formatNumber(semesterAverage),
        status: "Aprovacao direta",
        requiredLabel: "0",
        requiredCaption: "Sem NP3"
      };
    }

    const np3Required = clamp(120 - semesterAverage, 0, 100);
    return {
      averageLabel: formatNumber(semesterAverage),
      status: "Precisa NP3",
      requiredLabel: formatNumber(np3Required),
      requiredCaption: "Na NP3"
    };
  }

  return {
    averageLabel: average === null ? "--" : formatNumber(average),
    status: releasedGrades.length ? "Parcial" : "Sem nota",
    requiredLabel: "--",
    requiredCaption: "Aguardando"
  };
}

function getAbsenceMessage(subject, total, remaining) {
  if (remaining < 0) {
    return `Total de ${total} faltas em ${subject.name}. O limite previsto era ${subject.absenceLimit}.`;
  }

  if (remaining <= state.notifications.threshold) {
    return `Total de ${total} faltas. O aviso de risco foi acionado porque restam ${remaining} falta(s).`;
  }

  return `Total de ${total} faltas. O limite previsto da disciplina e ${subject.absenceLimit}.`;
}

function getAbsenceColor(remaining) {
  if (remaining < 0) return "var(--danger)";
  if (remaining <= state.notifications.threshold) return "var(--warning)";
  return "var(--success)";
}

function formatAbsence(value) {
  return value ? String(value) : "-";
}

function formatNumber(value) {
  if (value === null || value === undefined) return "--";
  return Number.isInteger(value) ? String(value) : value.toFixed(1);
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function showToast(message) {
  window.clearTimeout(toastTimer);
  elements.toast.textContent = message;
  elements.toast.classList.add("visible");
  toastTimer = window.setTimeout(() => {
    elements.toast.classList.remove("visible");
  }, 3400);
}

function loadState() {
  try {
    const saved = localStorage.getItem(storageKey);
    return saved ? JSON.parse(saved) : structuredClone(defaultState);
  } catch (error) {
    console.warn("Could not load saved demo state.", error);
    return structuredClone(defaultState);
  }
}

function saveState() {
  localStorage.setItem(storageKey, JSON.stringify(state));
}

function updatePublishedLink() {
  if (!elements.publishedLink) return;

  const isPublished = window.location.hostname.endsWith("github.io");
  if (!isPublished) return;

  elements.publishedLink.href = window.location.href;
  elements.publishedLink.textContent = `Link GitHub Pages: ${window.location.href}`;
  elements.publishedLink.removeAttribute("aria-disabled");
}
