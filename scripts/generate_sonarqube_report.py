import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# SonarQube server details from environment variables
SONAR_URL = os.getenv("SONAR_HOST_URL")
SONAR_API_TOKEN = os.getenv("SONAR_API_TOKEN")
PROJECT_KEY = os.getenv("SONAR_PROJECT_KEY")
print(f"SonarQube URL: {SONAR_URL}")
print(f"SONAR API TOKEN: {SONAR_API_TOKEN}")
print(f"PROJECT KEY: {PROJECT_KEY}")


# Function to fetch data from SonarQube
def fetch_sonar_data():
    headers = {
        'Authorization': f'Bearer {SONAR_API_TOKEN}'
    }

    # Fetch Quality Gate status
    quality_gate_url = f"{SONAR_URL}/api/qualitygates/project_status?projectKey={PROJECT_KEY}"
    quality_gate_response = requests.get(quality_gate_url, headers=headers)
    quality_gate_data = quality_gate_response.json()

    # Fetch Issues
    issues_url = f"{SONAR_URL}/api/issues/search?projectKeys={PROJECT_KEY}"
    issues_response = requests.get(issues_url, headers=headers)
    issues_data = issues_response.json()

    # Fetch Metrics
    metrics_url = f"{SONAR_URL}/api/measures/component?component={PROJECT_KEY}&metricKeys=bugs,vulnerabilities,code_smells,duplicated_lines_density,coverage"
    metrics_response = requests.get(metrics_url, headers=headers)
    metrics_data = metrics_response.json()

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
    c.drawString(100, height - 100, f"Quality Gate Status: {quality_gate_data['projectStatus']['status']}")

    # Add Conditions
    y_position = height - 130
    for condition in quality_gate_data['projectStatus']['conditions']:
        c.drawString(100, y_position, f"{condition['metricKey']}: {condition['actualValue']} ({condition['status']})")
        y_position -= 20

    # Add Issues
    c.drawString(100, y_position, "Issues:")
    y_position -= 20
    for issue in issues_data['issues']:
        c.drawString(100, y_position, f"{issue['severity']}: {issue['message']}")
        y_position -= 20

    # Add Metrics
    c.drawString(100, y_position, "Metrics:")
    y_position -= 20
    for measure in metrics_data['component']['measures']:
        c.drawString(100, y_position, f"{measure['metric']}: {measure['value']}")
        y_position -= 20

    # Save PDF
    c.save()
    print("PDF generated successfully.")

if __name__ == "__main__":
    quality_gate_data, issues_data, metrics_data = fetch_sonar_data()
    generate_pdf_report(quality_gate_data, issues_data, metrics_data)