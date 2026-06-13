#!/usr/bin/env python3
"""Generate a formatted PDF estimate from the quote provided by C.B. Fennell Ltd."""

from fpdf import FPDF

# ---- Brand / document constants -------------------------------------------------
NAVY = (24, 43, 77)
ACCENT = (191, 149, 63)   # muted gold
LIGHT = (242, 244, 248)
GREY = (110, 110, 110)
DARK = (40, 40, 40)

COMPANY = "C.B. FENNELL LTD."
TAGLINE = "Septic System Installation & Excavation"
CONTACT_NAME = "Buzzy"
PHONE = "(613) 813-1605"

ESTIMATE_NO = "CBF-2026-0613"
ESTIMATE_DATE = "June 13, 2026"
PROJECT = "Septic System Installation"

SUBTOTAL = 22855.00
HST_RATE = 0.13
HST = round(SUBTOTAL * HST_RATE, 2)
TOTAL = round(SUBTOTAL + HST, 2)

SCOPE = [
    ("1,500 gal septic tank", "Supply & install"),
    ("100 gal pump tank", "Supply & install"),
    ("180 ft raised filter media leaching bed", "Construct"),
    ("Equipment rental", "Included"),
    ("Labour", "Included"),
    ("Piping", "Supply & install"),
    ("Sand", "Supply & place"),
    ("Stone", "Supply & place"),
    ("Cover / final grading", "Included"),
]

NOTES = [
    "Rock breaking, if required, would be an additional charge.",
    "Does not include electrician fees.",
    "Does not include plumber fees.",
    "Taxes (HST) are additional to the quoted amount.",
]


class PDF(FPDF):
    def header(self):
        # Top banner
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 34, "F")
        self.set_fill_color(*ACCENT)
        self.rect(0, 34, 210, 1.5, "F")

        self.set_xy(15, 9)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 22)
        self.cell(0, 9, COMPANY, ln=1)

        self.set_x(15)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(210, 215, 225)
        self.cell(0, 6, TAGLINE, ln=1)

        # Right-aligned contact block in banner
        self.set_xy(120, 9)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(230, 233, 240)
        self.cell(75, 5, f"Contact: {CONTACT_NAME}", align="R", ln=1)
        self.set_x(120)
        self.cell(75, 5, f"Phone: {PHONE}", align="R", ln=1)

        self.set_y(46)

    def footer(self):
        self.set_y(-18)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.4)
        self.line(15, self.get_y(), 195, self.get_y())
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GREY)
        self.multi_cell(
            0, 4,
            "This document is a formatted transcription of a written quote provided by C.B. Fennell Ltd. "
            "The figures and scope above are as supplied and warranted by the contractor.",
            align="C",
        )


def section_title(pdf, text):
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 8, text, ln=1)
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.4)
    y = pdf.get_y()
    pdf.line(15, y, 60, y)
    pdf.ln(3)


def money(v):
    return f"${v:,.2f}"


pdf = PDF(format="A4")
pdf.set_auto_page_break(auto=True, margin=22)
pdf.set_margins(15, 46, 15)
pdf.add_page()

# ---- Title + meta block --------------------------------------------------------
pdf.set_font("Helvetica", "B", 18)
pdf.set_text_color(*DARK)
pdf.cell(0, 9, "ESTIMATE", ln=1)
pdf.ln(1)

# Meta box (right side)
meta_y = pdf.get_y()
pdf.set_fill_color(*LIGHT)
pdf.rect(120, meta_y, 75, 24, "F")
pdf.set_xy(124, meta_y + 3)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*NAVY)
pdf.cell(28, 6, "Estimate No.")
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*DARK)
pdf.cell(0, 6, ESTIMATE_NO, ln=1)
pdf.set_x(124)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*NAVY)
pdf.cell(28, 6, "Date")
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*DARK)
pdf.cell(0, 6, ESTIMATE_DATE, ln=1)
pdf.set_x(124)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*NAVY)
pdf.cell(28, 6, "Project")
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*DARK)
pdf.cell(0, 6, PROJECT, ln=1)

# Prepared for (left side)
pdf.set_xy(15, meta_y + 1)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*GREY)
pdf.cell(0, 5, "PREPARED FOR", ln=1)
pdf.set_x(15)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(*DARK)
pdf.cell(0, 6, "Property Owner / Prospective Purchasers", ln=1)
pdf.set_x(15)
pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(*GREY)
pdf.cell(0, 5, "Re: Proposed septic system installation", ln=1)

pdf.set_y(meta_y + 28)

# ---- Scope of work table -------------------------------------------------------
section_title(pdf, "Scope of Work")

# table header
pdf.set_font("Helvetica", "B", 10)
pdf.set_fill_color(*NAVY)
pdf.set_text_color(255, 255, 255)
pdf.cell(12, 8.5, "  #", border=0, fill=True)
pdf.cell(128, 8.5, "  Description", border=0, fill=True)
pdf.cell(40, 8.5, "Scope", border=0, fill=True, align="C", ln=1)

pdf.set_text_color(*DARK)
for i, (desc, scope) in enumerate(SCOPE, start=1):
    fill = (i % 2 == 0)
    if fill:
        pdf.set_fill_color(*LIGHT)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(12, 7.2, f"  {i}", border=0, fill=fill)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(128, 7.2, f"  {desc}", border=0, fill=fill)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GREY)
    pdf.cell(40, 7.2, scope, border=0, fill=fill, align="C", ln=1)
    pdf.set_text_color(*DARK)

pdf.ln(2)
pdf.set_font("Helvetica", "I", 8.5)
pdf.set_text_color(*GREY)
pdf.multi_cell(
    0, 4.5,
    "The amount below is an all-inclusive lump-sum price covering all items listed above "
    "(tank supply & installation, leaching bed, equipment, labour, piping, sand, stone, and cover).",
)
pdf.ln(3)

# ---- Pricing summary -----------------------------------------------------------
box_y = pdf.get_y()
pdf.set_fill_color(*LIGHT)
pdf.rect(110, box_y, 85, 34, "F")

def price_row(label, value, bold=False, color=DARK, size=10):
    pdf.set_x(112)
    pdf.set_font("Helvetica", "B" if bold else "", size)
    pdf.set_text_color(*color)
    pdf.cell(48, 8, label)
    pdf.cell(33, 8, money(value), align="R", ln=1)

pdf.set_y(box_y + 2)
price_row("Subtotal", SUBTOTAL)
price_row("Estimated HST (13%)", HST, color=GREY)
# divider
pdf.set_draw_color(*ACCENT)
pdf.line(112, pdf.get_y() + 1, 193, pdf.get_y() + 1)
pdf.ln(2)
pdf.set_x(110)
pdf.set_fill_color(*NAVY)
pdf.rect(110, pdf.get_y(), 85, 11, "F")
pdf.set_xy(112, pdf.get_y() + 1.5)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(255, 255, 255)
pdf.cell(48, 8, "TOTAL")
pdf.cell(33, 8, money(TOTAL), align="R", ln=1)

pdf.set_xy(15, box_y + 2)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*GREY)
pdf.multi_cell(
    88, 5,
    f"Quoted price: {money(SUBTOTAL)} plus taxes.\n\n"
    "HST is shown as an estimate at the Ontario rate of 13% for reference only.",
)

pdf.set_y(box_y + 33)

# ---- Notes & conditions --------------------------------------------------------
section_title(pdf, "Notes & Exclusions")
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(*DARK)
for n in NOTES:
    pdf.set_x(17)
    pdf.set_text_color(*ACCENT)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(5, 5.6, chr(149))  # bullet
    pdf.set_text_color(*DARK)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(170, 5.6, n)

pdf.ln(3)

# ---- Prepared by / acceptance --------------------------------------------------
blk_y = pdf.get_y()
pdf.set_draw_color(220, 223, 230)
pdf.set_line_width(0.3)
pdf.rect(15, blk_y, 180, 22)
pdf.line(105, blk_y, 105, blk_y + 22)

pdf.set_xy(19, blk_y + 3)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*NAVY)
pdf.cell(0, 5, "PREPARED BY", ln=1)
pdf.set_x(19)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 6, COMPANY, ln=1)
pdf.set_x(19)
pdf.set_font("Helvetica", "", 9)
pdf.cell(0, 5, f"{CONTACT_NAME}  -  {PHONE}", ln=1)

pdf.set_xy(109, blk_y + 3)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*NAVY)
pdf.cell(0, 5, "VALIDITY", ln=1)
pdf.set_x(109)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*DARK)
pdf.multi_cell(82, 5,
    "Figures as quoted by the contractor. Subject to the notes and "
    "exclusions above; final pricing confirmed by C.B. Fennell Ltd.")

pdf.output("CB_Fennell_Septic_Estimate.pdf")
print("Wrote CB_Fennell_Septic_Estimate.pdf")
