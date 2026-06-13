from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).parent
TEMPLATE = ROOT / "Exemplo de Formato de Entrega.pdf"
OUTPUT = ROOT / "Entrega_S05_App_Inatel_Notificacoes.pdf"
SCREENSHOT = Path.home() / "AppData" / "Local" / "Temp" / "inatel-dashboard-final-v2.png"
ASSET_DIR = ROOT / "delivery_assets"
CLASS_DIAGRAM_IMAGE = ASSET_DIR / "class-diagram.png"
POPUP_WIREFRAME_IMAGE = ASSET_DIR / "popup-wireframe.png"
DASHBOARD_WIREFRAME_PDF = ROOT / "wireframe (1).pdf"
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


def draw_image_fit(c, image_path, x, y, w, h):
    image = ImageReader(str(image_path))
    iw, ih = image.getSize()
    scale = min(w / iw, h / ih)
    draw_w = iw * scale
    draw_h = ih * scale
    draw_x = x + (w - draw_w) / 2
    draw_y = y + (h - draw_h) / 2
    c.drawImage(image, draw_x, draw_y, width=draw_w, height=draw_h, mask="auto")


def page1(c):
    clear(c, 45, 45, 390, 330)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(58, 342, "Nome: Gustavo Gago Lopes")
    c.drawString(58, 320, "Matrícula: 413")

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
    clear(c, 30, 18, 660, 355)
    heading(c, "Fluxo de Informação (Diagrama de Classes)", 42, 370)
    if CLASS_DIAGRAM_IMAGE.exists():
        draw_image_fit(c, CLASS_DIAGRAM_IMAGE, 36, 35, 648, 318)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(42, 22, "Diagrama UML simplificado: o aluno consulta dados acadêmicos, configura preferências e recebe notificações.")


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
    paragraph(c, "A entrega usa dois wireframes: a dashboard principal da matéria e o popup de notificações acadêmicas.", 52, 294, 98, 10, 14, MUTED)
    c.setStrokeColor(LINE)
    c.setFillColor(colors.white)
    c.roundRect(58, 47, 192, 228, 6, fill=1, stroke=1)
    c.roundRect(286, 47, 376, 228, 6, fill=1, stroke=1)
    if POPUP_WIREFRAME_IMAGE.exists():
        draw_image_fit(c, POPUP_WIREFRAME_IMAGE, 296, 58, 356, 206)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(154, 34, "1. Dashboard da matéria")
    c.drawCentredString(474, 34, "2. Popup de notificações")


def make_overlay(page_number):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=PAGE_SIZE)
    [page1, page2, page3, page4, page5][page_number](c)
    c.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def merge_pdf_page_fit(target_page, source_path, x, y, w, h):
    if not source_path.exists():
        return
    source_page = PdfReader(str(source_path)).pages[0]
    source_w = float(source_page.mediabox.width)
    source_h = float(source_page.mediabox.height)
    scale = min(w / source_w, h / source_h)
    draw_w = source_w * scale
    draw_h = source_h * scale
    tx = x + (w - draw_w) / 2
    ty = y + (h - draw_h) / 2
    transform = Transformation().scale(scale).translate(tx, ty)
    target_page.merge_transformed_page(source_page, transform, expand=False)


def main():
    reader = PdfReader(str(TEMPLATE))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        page.merge_page(make_overlay(i))
        if i == 4:
            merge_pdf_page_fit(page, DASHBOARD_WIREFRAME_PDF, 64, 53, 180, 216)
        writer.add_page(page)
    with OUTPUT.open("wb") as f:
        writer.write(f)
    print(OUTPUT)


if __name__ == "__main__":
    main()
