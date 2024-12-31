import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# SonarQube server details from environment variables
SONAR_URL = os.getenv("SONAR_HOST_URL")
SONAR_API_TOKEN = os.getenv("SONAR_API_TOKEN")
PROJECT_KEY = os.getenv("SONAR_PROJECT_KEY")

if not SONAR_URL or not SONAR_API_TOKEN or not PROJECT_KEY:
    raise ValueError("Missing required environment variables: SONAR_HOST_URL, SONAR_API_TOKEN, SONAR_PROJECT_KEY")

# Function to fetch data from SonarQube
def fetch_sonar_data():
    headers = {
        'Authorization': f'Bearer {SONAR_API_TOKEN}'
    }

    # Fetch Quality Gate status
    quality_gate_url = f"{SONAR_URL}/api/qualitygates/project_status?projectKey={PROJECT_KEY}"
    quality_gate_response = requests.get(quality_gate_url, headers=headers)
    quality_gate_data = quality_gate_response.json()
    print("Quality Gate Data:", quality_gate_data)  # Debugging statement

    # Fetch Issues
    issues_url = f"{SONAR_URL}/api/issues/search?projectKeys={PROJECT_KEY}"
    issues_response = requests.get(issues_url, headers=headers)
    issues_data = issues_response.json()
    print("Issues Data:", issues_data)  # Debugging statement

    # Fetch Metrics
    metrics_url = f"{SONAR_URL}/api/measures/component?component={PROJECT_KEY}&metricKeys=bugs,vulnerabilities,code_smells,duplicated_lines_density,coverage"
    metrics_response = requests.get(metrics_url, headers=headers)
    metrics_data = metrics_response.json()
    print("Metrics Data:", metrics_data)  # Debugging statement

    return quality_gate_data, issues_data, metrics_data

# Function to generate PDF report
def generate_pdf_report(quality_gate_data, issues_data, metrics_data):
    c = canvas.Canvas("sonarqube_report.pdf", pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica", 16)
    c.drawString(100, height - 50, "SonarQube Quality Gate and Analysis Report")

    # Add Quality Gate Status
    c.setFont("Helvetica", 12)
    if 'projectStatus' in quality_gate_data:
        c.drawString(100, height - 100, f"Quality Gate Status: {quality_gate_data['projectStatus']['status']}")
    else:
        c.drawString(100, height - 100, "Quality Gate Status: Data not available")

    # Add Conditions
    y_position = height - 130
    if 'projectStatus' in quality_gate_data and 'conditions' in quality_gate_data['projectStatus']:
        for condition in quality_gate_data['projectStatus']['conditions']:
            c.drawString(100, y_position, f"{condition['metricKey']}: {condition['actualValue']} ({condition['status']})")
            y_position -= 20
    else:
        c.drawString(100, y_position, "Conditions: Data not available")
        y_position -= 20

    # Add Issues
    c.drawString(100, y_position, "Issues:")
    y_position -= 20
    if 'issues' in issues_data:
        for issue in issues_data['issues']:
            c.drawString(100, y_position, f"{issue['severity']}: {issue['message']}")
            y_position -= 20
    else:
        c.drawString(100, y_position, "Issues: Data not available")
        y_position -= 20

    # Add Metrics
    c.drawString(100, y_position, "Metrics:")
    y_position -= 20
    if 'component' in metrics_data and 'measures' in metrics_data['component']:
        for measure in metrics_data['component']['measures']:
            c.drawString(100, y_position, f"{measure['metric']}: {measure['value']}")
            y_position -= 20
    else:
        c.drawString(100, y_position, "Metrics: Data not available")
        y_position -= 20

    # Save PDF
    c.save()
    print("PDF generated successfully.")

if __name__ == "__main__":
    quality_gate_data, issues_data, metrics_data = fetch_sonar_data()
    generate_pdf_report(quality_gate_data, issues_data, metrics_data)