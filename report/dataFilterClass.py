import pandas as pd
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from django.db.models import Q
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import logging
logger = logging.getLogger(__name__)




class PdfHeader:
    def __init__(self, model, request, date_field="date"):
        self.model = model
        self.request = request
        self.date_field = date_field
        self.queryset = None
        self._register_fonts()
        self._setup_styles()
        
    def _register_fonts(self):
        """Register custom fonts with fallback to standard fonts"""
        self.header_font = 'Helvetica-Bold'
        self.body_font = 'Helvetica'
        
        # Try to register Candara if available
        candara_paths = [
            'Candara.ttf',
            'Candarab.ttf',  # Bold variant
            os.path.join(os.path.dirname(__file__), 'static/fonts/Candara.ttf'),
            os.path.join(os.path.dirname(__file__), 'static/fonts/Candarab.ttf')
        ]
        
        for path in candara_paths:
            try:
                if 'Candarab.ttf' in path:
                    pdfmetrics.registerFont(TTFont('Candara-Bold', path))
                else:
                    pdfmetrics.registerFont(TTFont('Candara', path))
            except:
                continue
        
        # Check if we successfully registered both regular and bold
        if 'Candara' in pdfmetrics.getRegisteredFontNames() and 'Candara-Bold' in pdfmetrics.getRegisteredFontNames():
            self.header_font = 'Candara-Bold'
            self.body_font = 'Candara'
        else:
            # Fallback to Helvetica if we don't have both variants
            self.header_font = 'Helvetica-Bold'
            self.body_font = 'Helvetica'
    
    def _setup_styles(self):
        """Setup all the styles we'll need"""
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.styles.add(ParagraphStyle(
            name='ChurchHeader',
            fontSize=12,
            leading=14,
            alignment=1,  # Center
            fontName=self.header_font,
            spaceAfter=6
        ))
        
        self.styles.add(ParagraphStyle(
            name='InfoHeader',
            fontSize=9,
            leading=11,
            alignment=0,  # Left
            fontName=self.body_font,
            spaceAfter=6
        ))

    def draw_header(self, report_info):
        """Draw the standard church header"""
        header_content = []
        
        # Church header
        header_content.append(
            Paragraph("ACCRA CITY CONFERENCE OF SEVENTH-DAY ADVENTIST CHURCH", 
                     self.styles['ChurchHeader']))
        
        header_content.append(
            Paragraph(f"{report_info.get('church')} CHURCH, ACHIMOTA-DISTRICT", 
                      self.styles['ChurchHeader']))
        header_content.append(Spacer(1, 0.2*inch))
        
        
        # Report info in table form
        info_data = [
            [Paragraph("<font name='%s'><b>Report Period:</b></font>" % self.body_font, self.styles['InfoHeader']), 
             Paragraph(report_info.get('period', ''), self.styles['InfoHeader'])],
            [Paragraph("<font name='%s'><b>Department:</b></font>" % self.body_font, self.styles['InfoHeader']), 
             Paragraph(report_info.get('department', ''), self.styles['InfoHeader'])],
            [Paragraph("<font name='%s'><b>Elder in Charge:</b></font>" % self.body_font, self.styles['InfoHeader']), 
             Paragraph(report_info.get('elder', ''), self.styles['InfoHeader'])],
            [Paragraph("<font name='%s'><b>Leader:</b></font>" % self.body_font, self.styles['InfoHeader']), 
             Paragraph(report_info.get('leader', ''), self.styles['InfoHeader'])],
            [Paragraph("<font name='%s'><b>Members:</b></font>" % self.body_font, self.styles['InfoHeader']), 
             Paragraph(report_info.get('members', ''), self.styles['InfoHeader'])],
             [Paragraph("<font name='%s'><b>Reporter:</b></font>" % self.body_font, self.styles['InfoHeader']), 
             Paragraph(report_info.get('reporter', ''), self.styles['InfoHeader'])]
        ]
        
        # Create table with 2 columns
        info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        
        header_content.append(info_table)
        header_content.append(Spacer(1, 0.2*inch))
        header_content.append(Paragraph("<font name='%s'><b>Achieved</b></font>" % self.header_font))
        header_content.append(Spacer(1, 0.2*inch))
       
        
        return header_content



class PdfHeaderDist:
    def __init__(self, model, request, date_field="date"):
        self.model = model
        self.request = request
        self.date_field = date_field
        self.queryset = None
        self._register_fonts()
        self._setup_styles()
        
    def _register_fonts(self):
        """Register custom fonts with fallback to standard fonts"""
        self.header_font = 'Helvetica-Bold'
        self.body_font = 'Helvetica'
        
        # Try to register Candara if available
        candara_paths = [
            'Candara.ttf',
            'Candarab.ttf',  # Bold variant
            os.path.join(os.path.dirname(__file__), 'static/fonts/Candara.ttf'),
            os.path.join(os.path.dirname(__file__), 'static/fonts/Candarab.ttf')
        ]
        
        for path in candara_paths:
            try:
                if 'Candarab.ttf' in path:
                    pdfmetrics.registerFont(TTFont('Candara-Bold', path))
                else:
                    pdfmetrics.registerFont(TTFont('Candara', path))
            except:
                continue
        
        # Check if we successfully registered both regular and bold
        if 'Candara' in pdfmetrics.getRegisteredFontNames() and 'Candara-Bold' in pdfmetrics.getRegisteredFontNames():
            self.header_font = 'Candara-Bold'
            self.body_font = 'Candara'
        else:
            # Fallback to Helvetica if we don't have both variants
            self.header_font = 'Helvetica-Bold'
            self.body_font = 'Helvetica'
    
    def _setup_styles(self):
        """Setup all the styles we'll need"""
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.styles.add(ParagraphStyle(
            name='ChurchHeader',
            fontSize=12,
            leading=14,
            alignment=1,  # Center
            fontName=self.header_font,
            spaceAfter=6
        ))
        
        self.styles.add(ParagraphStyle(
            name='InfoHeader',
            fontSize=9,
            leading=11,
            alignment=0,  # Left
            fontName=self.body_font,
            spaceAfter=6
        ))

    def draw_header(self, report_info):
        """Draw the standard church header"""
        header_content = []
        
        # Church header
        header_content.append(
            Paragraph("ACCRA CITY CONFERENCE OF SEVENTH-DAY ADVENTIST CHURCH", 
                     self.styles['ChurchHeader']))
        
        header_content.append(
            Paragraph(f"{report_info.get('church')} CHURCH, ACHIMOTA-DISTRICT", 
                      self.styles['ChurchHeader']))
        header_content.append(Spacer(1, 0.2*inch))
        
        
        # Report info in table form
        info_data = [
            [Paragraph("<font name='%s'><b>Report Period:</b></font>" % self.body_font, self.styles['InfoHeader']), 
             Paragraph(report_info.get('period', ''), self.styles['InfoHeader'])],
            [Paragraph("<font name='%s'><b>Church:</b></font>" % self.body_font, self.styles['InfoHeader']), 
             Paragraph(report_info.get('church', ''), self.styles['InfoHeader'])],
            [Paragraph("<font name='%s'><b>Report:</b></font>" % self.body_font, self.styles['InfoHeader']), 
             Paragraph(report_info.get('report', ''), self.styles['InfoHeader'])],
            
            
        ]
        # Create table with 2 columns
        info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        
        header_content.append(info_table)
        header_content.append(Spacer(1, 0.3*inch))
       
        return header_content


class ChurchDataExporter:
    """
    Filters a model by church and date range.
    Exports data to Excel or PDF with professional formatting.
    """

    def __init__(self, model, date_field="date"):
        """
        :param model: Django model class
        :param date_field: The field name to use for date filtering (default is 'date')
        """
        self.model = model
        self.date_field = date_field
        self.queryset = None
        self._register_fonts()

    def _register_fonts(self):
        """Register custom fonts with fallback to standard fonts"""
        # Default to Helvetica
        self.header_font = 'Helvetica-Bold'
        self.body_font = 'Helvetica'
        
        # Try to register Candara if available
        candara_paths = [
            'Candara.ttf',
            'Candarab.ttf',  # Bold variant
            os.path.join(os.path.dirname(__file__), 'static/fonts/Candara.ttf'),
            os.path.join(os.path.dirname(__file__), 'static/fonts/Candarab.ttf')
        ]
        
        for path in candara_paths:
            try:
                if os.path.exists(path):
                    if 'Candarab.ttf' in path:
                        pdfmetrics.registerFont(TTFont('Candara-Bold', path))
                    else:
                        pdfmetrics.registerFont(TTFont('Candara', path))
            except Exception as e:
                logger.warning(f"Failed to register font {path}: {str(e)}")
                continue
        
        # Verify both regular and bold are registered before using Candara
        if ('Candara' in pdfmetrics.getRegisteredFontNames() and 
            'Candara-Bold' in pdfmetrics.getRegisteredFontNames()):
            self.header_font = 'Candara-Bold'
            self.body_font = 'Candara'
        else:
            # Fallback to Helvetica
            self.header_font = 'Helvetica-Bold'
            self.body_font = 'Helvetica'
            
            # Verify Helvetica is available
            if 'Helvetica' not in pdfmetrics.getRegisteredFontNames():
                logger.warning("Helvetica font not available - using Times-Roman")
                self.header_font = 'Times-Bold'
                self.body_font = 'Times-Roman'

    def filter_data(self, church=None, start_date=None, end_date=None):
        """
        Applies filters based on:
        - Church name (optional)
        - Date range (optional)
        
        :param church: Church name to filter by (partial match)
        :param start_date: Start date for range filter
        :param end_date: End date for range filter
        :return: Filtered queryset
        """
        query = Q()

        if church:
            query &= Q(church__icontains=church)

        if start_date and end_date:
            # Use dynamic date field
            date_filter = {f"{self.date_field}__range": [start_date, end_date]}
            query &= Q(**date_filter)

        self.queryset = self.model.objects.filter(query)
        return self.queryset

    def export_to_excel(self, fields, filename=None):
        """
        Exports filtered data to Excel with professional formatting.
        
        :param fields: List of fields to include in export
        :param filename: Optional output filename (default includes timestamp)
        :return: HttpResponse with Excel file
        """
        if not self.queryset:
            raise ValueError("No data filtered. Call filter_data() first.")

        if not filename:
            filename = f"church_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        df = pd.DataFrame(list(self.queryset.values(*fields)))
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, 
                       index=False, 
                       sheet_name='Church Data',
                       header=[field.upper() for field in fields])
        
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    def export_to_pdf(self, fields, filename=None, report_title="Church Data Report"):
        """
        Exports filtered data to PDF with professional formatting.
        
        :param fields: List of fields to include in export
        :param filename: Optional output filename (default includes timestamp)
        :param report_title: Title for the PDF report
        :return: HttpResponse with PDF file
        """
        if not self.queryset:
            raise ValueError("No data filtered. Call filter_data() first.")

        if not filename:
            filename = f"church_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        # Create custom styles with the registered fonts
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=styles['Heading2'],
            fontName=self.header_font,
            textColor=colors.HexColor('#333333'),
            alignment=1,  # Center
            spaceAfter=12
        ))
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['Normal'],
            fontName=self.body_font,
            textColor=colors.black,
            alignment=0,  # Left
            fontSize=10,
            leading=12
        ))
        styles.add(ParagraphStyle(
            name='TableHeader',
            parent=styles['Normal'],
            fontName=self.header_font,
            textColor=colors.white,
            fontSize=10,
            alignment=1  # Center
        ))
        
        elements = []
        
        # Add report title
        elements.append(Paragraph(report_title, styles['CustomHeader']))
        elements.append(Spacer(1, 0.25*inch))
        
        # Prepare table data
        data = []
        
        # Add table headers
        headers = [Paragraph(field.upper(), styles['TableHeader']) for field in fields]
        data.append(headers)
        
        # Add data rows
        for record in self.queryset:
            row = []
            for field in fields:
                value = str(getattr(record, field))
                row.append(Paragraph(value, styles['CustomBody']))
            data.append(row)
        
        # Create and style table
        table = Table(data, repeatRows=1)  # Repeat header on each page
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F81BD')),  # Header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), self.header_font),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D3D3D3')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        buffer.seek(0)
        return HttpResponse(
            buffer.read(),
            content_type='application/pdf',
            headers={'Content-Disposition': f'inline; filename="{filename}"'}
        )



class ReportDataExporter_error:
    """
    Filters a model by the user's church and department, plus optional date range.
    Exports data to Excel or PDF.
    """

    def __init__(self, model, request, date_field="date"):
        """
        :param model: Django model class
        :param request: HttpRequest object (to access user)
        :param date_field: The field name to use for date filtering (default is 'date')
        """
        self.model = model
        self.request = request
        self.date_field = date_field
        self.queryset = None
    
    def _register_fonts(self):
        """Register custom fonts with fallback to standard fonts"""
        self.header_font = 'Helvetica-Bold'
        self.body_font = 'Helvetica'
        
        # Try to register Candara if available
        candara_paths = [
            'Candara.ttf',
            'Candarab.ttf',  # Bold variant
            os.path.join(os.path.dirname(__file__), 'static/fonts/Candara.ttf'),
            os.path.join(os.path.dirname(__file__), 'static/fonts/Candarab.ttf')
        ]
        
        for path in candara_paths:
            try:
                if 'Candarab.ttf' in path:
                    pdfmetrics.registerFont(TTFont('Candara-Bold', path))
                else:
                    pdfmetrics.registerFont(TTFont('Candara', path))
            except:
                continue
        
        # Check if we successfully registered both regular and bold
        if 'Candara' in pdfmetrics.getRegisteredFontNames() and 'Candara-Bold' in pdfmetrics.getRegisteredFontNames():
            self.header_font = 'Candara-Bold'
            self.body_font = 'Candara'
        else:
            # Fallback to Helvetica if we don't have both variants
            self.header_font = 'Helvetica-Bold'
            self.body_font = 'Helvetic'        
            

    def filter_data(self, start_date=None, end_date=None):
        """
        Applies filters based on:
        - User's church (if the model has a church field)
        - User's department (if the model has a department field)
        - Optional date range (uses self.date_field)
        """
        query = Q()
        model_fields = [f.name for f in self.model._meta.get_fields()]

        # Filter by user's church, only if model has the 'church' field
        if 'church' in model_fields and hasattr(self.request.user, 'church'):
            query &= Q(church=self.request.user.church)

        # Filter by user's department, only if model has the 'department' field
        if 'department' in model_fields and hasattr(self.request.user, 'department'):
            user_dept = self.request.user.department
            if isinstance(user_dept, str):
                query &= Q(department=user_dept)
            else:
                query &= Q(department=user_dept)

        # Optional date range filter
        if start_date and end_date:
            if self.date_field in model_fields:
                date_filter = {f"{self.date_field}__range": [start_date, end_date]}
                query &= Q(**date_filter)

        self.queryset = self.model.objects.filter(query)
        print(self.queryset)
        return self.queryset



    def export_to_excel(self, fields, filename="department_data.xlsx"):
        """Exports filtered data to Excel."""
        if not self.queryset:
            raise ValueError("No data filtered. Call filter_data() first.")

        df = pd.DataFrame(list(self.queryset.values(*fields)))
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='department data')
        
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    
    
    
    def export_to_pdf(self, fields, filename="department_data.pdf", report_info=None):
        if self.queryset is None:
            raise ValueError("No data filtered. Call filter_data() first.")

        if not self.queryset.exists():
            raise ValueError("No data found for the selected filters.")

        if report_info is None:
            report_info = {
                'period': '',
                'department': '',
                'elder': '',
                'leader': '',
                'members': '',
                'church': ''
            }
    
    
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        # Initialize fonts first
        self._register_fonts()
        
        # Create custom styles with the registered fonts
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=styles['Heading4'],
            fontName=self.header_font,
            textColor=colors.black,
            alignment=1  # Center
        ))
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['Normal'],
            fontName=self.body_font,
            textColor=colors.black,
            alignment=1  # Center
        ))
        
        # Initialize header
        header = PdfHeader(None, doc)
        elements = header.draw_header(report_info)
        
        # Prepare table data
        data = []
        
        # Add table headers with custom style
        headers = [Paragraph(f"<font name='{self.header_font}'>{field.upper()}</font>", 
                            styles['CustomHeader']) for field in fields]
        data.append(headers)
        
        # Add data rows with custom style
        for record in self.queryset:
            row = []
            for field in fields:
                value = str(getattr(record, field))
                row.append(Paragraph(f"<font name='{self.body_font}'>{value}</font>", 
                                styles['CustomBody']))
            data.append(row)
        
        # Create and style table
        table = Table(data, repeatRows=1)  # Repeat header on each page
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F5F5F5')),  # Header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        
        non_achieved = Paragraph("<font name='%s'><b>Non Achieved</b></font>" % self.header_font)
      
        table.setStyle(style)
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        elements.append(non_achieved)
        elements.append(Spacer(1, 0.2*inch))
        
        # Build PDF
        doc.build(elements)
        
        buffer.seek(0)
        return HttpResponse(
            buffer.read(),
            content_type='application/pdf',
            headers={'Content-Disposition': f'inline; filename="{filename}"'}
        )



class ReportDataExporter:
    """
    Filters a model by the user's church and department, plus optional date range.
    Exports data to Excel or PDF.
    """

    def __init__(self, model, request, date_field="date"):
        """
        :param model: Django model class
        :param request: HttpRequest object (to access user)
        :param date_field: The field name to use for date filtering (default is 'date')
        """
        self.model = model
        self.request = request
        self.date_field = date_field
        self.queryset = None
    
    def _register_fonts(self):
        """Register custom fonts with fallback to standard fonts"""
        # Default to Helvetica
        self.header_font = 'Helvetica-Bold'
        self.body_font = 'Helvetica'
        
        # Try to register Candara if available
        candara_paths = [
            'Candara.ttf',
            'Candarab.ttf',  # Bold variant
            os.path.join(os.path.dirname(__file__), 'static/fonts/Candara.ttf'),
            os.path.join(os.path.dirname(__file__), 'static/fonts/Candarab.ttf')
        ]
        
        for path in candara_paths:
            try:
                if os.path.exists(path):
                    if 'Candarab.ttf' in path:
                        pdfmetrics.registerFont(TTFont('Candara-Bold', path))
                    else:
                        pdfmetrics.registerFont(TTFont('Candara', path))
            except Exception as e:
                logger.warning(f"Failed to register font {path}: {str(e)}")
                continue
        
        # Verify both regular and bold are registered before using Candara
        if ('Candara' in pdfmetrics.getRegisteredFontNames() and 
            'Candara-Bold' in pdfmetrics.getRegisteredFontNames()):
            self.header_font = 'Candara-Bold'
            self.body_font = 'Candara'
        else:
            # Fallback to Helvetica
            self.header_font = 'Helvetica-Bold'
            self.body_font = 'Helvetica'
            
            # Verify Helvetica is available
            if 'Helvetica' not in pdfmetrics.getRegisteredFontNames():
                logger.warning("Helvetica font not available - using Times-Roman")
                self.header_font = 'Times-Bold'
                self.body_font = 'Times-Roman'

    def filter_data(self, start_date=None, end_date=None):
        """
        Applies filters based on:
        - User's church (if the model has a church field)
        - User's department (if the model has a department field)
        - Optional date range (uses self.date_field)
        """
        query = Q()
        model_fields = [f.name for f in self.model._meta.get_fields()]

        # Filter by user's church, only if model has the 'church' field
        if 'church' in model_fields and hasattr(self.request.user, 'church'):
            query &= Q(church=self.request.user.church)

        # Filter by user's department, only if model has the 'department' field
        if 'department' in model_fields and hasattr(self.request.user, 'department'):
            user_dept = self.request.user.department
            if isinstance(user_dept, str):
                query &= Q(department=user_dept)
            else:
                query &= Q(department=user_dept)

        # Optional date range filter
        if start_date and end_date:
            if self.date_field in model_fields:
                date_filter = {f"{self.date_field}__range": [start_date, end_date]}
                query &= Q(**date_filter)

        self.queryset = self.model.objects.filter(query)
        return self.queryset


    def export_to_excel(self, fields, filename=None):
        """Exports filtered data to Excel."""
        if not self.queryset:
            raise ValueError("No data filtered. Call filter_data() first.")

        if not filename:
            filename = f"department_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        df = pd.DataFrame(list(self.queryset.values(*fields)))
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Department Data')
        
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    
    
    def export_to_pdf(self, fields, filename=None, report_info=None):
        """Exports filtered data to PDF with custom styling."""
        if self.queryset is None:
            raise ValueError("No data filtered. Call filter_data() first.")

        if not self.queryset.exists():
            raise ValueError("No data found for the selected filters.")

        if not filename:
            filename = f"department_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        if report_info is None:
            report_info = {
                'period': '',
                'department': '',
                'elder': '',
                'leader': '',
                'members': '',
                'church': ''
            }
    
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        # Initialize fonts first
        self._register_fonts()
        
        # Create custom styles with the registered fonts
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=styles['Heading4'],
            fontName=self.header_font,
            textColor=colors.black,
            alignment=1,  # Center
            spaceAfter=6
        ))
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['Normal'],
            fontName=self.body_font,
            textColor=colors.black,
            alignment=1,  # Center
            fontSize=9,
            leading=12
        ))
        
        # Initialize header
        header = PdfHeader(None, doc)
        elements = header.draw_header(report_info)
        
        # Prepare table data
        data = []
        
        # Add table headers with custom style
        headers = [Paragraph(f"<font name='{self.header_font}'>{field.upper()}</font>", 
                          styles['CustomHeader']) for field in fields]
        data.append(headers)
        
        # Add data rows with custom style
        for record in self.queryset:
            row = []
            for field in fields:
                value = str(getattr(record, field))
                row.append(Paragraph(f"<font name='{self.body_font}'>{value}</font>", 
                                styles['CustomBody']))
            data.append(row)
        
        # Create and style table
        table = Table(data, repeatRows=1)  # Repeat header on each page
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F5F5F5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        table.setStyle(style)
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add non-achieved section
        non_achieved = Paragraph(
            f"<font name='{self.header_font}'><b>Non Achieved</b></font>",
            styles['CustomHeader']
        )
        elements.append(non_achieved)
        elements.append(Spacer(1, 0.2*inch))
        
        # Build PDF
        doc.build(elements)
        
        buffer.seek(0)
        return HttpResponse(
            buffer.read(),
            content_type='application/pdf',
            headers={'Content-Disposition': f'inline; filename="{filename}"'}
        )


class ReportDataExporterDist:
    """
    Filters a model by the user's church and department, plus optional date range.
    Exports data to Excel or PDF.
    """

    def __init__(self, model, request, date_field="date"):
        """
        :param model: Django model class
        :param request: HttpRequest object (to access user)
        :param date_field: The field name to use for date filtering (default is 'date')
        """
        self.model = model
        self.request = request
        self.date_field = date_field
        self.queryset = None
    
    def _register_fonts(self):
        """Register custom fonts with fallback to standard fonts"""
        # Default to Helvetica
        self.header_font = 'Helvetica-Bold'
        self.body_font = 'Helvetica'
        
        # Try to register Candara if available
        candara_paths = [
            'Candara.ttf',
            'Candarab.ttf',  # Bold variant
            os.path.join(os.path.dirname(__file__), 'static/fonts/Candara.ttf'),
            os.path.join(os.path.dirname(__file__), 'static/fonts/Candarab.ttf')
        ]
        
        for path in candara_paths:
            try:
                if os.path.exists(path):
                    if 'Candarab.ttf' in path:
                        pdfmetrics.registerFont(TTFont('Candara-Bold', path))
                    else:
                        pdfmetrics.registerFont(TTFont('Candara', path))
            except Exception as e:
                logger.warning(f"Failed to register font {path}: {str(e)}")
                continue
        
        # Verify both regular and bold are registered before using Candara
        if ('Candara' in pdfmetrics.getRegisteredFontNames() and 
            'Candara-Bold' in pdfmetrics.getRegisteredFontNames()):
            self.header_font = 'Candara-Bold'
            self.body_font = 'Candara'
        else:
            # Fallback to Helvetica
            self.header_font = 'Helvetica-Bold'
            self.body_font = 'Helvetica'
            
            # Verify Helvetica is available
            if 'Helvetica' not in pdfmetrics.getRegisteredFontNames():
                logger.warning("Helvetica font not available - using Times-Roman")
                self.header_font = 'Times-Bold'
                self.body_font = 'Times-Roman'

    def filter_data(self, start_date=None, end_date=None):
        """
        Applies filters based on:
        - User's church (if the model has a church field)
        - User's department (if the model has a department field)
        - Optional date range (uses self.date_field)
        """
        query = Q()
        model_fields = [f.name for f in self.model._meta.get_fields()]

        # Filter by user's church, only if model has the 'church' field
        if 'church' in model_fields and hasattr(self.request.user, 'church'):
            query &= Q(church=self.request.user.church)

        # Optional date range filter
        if start_date and end_date:
            if self.date_field in model_fields:
                date_filter = {f"{self.date_field}__range": [start_date, end_date]}
                query &= Q(**date_filter)

        self.queryset = self.model.objects.filter(query)
        return self.queryset

    def export_to_excel(self, fields, filename=None):
        """Exports filtered data to Excel."""
        if not self.queryset:
            raise ValueError("No data filtered. Call filter_data() first.")

        if not filename:
            filename = f"report_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        df = pd.DataFrame(list(self.queryset.values(*fields)))
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Report Data')
        
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    def export_to_pdf(self, fields, filename=None, report_info=None):
        """Exports filtered data to PDF with custom styling."""
        if self.queryset is None:
            raise ValueError("No data filtered. Call filter_data() first.")

        if not self.queryset.exists():
            raise ValueError("No data found for the selected filters.")

        if not filename:
            filename = f"report_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        if report_info is None:
            report_info = {
                'period': '',
                'church': '',
                'report': '',
            }
    
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        # Initialize fonts first
        self._register_fonts()
        
        # Create custom styles with the registered fonts
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=styles['Heading4'],
            fontName=self.header_font,
            textColor=colors.black,
            alignment=1,  # Center
            spaceAfter=6
        ))
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['Normal'],
            fontName=self.body_font,
            textColor=colors.black,
            alignment=1,  # Center
            fontSize=9,
            leading=12
        ))
        
        # Initialize header
        header = PdfHeaderDist(None, doc)
        elements = header.draw_header(report_info)
        
        # Prepare table data
        data = []
        
        # Add table headers with custom style
        headers = [Paragraph(f"<font name='{self.header_font}'>{field.upper()}</font>", 
                          styles['CustomHeader']) for field in fields]
        data.append(headers)
        
        # Add data rows with custom style
        for record in self.queryset:
            row = []
            for field in fields:
                value = str(getattr(record, field))
                row.append(Paragraph(f"<font name='{self.body_font}'>{value}</font>", 
                                styles['CustomBody']))
            data.append(row)
        
        # Create and style table
        table = Table(data, repeatRows=1)  # Repeat header on each page
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F5F5F5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        table.setStyle(style)
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
      
        # Build PDF
        doc.build(elements)
        
        buffer.seek(0)
        return HttpResponse(
            buffer.read(),
            content_type='application/pdf',
            headers={'Content-Disposition': f'inline; filename="{filename}"'}
        )