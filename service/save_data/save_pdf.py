from fpdf import FPDF


class OperationsPDF(FPDF):
    def __init__(self, orientation, unit, format_, font_cache_dir="DEPRECATED"):
        super().__init__(orientation, unit, format_, font_cache_dir)
        self.header_text = ''
        self.title_text = ''
        self.body_text = []

    def header(self) -> None:
        """Elements for the header in PDF"""
        self.image('service/save_data/images/bank.png', 15, 8, 30)
        self.set_font('helvetica', 'B', 20)
        title_w = self.get_string_width(self.header_text) + 6
        doc_w = self.w
        self.set_x((doc_w - title_w) / 2)
        self.cell(title_w, 25, self.header_text, border=0, ln=1, align='C', fill=False)
        self.ln(10)

    def footer(self) -> None:
        """Elements for the footer in PDF"""
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(169, 169, 169)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def print_title(self) -> None:
        """Elements for the title in PDF"""
        self.set_font('helvetica', 'BI', 16)
        title_w = self.get_string_width(self.title_text) + 6
        doc_w = self.w
        self.set_x((doc_w - title_w) / 2)
        self.cell(title_w, 5, self.title_text, border=0, ln=1, align='C', fill=False)
        self.ln()

    def print_body(self) -> None:
        """Print the required text in the body section"""
        self.set_font('helvetica', 'I', 12)
        body_ = self.get_one_line()
        for x in body_:
            title_w = self.get_string_width(x) + 6
            doc_w = self.w
            self.set_x((doc_w - title_w) / 2)
            self.cell(title_w, 5, x, border=0, ln=1, align='C', fill=False)
        self.ln()

    def get_one_line(self) -> iter:
        """Get one line and return to body section as generator"""
        for x in self.body_text:
            for y in range(0, 8):
                match y:
                    case 0:
                        yield f'Payment: {x[0]}'
                    case 1:
                        yield f'Payout: {x[1]}'
                    case 2:
                        yield f'Transaction name: {x[2]}'
                    case 3:
                        yield f'Transaction time: {x[3]}'
                    case 4:
                        yield f'Recipient name: {x[4]}'
                    case 5:
                        yield f'Bank account number: {x[5]}'
                    case 6:
                        yield f'Transfer amount: {x[6]}'
                    case 7:
                        yield ' '
