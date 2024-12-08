import urllib.request
import pypdf
import re

def fetch_pdf_from_url(url, save_path):
    """
    Fetch the PDF data from the provided URL and save it locally.
    :param url: URL of the PDF file
    :param save_path: Path to save the downloaded file
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        with open(save_path, 'wb') as file:
            file.write(response.read())

def extract_incidents_from_pdf(pdf_path):
    """
    Extract incident data from a NormanPD-style PDF.
    :param pdf_path: Path to the PDF file
    :return: List of incident dictionaries
    """
    reader = pypdf.PdfReader(pdf_path)
    content = ""

    for page in reader.pages:
        content += page.extract_text(extraction_mode="layout")

    lines = content.splitlines()[3:-1]  # Remove headers/footers if needed
    incidents_data = []
    lines = [line for line in lines if line.strip()]

    for line in lines:
        process_incident_line(line, incidents_data)

    return incidents_data

def process_incident_line(line, incidents_data):
    """
    Process a single line of incident data.
    :param line: Line from the PDF
    :param incidents_data: List to append processed data
    """
    date_pattern = r'\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}'
    dates_found = re.finditer(date_pattern, line)
    parts = []

    if dates_found:
        split_positions = [match.start() for match in dates_found]
        parts = [line[start:end].strip() for start, end in zip(split_positions, split_positions[1:] + [len(line)])]

    cleaned_parts = [part for part in parts if part]

    for segment in cleaned_parts:
        split_segment = re.split(r"\s{4,}", segment)
        valid_fields = [field.strip() for field in split_segment if field.strip()]
        extract_fields(valid_fields, incidents_data)

def extract_fields(valid_fields, incidents_data):
    """
    Extract fields from a processed segment and append to the incidents list.
    :param valid_fields: List of cleaned fields
    :param incidents_data: List to append incident data
    """
    if len(valid_fields) == 5:
        extracted_data = {
            "DateTime": valid_fields[0],
            "IncidentNumber": valid_fields[1],
            "Location": valid_fields[2],
            "Nature": valid_fields[3],
            "IncidentType": valid_fields[4]
        }
        incidents_data.append(extracted_data)
