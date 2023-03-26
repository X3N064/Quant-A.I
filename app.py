from flask import Flask, render_template
import subprocess
import requests
import json
import os
import sys
import time
import string

app = Flask(__name__)

def write_file(file_path, data):
    with open(file_path, 'w') as f:
        file_contents = f.write(str(data))
        f.close()
    return file_contents

# for reading files
def read_file(file_path):
    with open(file_path, 'r') as f:
        file_contents = f.read()
        f.close()
    return file_contents

#index page
@app.route("/")
def index():
    return render_template('index.html')

#result page
@app.route("/answer")
def result():
    openai()
    file_contents = read_file('result.txt')
    return render_template('result.html', file_contents=file_contents)

@app.route("/test")
def test():
    file_contents = read_file('result.txt')
    return render_template('page.html', file_contents=file_contents)

#for command
@app.route("/runcommand/<command>")
def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr

#response from chatgpt
def openai():
    url = "https://chatgpt-api.shn.hk/v1/"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": read_file('userinput.txt')}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        resp = response.json()
        response_data = json.loads(response.text)
        final =  response_data['choices'][0]['message']['content']
        write_file('answer_json.txt', final)
        write_file('result.txt', read_file('answer_json.txt'))

    except json.decoder.JSONDecodeError:
        result = 'The string does NOT contain valid JSON'
        write_file('result.txt', result)

#server starts
app.run(port=4444, debug=True)