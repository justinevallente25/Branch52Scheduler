# controllers/pdf_manager.py

import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.lib.pagesizes import LETTER

from reportlab.lib.enums import TA_CENTER

from reportlab.lib import colors

from datetime import datetime


class PDFManager:

    def add_page_number(self, canvas, doc):

        canvas.saveState()

        page_number = canvas.getPageNumber()

        canvas.setFont("Helvetica", 9)

        canvas.drawCentredString(LETTER[0] / 2, 20, f"Page {page_number}")

        canvas.restoreState()

    def generate_today_schedule(self, schedules):

        now = datetime.now()

        folder = os.path.join("Print", now.strftime("%Y"), now.strftime("%B"))

        os.makedirs(folder, exist_ok=True)

        filename = os.path.join(folder, now.strftime("%Y-%m-%d_%I-%M-%S_%p") + ".pdf")

        doc = SimpleDocTemplate(
            filename,
            pagesize=LETTER,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=50,
        )

        styles = getSampleStyleSheet()

        header_style = ParagraphStyle(
            "header",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=11,
            leading=15,
        )

        cell_style = ParagraphStyle(
            "cell", parent=styles["Normal"], fontSize=9, leading=11
        )

        elements = []

        # ==========================
        # OFFICIAL LETTERHEAD
        # ==========================

        nlrc_logo = Image("assets/nlrclogo.png", width=70, height=70)

        dole_logo = Image("assets/dolelogo.png", width=70, height=70)

        letterhead_text = Paragraph(
            """

            Republic of the Philippines<br/>

            Department of Labor and Employment<br/>

            NATIONAL LABOR RELATIONS COMMISSION<br/>

            NATIONAL CAPITAL REGION<br/>

            ARBITRATION BRANCH NO. 52<br/>

            Quezon City

            """,
            header_style,
        )

        letterhead = Table(
            [[nlrc_logo, letterhead_text, dole_logo]], colWidths=[90, 300, 90]
        )

        letterhead.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )

        elements.append(letterhead)

        elements.append(Spacer(1, 10))

        elements.append(
            Paragraph(
                """

                Office of Labor Arbiter<br/>

                <b>CLARISSA G. BELTRAN-LERIOS</b>

                """,
                header_style,
            )
        )

        elements.append(Spacer(1, 10))

        elements.append(Paragraph("<b>SCHEDULE OF PROCEEDINGS</b>", header_style))

        elements.append(Spacer(1, 10))

        elements.append(
            Paragraph("Printed Date: " + now.strftime("%B %d, %Y"), header_style)
        )

        elements.append(Spacer(1, 20))

        # ==========================
        # TABLE DATA
        # ==========================

        data = [
            [
                Paragraph("<b>Date</b>", cell_style),
                Paragraph("<b>Complainant VS Respondent</b>", cell_style),
                Paragraph("<b>Time</b>", cell_style),
                Paragraph("<b>Type of Proceeding</b>", cell_style),
            ]
        ]

        for s in schedules:

            try:

                date = datetime.strptime(s.date, "%Y-%m-%d")

                formatted_date = (
                    date.strftime("%m-%d-%y") + "<br/>" + date.strftime("(%A)")
                )

            except:

                formatted_date = s.date

            data.append(
                [
                    Paragraph(formatted_date, cell_style),
                    Paragraph(f"{s.complainant} VS {s.respondent}", cell_style),
                    Paragraph(s.time if s.time else "-", cell_style),
                    Paragraph(s.proceeding if s.proceeding else "-", cell_style),
                ]
            )

        table = Table(data, repeatRows=1, colWidths=[90, 175, 70, 130])

        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )

        elements.append(table)

        doc.build(
            elements,
            onFirstPage=self.add_page_number,
            onLaterPages=self.add_page_number,
        )

        return filename
