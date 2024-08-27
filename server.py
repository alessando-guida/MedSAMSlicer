from flask import Flask, request, send_file, jsonify
import shutil
from pathlib import Path
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def welcome():
    return "All good, The Slicer server is reachable."

@app.route('/run_script', methods=['POST'])
def run_script():
    input_name = request.form.get('input')
    gts_name = request.form.get('gts')
    propagate = request.form.get('propagate')
    checkpoint = request.form.get('checkpoint')


    print(f"Received input_name: {input_name}")
    print(f"Received gts_name: {gts_name}")
    print(f"Received propagate: {propagate}")
    print(f"Received checkpoint: {checkpoint}")

    script_parameters = [
        'python',
        'infer_video_tiny_debug.py',
        '--img_path',
        input_name,
        '--gts_path',
        gts_name,
        '--propagate',
        propagate,
        '--checkpoint',
        checkpoint,
    ]
    
    print(f"Script parameters: {script_parameters}")
    
    process = subprocess.Popen(script_parameters, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()


    print(f"Script stdout: {stdout.decode('utf-8')}")
    print(f"Script stderr: {stderr.decode('utf-8')}")
    print(f"Script return code: {process.returncode}")

    #TODO: remove custom model?
    
    if process.returncode == 0:
        return f'Success: {stdout.decode("utf-8")}'
    else:
        return f'Error: {stderr.decode("utf-8")}'

@app.route('/download_file', methods=['GET'])
def download_file():
    output_name = request.form.get('output')
    
    print(f"Received output_name: {output_name}")

    try:
        response = send_file(output_name, as_attachment=True)
        print(f"File {output_name} sent successfully")
        return response
    except Exception as e:
        print(f"Error sending file {output_name}: {e}")
        return str(e)
    
    #return send_file(output_name, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():    
    file = request.files['file']

    if file:
        print(f"Received file: {file.filename}")
        file.save(file.filename)
        print(f"File saved: {file.filename}")
        return 'File uploaded successfully'
    else:
        print("No file received")


@app.route('/testme', methods=['POST'])
def testme():
    print("you pressed the button ")
    return "Button pressed!"

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(host='127.0.0.1', port=8080, debug=True)
