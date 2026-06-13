from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).parent
TEMPLATE = ROOT / "Exemplo de Formato de Entrega.pdf"
OUTPUT = ROOT / "Entrega_S05_App_Inatel_Notificacoes.pdf"
SCREENSHOT = Path.home() / "AppData" / "Local" / "Temp" / "inatel-dashboard-final-v2.png"
PAGE_SIZE = landscape((405, 720))
WIDTH, HEIGHT = PAGE_SIZE
BLUE = colors.HexColor("#006db7")
INK = colors.HexColor("#111827")
MUTED = colors.HexColor("#4b5563")
LINE = colors.HexColor("#d0d7de")
SOFT = colors.HexColor("#eef6fc")
WARN = colors.HexColor("#d98218")


def wrap_text(text, max_chars):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(c, text, x, y, width_chars=76, size=12, leading=16, color=INK):
    c.setFillColor(color)
    c.setFont("Helvetica", size)
    cursor = y
    for line in wrap_text(text, width_chars):
        c.drawString(x, cursor, line)
        cursor -= leading
    return cursor


def heading(c, text, x, y):
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(x, y, text)


def small_label(c, text, x, y):
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x, y, text.upper())


def clear(c, x, y, w, h):
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.white)
    c.rect(x, y, w, h, fill=1, stroke=0)


def page1(c):
    clear(c, 45, 45, 390, 330)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(58, 342, "Nome: Gustavo Gago Lopes")
    c.drawString(58, 320, "Matrícula: __________________")

    small_label(c, "Justificativa da funcionalidade", 58, 280)
    text = (
        "A funcionalidade permite que o aluno acompanhe notas, faltas e risco de "
        "limite em uma dashboard no App Inatel. A proposta reduz a necessidade de "
        "conferência manual, apresenta nota necessária para aprovação e envia avisos "
        "quando uma nota ou falta é lançada pelo professor."
    )
    y = paragraph(c, text, 58, 264, width_chars=54, size=11, leading=14)
    small_label(c, "Link GitHub Pages", 58, y - 8)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(58, y - 24, "https://gustavogago.github.io/S05/")
    c.linkURL("https://gustavogago.github.io/S05/", (58, y - 28, 260, y - 14), relative=0)

    if SCREENSHOT.exists():
        clear(c, 467, 69, 124, 258)
        c.drawImage(ImageReader(str(SCREENSHOT)), 467, 69, width=124, height=258, preserveAspectRatio=True, mask="auto")


def page2(c):
    clear(c, 80, 125, 560, 170)
    heading(c, "User Story", 80, 300)
    story = (
        "Como aluno do Inatel, quero visualizar uma dashboard da matéria com minhas "
        "notas, faltas e preferências de notificação, para acompanhar minha situação "
        "acadêmica e ser avisado quando uma nota sair, quando uma falta for lançada "
        "ou quando eu estiver perto de estourar o limite de faltas."
    )
    y = paragraph(c, story, 80, 272, width_chars=86, size=13, leading=18)
    small_label(c, "Persona", 80, y - 10)
    paragraph(c, "Aluno do Inatel que acompanha o desempenho acadêmico pelo celular.", 80, y - 26, 86, 11, 15, MUTED)
    small_label(c, "Meta", 80, y - 56)
    paragraph(c, "Consultar notas/faltas e ativar avisos acadêmicos por disciplina.", 80, y - 72, 86, 11, 15, MUTED)


def page3(c):
    clear(c, 58, 70, 610, 250)
    heading(c, "Análise da Tarefa", 58, 318)
    rows = [
        ("0", "Acompanhar situação acadêmica", "Plano: 1 > 2 > 3 > 4 > 5. O aluno usa a dashboard para entender notas, faltas e próximos riscos."),
        ("1", "Abrir o App Inatel", "O aluno acessa sua conta e entra na área acadêmica."),
        ("2", "Selecionar Dashboard da Matéria", "A opção fica visível no menu do app e abre a tela de acompanhamento."),
        ("3", "Escolher a matéria", "O seletor carrega as disciplinas do semestre e atualiza todos os gráficos."),
        ("4", "Ativar notificações", "O aluno escolhe avisos de nota lançada, falta lançada e risco de limite."),
        ("5", "Interpretar feedback", "O sistema mostra donut de faltas, régua de limite, gráfico de notas, nota necessária e feed de avisos.")
    ]
    x, y = 58, 286
    for number, title, body in rows:
        c.setFillColor(SOFT)
        c.setStrokeColor(LINE)
        c.roundRect(x, y - 31, 610, 38, 5, fill=1, stroke=1)
        c.setFillColor(BLUE)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x + 12, y - 12, number)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 42, y - 8, title)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8.5)
        c.drawString(x + 42, y - 22, body[:118])
        y -= 42


def class_box(c, x, y, w, h, title, fields, methods, accent=BLUE):
    c.setFillColor(colors.white)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 5, fill=1, stroke=1)
    c.setFillColor(accent)
    c.rect(x, y + h - 5, w, 5, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 8.4)
    c.drawString(x + 8, y + h - 18, title)
    c.setFont("Helvetica", 7.1)
    c.setFillColor(MUTED)
    line_y = y + h - 31
    for field in fields:
        c.drawString(x + 8, line_y, field)
        line_y -= 8.5
    c.setFillColor(BLUE)
    for method in methods:
        c.drawString(x + 8, line_y, method)
        line_y -= 8.5


def page4(c):
    clear(c, 38, 32, 648, 304)
    heading(c, "Fluxo de Informação (Diagrama de Classes)", 42, 328)
    boxes = [
        (42, 229, "Aluno", ["- matrícula", "- nome"], ["+ escolherMateria()", "+ configurarAvisos()"], BLUE),
        (267, 229, "DashboardMateria", ["- disciplinaAtual", "- resumoStatus"], ["+ carregarDados()", "+ exibirIndicadores()"], BLUE),
        (492, 229, "Disciplina", ["- código", "- nome", "- professor"], ["+ obterNotas()", "+ obterFrequência()"], BLUE),
        (42, 148, "PreferênciaNotificação", ["- notaAtiva", "- faltaAtiva", "- riscoAtivo"], ["+ ativar()", "+ desativar()"], WARN),
        (267, 148, "ServiçoNotificação", ["- preferências", "- feedAvisos"], ["+ filtrarAvisos()", "+ exibirAviso()"], WARN),
        (492, 148, "EventoAcadêmico", ["- tipoEvento", "- mensagem", "- data"], ["+ gerarAviso()"], WARN),
        (42, 67, "Frequência", ["- aulasMinistradas", "- faltas", "- limite"], ["+ calcularRestantes()"], BLUE),
        (267, 67, "Avaliação", ["- tipo", "- nota", "- lançadaEm"], ["+ exibirStatus()"], BLUE),
        (492, 67, "CalculadoraAcadêmica", ["- médiaAprovação = 60", "- limiteFaltas"], ["+ calcularNP2()", "+ verificarRisco()"], BLUE),
    ]
    c.setStrokeColor(MUTED)
    c.setLineWidth(1)
    for x1, y1, x2, y2 in [
        (216, 263, 267, 263),
        (441, 263, 492, 263),
        (129, 229, 129, 216),
        (129, 216, 129, 148),
        (441, 182, 492, 182),
        (579, 216, 579, 148),
        (354, 229, 354, 135),
        (354, 135, 129, 135),
        (354, 135, 354, 67),
        (354, 135, 579, 135),
        (579, 135, 579, 67),
    ]:
        c.line(x1, y1, x2, y2)
    for x, y, title, fields, methods, accent in boxes:
        class_box(c, x, y, 174, 68, title, fields, methods, accent)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(42, 45, "Validação: o aluno não registra nota/falta; ele consulta Avaliação/Frequência, altera preferências e recebe EventoAcadêmico como aviso.")
    c.drawString(42, 33, "Regras: faltas restantes = limite - faltas; com NP1 = 70, a dashboard calcula NP2 necessária = 50 para média 60.")


def wire_text(c, x, y, text, size=6.4, color=MUTED, bold=False):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    c.drawString(x, y, text)


def draw_phone_frame(c, x, y, title):
    c.setFillColor(colors.white)
    c.setStrokeColor(INK)
    c.roundRect(x, y, 156, 242, 20, fill=1, stroke=1)
    c.setFillColor(BLUE)
    c.rect(x + 1, y + 205, 154, 24, fill=1, stroke=0)
    wire_text(c, x + 14, y + 212, "Inatel", 7.2, colors.white, True)
    c.setFillColor(colors.white)
    c.circle(x + 136, y + 217, 4, fill=1, stroke=0)
    wire_text(c, x + 12, y - 12, title, 7, MUTED, True)


def draw_dashboard_wire(c, x, y):
    draw_phone_frame(c, x, y, "1. Dashboard da matéria")
    wire_text(c, x + 14, y + 190, "Matéria selecionada", 6.5, INK, True)
    c.setStrokeColor(LINE)
    c.roundRect(x + 14, y + 174, 128, 13, 3, fill=0, stroke=1)
    wire_text(c, x + 20, y + 178, "S05 - IHC", 5.8)
    c.setFillColor(colors.HexColor("#fff4e6"))
    c.roundRect(x + 14, y + 147, 128, 18, 4, fill=1, stroke=0)
    wire_text(c, x + 20, y + 153, "Alerta: restam 2 faltas", 5.8, WARN, True)
    c.setStrokeColor(LINE)
    c.setFillColor(colors.white)
    c.roundRect(x + 14, y + 86, 60, 52, 5, fill=1, stroke=1)
    c.roundRect(x + 82, y + 86, 60, 52, 5, fill=1, stroke=1)
    wire_text(c, x + 20, y + 124, "Faltas", 5.8, INK, True)
    c.setFillColor(WARN)
    c.circle(x + 44, y + 106, 12, fill=0, stroke=1)
    wire_text(c, x + 35, y + 103, "10/12", 5.2, WARN, True)
    wire_text(c, x + 88, y + 124, "Notas", 5.8, INK, True)
    c.setFillColor(BLUE)
    c.rect(x + 92, y + 98, 9, 22, fill=1, stroke=0)
    c.rect(x + 106, y + 106, 9, 14, fill=1, stroke=0)
    c.rect(x + 120, y + 94, 9, 26, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.roundRect(x + 14, y + 45, 128, 26, 5, fill=0, stroke=1)
    wire_text(c, x + 20, y + 58, "NP2 necessária: 50", 6, INK, True)


def draw_modal_wire(c, x, y):
    draw_phone_frame(c, x, y, "2. Popup de notificações")
    c.setFillColor(colors.HexColor("#f3f4f6"))
    c.roundRect(x + 14, y + 170, 128, 16, 3, fill=1, stroke=0)
    c.roundRect(x + 14, y + 132, 128, 26, 4, fill=1, stroke=0)
    c.roundRect(x + 14, y + 92, 128, 26, 4, fill=1, stroke=0)
    c.roundRect(x + 14, y + 52, 128, 26, 4, fill=1, stroke=0)
    c.setFillColor(colors.Color(0.07, 0.12, 0.2, alpha=0.22))
    c.roundRect(x + 1, y + 1, 154, 228, 20, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setStrokeColor(INK)
    c.roundRect(x + 22, y + 55, 112, 134, 7, fill=1, stroke=1)
    wire_text(c, x + 34, y + 174, "Notificações", 7, INK, True)
    wire_text(c, x + 34, y + 158, "Status: Ativadas", 5.8)
    c.setFillColor(BLUE)
    c.roundRect(x + 84, y + 151, 38, 13, 4, fill=1, stroke=0)
    wire_text(c, x + 93, y + 155, "Desativar", 4.9, colors.white, True)
    for i, label in enumerate(["Nova nota", "Nova falta", "Risco de falta"]):
        row_y = y + 126 - i * 25
        c.setStrokeColor(LINE)
        c.line(x + 34, row_y - 6, x + 122, row_y - 6)
        c.setFillColor(WARN if i == 2 else BLUE)
        c.circle(x + 40, row_y, 4, fill=1, stroke=0)
        wire_text(c, x + 50, row_y - 2, label, 5.9, INK)


def draw_feedback_wire(c, x, y):
    draw_phone_frame(c, x, y, "3. Feedback e decisão")
    c.setFillColor(colors.HexColor("#fff4e6"))
    c.roundRect(x + 14, y + 172, 128, 25, 5, fill=1, stroke=0)
    wire_text(c, x + 22, y + 185, "Risco de faltas", 6.1, WARN, True)
    wire_text(c, x + 22, y + 176, "Revise presença nas próximas aulas", 4.9, WARN)
    c.setStrokeColor(LINE)
    c.setFillColor(colors.white)
    c.roundRect(x + 14, y + 112, 128, 46, 5, fill=1, stroke=1)
    wire_text(c, x + 22, y + 143, "Avisos recentes", 6.1, INK, True)
    wire_text(c, x + 22, y + 130, "Nota de NP1 lançada: 70", 5.4)
    wire_text(c, x + 22, y + 118, "Falta registrada em S05", 5.4)
    c.roundRect(x + 14, y + 55, 128, 42, 5, fill=1, stroke=1)
    wire_text(c, x + 22, y + 82, "Próxima ação", 6.1, INK, True)
    wire_text(c, x + 22, y + 70, "Consultar faltas e planejar presença", 5.2)
    c.setFillColor(BLUE)
    c.roundRect(x + 22, y + 58, 64, 12, 4, fill=1, stroke=0)
    wire_text(c, x + 31, y + 61.5, "Abrir matéria", 4.8, colors.white, True)


def page5(c):
    clear(c, 42, 35, 642, 300)
    heading(c, "Wireframes", 52, 320)
    paragraph(c, "Fluxo de baixa fidelidade alinhado à tela final: consulta da matéria, popup de notificações e feedback visual quando houver risco ou novo aviso.", 52, 294, 98, 10, 14, MUTED)
    draw_dashboard_wire(c, 58, 34)
    draw_modal_wire(c, 282, 34)
    draw_feedback_wire(c, 506, 34)
    c.setStrokeColor(MUTED)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8)
    c.line(222, 156, 260, 156)
    c.drawString(232, 162, "abre")
    c.line(446, 156, 484, 156)
    c.drawString(454, 162, "avisa")


def make_overlay(page_number):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=PAGE_SIZE)
    [page1, page2, page3, page4, page5][page_number](c)
    c.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def main():
    reader = PdfReader(str(TEMPLATE))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        page.merge_page(make_overlay(i))
        writer.add_page(page)
    with OUTPUT.open("wb") as f:
        writer.write(f)
    print(OUTPUT)


if __name__ == "__main__":
    main()
