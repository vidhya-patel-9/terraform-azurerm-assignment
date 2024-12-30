import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to load JSON data with error handling
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}.")
        return None

# Load JSON data
quality_gate = load_json('quality_gate.json')
issues = load_json('issues.json')
metrics = load_json('metrics.json')

# Check if all JSON data is loaded successfully
if not quality_gate or not issues or not metrics:
    print("Error: Failed to load JSON data.")
    exit(1)

# Create PDF report
def generate_pdf_report():
    c = canvas.Canvas("sonarqube_report.pdf", pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica", 16)
    c.drawString(100, height - 50, "SonarQube Quality Gate and Analysis Report")

    # Add Quality Gate Status
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 100, f"Quality Gate Status: {quality_gate['projectStatus']['status']}")

    # Add Conditions
    y_position = height - 130
    for condition in quality_gate['projectStatus']['conditions']:
        c.drawString(100, y_position, f"{condition['metricKey']}: {condition['actualValue']} ({condition['status']})")
        y_position -= 20

    # Add Issues
    c.drawString(100, y_position, "Issues:")
    y_position -= 20
    for issue in issues:
        c.drawString(100, y_position, f"{issue['severity']}: {issue['message']}")
        y_position -= 20

    # Add Metrics
    c.drawString(100, y_position, "Metrics:")
    y_position -= 20
    for measure in metrics['component']['measures']:
        c.drawString(100, y_position, f"{measure['metric']}: {measure['value']}")
        y_position -= 20

    # Save PDF
    c.save()
    print("PDF generated successfully.")

if __name__ == "__main__":
    generate_pdf_report()