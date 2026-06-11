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
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 8, y + h - 18, title)
    c.setFont("Helvetica", 7.6)
    c.setFillColor(MUTED)
    line_y = y + h - 32
    for field in fields:
        c.drawString(x + 8, line_y, field)
        line_y -= 10
    c.setFillColor(BLUE)
    for method in methods:
        c.drawString(x + 8, line_y, method)
        line_y -= 10


def page4(c):
    clear(c, 42, 55, 640, 280)
    heading(c, "Fluxo de Informação (Diagrama de Classes)", 42, 328)
    boxes = [
        (42, 236, "Aluno", ["- matrícula", "- nome"], ["+ escolherMateria()"], BLUE),
        (188, 236, "DashboardMateria", ["- matériaAtual", "- statusAcadêmico"], ["+ atualizarDashboard()"], BLUE),
        (334, 236, "Disciplina", ["- nome", "- professor"], ["+ consultarNotas()", "+ consultarFrequência()"], BLUE),
        (480, 236, "PreferênciaNotificação", ["- notaAtiva", "- faltaAtiva", "- riscoAtivo"], ["+ alterarPreferência()"], WARN),
        (42, 126, "Frequência", ["- aulas", "- faltas", "- limite"], ["+ calcularRestantes()"], BLUE),
        (188, 126, "Avaliação", ["- tipo", "- nota", "- lançada"], ["+ registrarNota()"], BLUE),
        (334, 126, "CalculadoraAcadêmica", ["- médiaAprovação = 60"], ["+ calcularNotaNecessária()", "+ verificarRiscoFalta()"], BLUE),
        (480, 126, "ServiçoNotificação", ["- canais", "- mensagens"], ["+ avisarNota()", "+ avisarFalta()", "+ avisarRisco()"], WARN),
    ]
    for x, y, title, fields, methods, accent in boxes:
        class_box(c, x, y, 126, 84, title, fields, methods, accent)
    c.setStrokeColor(MUTED)
    c.setLineWidth(1)
    for x1, y1, x2, y2 in [(168, 278, 188, 278), (314, 278, 334, 278), (460, 278, 480, 278), (397, 236, 397, 210), (251, 236, 251, 210), (105, 236, 105, 210), (460, 168, 480, 168)]:
        c.line(x1, y1, x2, y2)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(42, 88, "Regra: faltas restantes = limite - faltas. Se restarem 2 ou menos, o aviso de risco é exibido.")
    c.drawString(42, 74, "Regra: com NP1 = 70, a dashboard calcula NP2 necessária = 50 para média final 60.")


def draw_phone_wire(c, x, y, title, alert=False):
    c.setFillColor(colors.white)
    c.setStrokeColor(INK)
    c.roundRect(x, y, 150, 230, 20, fill=1, stroke=1)
    c.setFillColor(BLUE)
    c.rect(x + 1, y + 190, 148, 25, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + 75, y + 174, title)
    c.setStrokeColor(LINE)
    c.roundRect(x + 14, y + 150, 122, 26, 4, fill=0, stroke=1)
    c.roundRect(x + 14, y + 75, 122, 66, 4, fill=0, stroke=1)
    c.roundRect(x + 14, y + 30, 122, 34, 4, fill=0, stroke=1)
    c.setFillColor(WARN if alert else BLUE)
    c.rect(x + 24, y + 88, 22, 42, fill=1, stroke=0)
    c.rect(x + 54, y + 108, 22, 22, fill=1, stroke=0)
    c.rect(x + 84, y + 96, 22, 34, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7)
    c.drawCentredString(x + 75, y + 12, title)


def page5(c):
    clear(c, 52, 80, 620, 245)
    heading(c, "Wireframes", 52, 320)
    paragraph(c, "A sequência representa o percurso do aluno: abrir a dashboard, ativar notificações e receber feedback de risco/notas/faltas.", 52, 294, 96, 11, 15, MUTED)
    draw_phone_wire(c, 72, 45, "Dashboard")
    draw_phone_wire(c, 285, 45, "Configuração")
    draw_phone_wire(c, 498, 45, "Feedback", alert=True)


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
