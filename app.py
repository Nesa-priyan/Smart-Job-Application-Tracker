# This is my next new project on Smart Job Application tracker
# This project helps HR to Visit the candidates profile and their details there....by giving candidates information it will
# Store the info in database in Jobs.JSON file
#Lets start the project....
# importing the necessary libraries first...
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import json
import os
from fpdf import FPDF
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Define the path for the JSON file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
JOBS_FILE = os.path.join(BASE_DIR, 'jobs.json')  # Define the absolute path for jobs.json

UPLOAD_FOLDER = 'static/logos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Load job data from JSON file
def load_jobs():
    if not os.path.exists(JOBS_FILE):
        return []  # Create an empty jobs list if the file does not exist
    with open(JOBS_FILE, 'r') as f:
        return json.load(f)


# Save job data to JSON file
def save_jobs(jobs):
    with open(JOBS_FILE, 'w') as f:
        json.dump(jobs, f, indent=4)


# Home route
@app.route('/')
def index():
    jobs = load_jobs()
    return render_template('index.html', jobs=jobs)


# Add job route
@app.route('/add', methods=['GET', 'POST']) # Operations we do here GET and POST
def add_job():
    if request.method == 'POST':
        new_job = {
            "id": len(load_jobs()) + 1,
            "company": request.form['company'],
            "position": request.form['position'],
            "status": request.form['status'],
            "deadline": request.form['deadline']
        }
        jobs = load_jobs()
        jobs.append(new_job)
        save_jobs(jobs)
        flash('Job added successfully!', 'success')  # Flash success message
        return redirect(url_for('index'))
    return render_template('add_job.html')

# Delete job route
@app.route('/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    jobs = load_jobs()
    jobs = [job for job in jobs if job['id'] != job_id]  # Remove job with the matching ID
    save_jobs(jobs)
    return redirect(url_for('index'))

# Update job status route
@app.route('/update_status', methods=['POST'])
def update_status():
    job_id = request.form['job_id']  # Get the job ID from the form
    new_status = request.form['status']  # Get the new status from the form
    jobs = load_jobs()

    for job in jobs:
        if job['id'] == int(job_id):  # Find the job by ID
            job['status'] = new_status  # Update the status
            break

    save_jobs(jobs)  # Save the updated jobs list
    flash('Job status updated successfully!', 'success')  # Flash success message
    return redirect(url_for('index'))  # Redirect back to the index page


# Download as PDF
@app.route('/download_pdf') # We can also the download the updated or applied page in pdf format or in a csv format
def download_pdf():
    jobs = load_jobs()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for job in jobs:
        pdf.cell(200, 10, txt=f"{job['company']} - {job['position']} - {job['status']} - {job['deadline']}", ln=True)

    pdf_output = os.path.join(BASE_DIR, 'jobs.pdf')  # Save PDF in the same directory
    pdf.output(pdf_output)
    return send_file(pdf_output, as_attachment=True)


# Download as CSV
@app.route('/download_csv')
def download_csv():
    jobs = load_jobs()
    csv_output = os.path.join(BASE_DIR, 'jobs.csv')  # Save CSV in the same directory

    with open(csv_output, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company", "Position", "Status", "Deadline"])
        for job in jobs:
            writer.writerow([job['company'], job['position'], job['status'], job['deadline']])

    return send_file(csv_output, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
# Thank You>>>