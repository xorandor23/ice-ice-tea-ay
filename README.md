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
pip install -r requirements.txt
```
