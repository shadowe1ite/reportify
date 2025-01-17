from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .forms import ReportForm
from crewai import Agent, Task, Crew, LLM
from fpdf import FPDF
from datetime import datetime
import os

class CollegeEventReportGenerator(FPDF):
    def __init__(self, event_name, event_date, organizer, description):
        super().__init__()
        self.event_name = event_name
        self.event_date = event_date
        self.organizer = organizer
        self.description = description
        self.llm = LLM(
            model="groq/mixtral-8x7b-32768",
            api_key=settings.GROQ_API_KEY,
            temperature=0.7
        )
        self.setup_agents()

    def setup_agents(self):
        self.researcher = Agent(
            role='Event Analyst',
            goal=f'Analyze and document the college event: {self.event_name}',
            backstory='Experienced event coordinator with expertise in academic event analysis',
            verbose=False,
            llm=self.llm
        )

        self.writer = Agent(
            role='Report Writer',
            goal='Create a formal event report with proper structure and academic tone',
            backstory='Professional report writer specialized in academic documentation',
            verbose=False,
            llm=self.llm
        )

    def create_tasks(self):
        research_task = Task(
            description=f'''Analyze the college event "{self.event_name}". 
                          Event Description: {self.description}
                          Include event objectives, participation, outcomes, and impact.''',
            expected_output="Detailed event analysis with key metrics and highlights",
            agent=self.researcher,
            async_execution=False
        )

        writing_task = Task(
            description='Create a formal event report including executive summary, event details, outcomes, and recommendations.',
            expected_output="Professional event report with structured sections",
            agent=self.writer,
            async_execution=False
        )

        return [research_task, writing_task]

    def header(self):
        # Set the template image as the background
        template_path = os.path.join('static', 'imgs', 'template.png')
        self.image(template_path, x=0, y=0, w=210, h=297)  # A4 dimensions in mm
        self.set_y(60)  # Adjust Y position to avoid overlapping with the image
        self.set_font("Helvetica", "B", 16)
        #self.cell(200, 10, txt="College Event Report", new_x="LMARGIN", new_y="NEXT", align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, 'C')

    def generate_pdf(self, content):
        self.add_page()
        
        self.set_font("Helvetica", size=12)
        
        # Event Details
        self.set_font("Helvetica", "B", 12)
        self.cell(200, 10, txt=f"Event: {self.event_name}", new_x="LMARGIN", new_y="NEXT", align='L')
        self.cell(200, 10, txt=f"Date: {self.event_date}", new_x="LMARGIN", new_y="NEXT", align='L')
        self.cell(200, 10, txt=f"Organizer: {self.organizer}", new_x="LMARGIN", new_y="NEXT", align='L')
        
        # Content
        self.set_font("Helvetica", size=12)
        self.multi_cell(0, 10, txt=str(content))
        
        # Signature Space
        self.ln(20)
        self.line(20, self.get_y(), 90, self.get_y())
        self.line(120, self.get_y(), 190, self.get_y())
        self.set_y(self.get_y() + 5)
        self.cell(90, 10, "Event Coordinator's Signature", 0, 0, 'L')
        self.cell(30, 10, "", 0, 0, 'C')
        self.cell(70, 10, "Dean's Signature", 0, 1, 'L')
        
        # Date
        self.ln(10)
        self.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d')}", 0, 1, 'R')
        
        filename = f"event_report_{self.event_name.lower().replace(' ', '_')}.pdf"
        filepath = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
        self.output(filepath)
        return filename

    def run(self):
        crew = Crew(
            agents=[self.researcher, self.writer],
            tasks=self.create_tasks(),
            max_rpm=29
        )
        
        result = crew.kickoff()
        filename = self.generate_pdf(result)
        return filename

def index(request):
    try:
        if request.method == "POST":
            form = ReportForm(request.POST)
            if form.is_valid():
                try:
                    # Get form data
                    event_name = form.cleaned_data['event_name']
                    event_date = form.cleaned_data['event_date']
                    organizer = form.cleaned_data['organizer']
                    description = form.cleaned_data['description']
                    report_format = form.cleaned_data['report_format']

                    # Create media directory if it doesn't exist
                    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'reports'), exist_ok=True)

                    # Generate report
                    report_gen = CollegeEventReportGenerator(
                        event_name=event_name,
                        event_date=event_date,
                        organizer=organizer,
                        description=description
                    )
                    
                    filename = report_gen.run()
                    filepath = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
                    
                    if os.path.exists(filepath):
                        with open(filepath, 'rb') as f:
                            response = HttpResponse(f.read(), content_type='application/pdf')
                            response['Content-Disposition'] = f'attachment; filename="{filename}"'
                            return response
                    else:
                        raise FileNotFoundError("Report file was not generated")
                    
                except Exception as e:
                    return JsonResponse({
                        'error': 'Failed to generate report',
                        'details': str(e)
                    }, status=500)
            else:
                return JsonResponse({
                    'error': 'Invalid form data',
                    'details': form.errors
                }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'Server error',
            'details': str(e)
        }, status=500)
    
    form = ReportForm()
    return render(request, 'reporter/index.html', {'form': form})
