const subjects = [
  {
    id: "eng-software",
    name: "Engenharia de Software",
    code: "S05",
    classes: 40,
    absenceLimit: 10,
    absences: 5,
    grades: [
      { type: "NP1", value: 70, released: true },
      { type: "NP2", value: null, released: false },
      { type: "NP3", value: null, released: false }
    ],
    feed: [
      { type: "risk", title: "Alerta de faltas", body: "Você usou 5 de 10 faltas permitidas nesta matéria.", time: "Hoje, 09:10" },
      { type: "grade", title: "Nota NP1 lançada", body: "Engenharia de Software: NP1 publicada com 70 pontos.", time: "Ontem, 18:40" }
    ]
  },
  {
    id: "arquitetura",
    name: "Arquiteturas de Computadores",
    code: "C08 A",
    classes: 64,
    absenceLimit: 20,
    absences: 2,
    grades: [
      { type: "NP1", value: 75, released: true },
      { type: "NP2", value: null, released: false },
      { type: "NP3", value: null, released: false }
    ],
    feed: [
      { type: "grade", title: "Nota NP1 lançada", body: "Arquiteturas de Computadores: 75 pontos.", time: "Hoje, 08:42" }
    ]
  },
  {
    id: "sistemas",
    name: "Sistemas Distribuídos",
    code: "C216",
    classes: 38,
    absenceLimit: 15,
    absences: 13,
    grades: [
      { type: "LE1", value: 55, released: true },
      { type: "LE2", value: 88, released: true },
      { type: "LE3", value: 72, released: true },
      { type: "NP1", value: 72, released: true },
      { type: "NP2", value: null, released: false },
      { type: "NP3", value: null, released: false }
    ],
    feed: [
      { type: "absence", title: "Falta lançada", body: "Sistemas Distribuídos recebeu 1 falta em Jun.", time: "Ontem, 18:10" },
      { type: "risk", title: "Risco de limite", body: "Restam 2 faltas antes do limite previsto.", time: "Ontem, 18:10" }
    ]
  },
  {
    id: "topicos",
    name: "Tópicos Especiais II",
    code: "C318",
    classes: 42,
    absenceLimit: 10,
    absences: 2,
    grades: [
      { type: "ATV1", value: 100, released: true },
      { type: "ATV2", value: 85, released: true },
      { type: "ATV3", value: 85, released: true },
      { type: "NP1", value: 90, released: true },
      { type: "ATV4", value: 0, released: true },
      { type: "NP2", value: null, released: false }
    ],
    feed: [
      { type: "grade", title: "Atividades atualizadas", body: "ATV4 lançada no portal acadêmico.", time: "Seg, 14:05" }
    ]
  }
];

const storageKey = "inatel-student-dashboard-v2";
const state = loadState();
const els = {
  subjectSelect: document.querySelector("#subjectSelect"),
  notificationButton: document.querySelector("#notificationButton"),
  notificationModal: document.querySelector("#notificationModal"),
  closeNotificationModal: document.querySelector("#closeNotificationModal"),
  notificationStatus: document.querySelector("#notificationStatus"),
  enableNotifications: document.querySelector("#enableNotifications"),
  settingsCard: document.querySelector("#settingsCard"),
  gradeToggle: document.querySelector("#gradeToggle"),
  absenceToggle: document.querySelector("#absenceToggle"),
  riskToggle: document.querySelector("#riskToggle"),
  riskStrip: document.querySelector("#riskStrip"),
  absenceRatio: document.querySelector("#absenceRatio"),
  absenceDonut: document.querySelector("#absenceDonut"),
  classesCount: document.querySelector("#classesCount"),
  absenceCount: document.querySelector("#absenceCount"),
  totalLegend: document.querySelector("#totalLegend"),
  usedLegend: document.querySelector("#usedLegend"),
  limitLabel: document.querySelector("#limitLabel"),
  usedBar: document.querySelector("#usedBar"),
  limitMarker: document.querySelector("#limitMarker"),
  midScale: document.querySelector("#midScale"),
  limitScale: document.querySelector("#limitScale"),
  absenceMessage: document.querySelector("#absenceMessage"),
  averageBadge: document.querySelector("#averageBadge"),
  barChart: document.querySelector("#barChart"),
  gradesTable: document.querySelector("#gradesTable"),
  requiredGrade: document.querySelector("#requiredGrade"),
  requiredCaption: document.querySelector("#requiredCaption"),
  gradeMessage: document.querySelector("#gradeMessage"),
  notificationFeed: document.querySelector("#notificationFeed"),
  feedCount: document.querySelector("#feedCount"),
  toast: document.querySelector("#toast")
};

let toastTimer = null;

init();

function init() {
  subjects.forEach((subject) => {
    const option = document.createElement("option");
    option.value = subject.id;
    option.textContent = subject.name;
    els.subjectSelect.appendChild(option);
  });

  els.subjectSelect.value = state.selectedSubjectId;
  els.subjectSelect.addEventListener("change", () => {
    state.selectedSubjectId = els.subjectSelect.value;
    saveState();
    render();
  });

  els.enableNotifications.addEventListener("click", toggleNotifications);
  els.notificationButton.addEventListener("click", openNotificationModal);
  els.closeNotificationModal.addEventListener("click", closeNotificationModal);
  els.notificationModal.addEventListener("click", (event) => {
    if (event.target === els.notificationModal) closeNotificationModal();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !els.notificationModal.hidden) closeNotificationModal();
  });

  [els.gradeToggle, els.absenceToggle, els.riskToggle].forEach((input) => {
    input.addEventListener("change", () => {
      state.notifications[input.id.replace("Toggle", "")] = input.checked;
      saveState();
      render();
      showToast("Preferência atualizada.");
    });
  });

  syncControls();
  render();
}

async function toggleNotifications() {
  state.notifications.enabled = !state.notifications.enabled;
  saveState();
  syncControls();
  render();
  showToast(state.notifications.enabled
    ? "Notificações ativadas para notas, faltas e risco de limite."
    : "Notificações desativadas.");

  if (state.notifications.enabled && "Notification" in window && Notification.permission === "default") {
    try {
      await Notification.requestPermission();
    } catch (error) {
      console.warn("Permissão de notificação não concluída.", error);
    }
  }
}

function openNotificationModal() {
  els.notificationModal.hidden = false;
  els.closeNotificationModal.focus();
}

function closeNotificationModal() {
  els.notificationModal.hidden = true;
  els.notificationButton.focus();
}

function render() {
  const subject = getSubject();
  const remaining = subject.absenceLimit - subject.absences;
  const absencePercent = clamp(subject.absences / subject.absenceLimit, 0, 1);
  const gradeInfo = calculateGrades(subject);

  els.absenceRatio.textContent = `${subject.absences}/${subject.absenceLimit}`;
  els.classesCount.textContent = `${subject.classes} aulas`;
  els.absenceCount.textContent = `${subject.absences} faltas`;
  els.totalLegend.textContent = `Total de aulas (${subject.classes})`;
  els.usedLegend.textContent = `Aulas faltadas (${subject.absences})`;
  els.limitLabel.textContent = `Limite (${subject.absenceLimit} faltas)`;
  els.midScale.textContent = Math.floor(subject.absenceLimit / 2);
  els.limitScale.textContent = subject.absenceLimit;
  els.usedBar.style.width = `${absencePercent * 100}%`;
  els.limitMarker.style.left = "100%";
  els.absenceDonut.style.background = `conic-gradient(${absenceColor(remaining)} 0deg ${absencePercent * 360}deg, #dce6ef ${absencePercent * 360}deg 360deg)`;
  els.absenceMessage.textContent = remaining >= 0
    ? `Você usou ${subject.absences} de ${subject.absenceLimit} faltas (${Math.round(absencePercent * 100)}%). Restam ${remaining} falta(s).`
    : `Limite excedido em ${Math.abs(remaining)} falta(s). Procure a secretaria acadêmica.`;

  renderRisk(subject, remaining);
  renderBars(subject);
  renderTable(subject);
  renderTarget(gradeInfo);
  renderFeed(subject);
  syncControls();
}

function renderRisk(subject, remaining) {
  els.riskStrip.className = "risk-strip";

  if (remaining < 0) {
    els.riskStrip.classList.add("danger");
    els.riskStrip.textContent = `${subject.code}: limite de faltas excedido.`;
    return;
  }

  if (remaining <= 2) {
    els.riskStrip.textContent = `${subject.code}: você está perto do limite. Restam ${remaining} falta(s) antes de estourar.`;
    return;
  }

  els.riskStrip.classList.add("safe");
  els.riskStrip.textContent = `${subject.code}: frequência dentro do limite. Restam ${remaining} falta(s).`;
}

function renderBars(subject) {
  els.barChart.innerHTML = subject.grades.map((grade) => {
    const height = grade.released ? clamp(grade.value, 0, 100) : 8;
    const value = grade.released ? grade.value : "-";
    const pending = grade.released ? "" : " pending";
    return `
      <div class="bar-item">
        <span class="bar-column${pending}" style="height:${height}%"></span>
        <span class="bar-label"><strong>${value}</strong>${grade.type}</span>
      </div>
    `;
  }).join("");
}

function renderTable(subject) {
  els.gradesTable.innerHTML = subject.grades.map((grade) => {
    const value = grade.released ? grade.value : "-";
    const status = grade.released ? "Lançada" : "Pendente";
    const klass = grade.released ? "" : " pending";
    return `
      <tr>
        <td>${grade.type}</td>
        <td>${value}</td>
        <td><span class="chip${klass}">${status}</span></td>
      </tr>
    `;
  }).join("");
}

function renderTarget(info) {
  els.averageBadge.textContent = info.averageLabel;
  els.requiredGrade.textContent = info.required;
  els.requiredCaption.textContent = info.caption;
  els.gradeMessage.textContent = info.message;
}

function renderFeed(subject) {
  const filtered = subject.feed.filter((item) => {
    if (!state.notifications.enabled) return true;
    if (item.type === "grade") return state.notifications.grade;
    if (item.type === "absence") return state.notifications.absence;
    if (item.type === "risk") return state.notifications.risk;
    return true;
  });

  els.feedCount.textContent = filtered.length;
  els.notificationFeed.innerHTML = filtered.map((item) => `
    <li class="${item.type}">
      <strong>${item.title}</strong>
      <span>${item.body}</span>
      <span>${item.time}</span>
    </li>
  `).join("");
}

function syncControls() {
  els.notificationStatus.textContent = state.notifications.enabled ? "Ativadas" : "Desativadas";
  els.enableNotifications.textContent = state.notifications.enabled ? "Desativar" : "Ativar";
  els.enableNotifications.classList.toggle("secondary", state.notifications.enabled);
  els.gradeToggle.checked = state.notifications.grade;
  els.absenceToggle.checked = state.notifications.absence;
  els.riskToggle.checked = state.notifications.risk;
}

function calculateGrades(subject) {
  const np1 = subject.grades.find((grade) => grade.type === "NP1");
  const np2 = subject.grades.find((grade) => grade.type === "NP2");
  const released = subject.grades.filter((grade) => grade.released && Number.isFinite(grade.value));
  const average = released.length ? released.reduce((sum, grade) => sum + grade.value, 0) / released.length : null;

  if (np1?.released && !np2?.released) {
    const needed = clamp(120 - np1.value, 0, 100);
    return {
      averageLabel: `Média parcial: ${format(average)}`,
      required: format(needed),
      caption: "necessário na NP2",
      message: `Com NP1 = ${np1.value}, você precisa de ${format(needed)} na NP2 para atingir média 60.`
    };
  }

  if (np1?.released && np2?.released) {
    const semesterAverage = (np1.value + np2.value) / 2;
    if (semesterAverage >= 60) {
      return {
        averageLabel: `Média: ${format(semesterAverage)}`,
        required: "0",
        caption: "sem NP3",
        message: "A média atual permite aprovação direta nesta disciplina."
      };
    }

    const neededNp3 = clamp(120 - semesterAverage, 0, 100);
    return {
      averageLabel: `Média: ${format(semesterAverage)}`,
      required: format(neededNp3),
      caption: "necessário na NP3",
      message: `A média ficou abaixo de 60. A NP3 precisa ser pelo menos ${format(neededNp3)}.`
    };
  }

  return {
    averageLabel: average === null ? "Sem notas" : `Média parcial: ${format(average)}`,
    required: "--",
    caption: "aguardando avaliação",
    message: "A nota necessária será calculada quando a NP1 for lançada."
  };
}

function getSubject() {
  return subjects.find((subject) => subject.id === state.selectedSubjectId) || subjects[0];
}

function absenceColor(remaining) {
  if (remaining < 0) return "var(--danger)";
  if (remaining <= 2) return "var(--warning)";
  return "var(--success)";
}

function showToast(message) {
  clearTimeout(toastTimer);
  els.toast.textContent = message;
  els.toast.classList.add("visible");
  toastTimer = setTimeout(() => els.toast.classList.remove("visible"), 3200);
}

function loadState() {
  try {
    const saved = localStorage.getItem(storageKey);
    if (saved) return JSON.parse(saved);
  } catch (error) {
    console.warn("Estado local inválido.", error);
  }

  return {
    selectedSubjectId: "eng-software",
    notifications: {
      enabled: false,
      grade: true,
      absence: true,
      risk: true
    }
  };
}

function saveState() {
  localStorage.setItem(storageKey, JSON.stringify(state));
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function format(value) {
  if (value === null || value === undefined) return "--";
  return Number.isInteger(value) ? String(value) : value.toFixed(1);
}
