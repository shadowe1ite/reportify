from django import forms

class ReportForm(forms.Form):
    # Define common styles for input fields
    input_css_classes = "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 dark:text-gray-300 dark:bg-gray-900 leading-tight focus:outline-none focus:shadow-outline"
    label_css_classes = "block text-gray-700 dark:text-gray-300 font-bold mb-2"

    REPORT_FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
        ('html', 'HTML'),
        ('txt', 'TXT'),
    ]

    report_format = forms.ChoiceField(
        choices=REPORT_FORMAT_CHOICES,
        required=True,
        label='Report Format',
        widget=forms.Select(attrs={
            'class': input_css_classes,
        })
    )
    event_name = forms.CharField(
        max_length=100,
        required=True,
        label='Event Name',
        widget=forms.TextInput(attrs={
            'class': input_css_classes,
            'placeholder': 'TechNora 2025',
        })
    )
    description = forms.CharField(
        required=False,
        label='Description',
        widget=forms.Textarea(attrs={
            'class': input_css_classes,
            'placeholder': 'Tech Fest',
        })
    )
    event_date = forms.DateField(
        required=True,
        label='Event Date',
        widget=forms.DateInput(attrs={
            'class': input_css_classes,
            'type': 'date',
        })
    )
    organizer = forms.CharField(
        max_length=100,
        required=True,
        label='Organizer',
        widget=forms.TextInput(attrs={
            'class': input_css_classes,
            'placeholder': 'Department of Computer Applications',
        })
    )