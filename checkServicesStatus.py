from flask import Flask
import requests
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup


app = Flask(__name__)

def googleStatus():
    html_page = urlopen("https://www.google.com/appsstatus/dashboard/")
    html_text = html_page.read()#.decode("utf-8")

    soup = BeautifulSoup(html_text, "html.parser")
    htmlString = ""

    for table in soup.find_all("table"):
        tbody = table.find("tbody")
        for tr in tbody.find_all("tr"):
            for td in tr.find_all("td"):
                if td["class"][0] == "product-name":
                    print(td.text)
                    htmlString += "<tr><td>" + td.text + "</td>"
                else:
                    if td.find("div") != None:
                        div = td.find("div")
                        a = div.find("a")
                        print(a["class"][1])
                        if a["class"][1] == 'available':
                            htmlString += "<td>" + "&#9989;" + "</td></tr>"
    
    return htmlString

def psStatus():
    response = requests.get("https://status.playstation.com/data/statuses/region/SCEE.json")

    jsonResponse = json.loads(response.text)

    countries = jsonResponse["countries"]

    htmlString = ""

    for country in countries:
        if country["countryCode"] == "IT":
            for service in country["services"]:
                print(service["serviceName"])
                htmlString += "<tr><td>" + service["serviceName"] + "</td>"
                if not service["status"]:
                    htmlString += "<td>" + "&#9989;" + "</td></tr>"

    return htmlString

def xboxStatus():
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    response = requests.get("https://xnotify.xboxlive.com/servicestatusv6/IT/it-IT", headers=headers)

    print(response.text)

    jsonResponse = json.loads(response.text)

    htmlString = ""

    coreServices = jsonResponse["CoreServices"] 
    titles = jsonResponse["Titles"] 
    for service in coreServices:
        print(service["Name"])
        htmlString += "<tr><td>" + service["Name"] + "</td>"
        print(service["Status"]["Name"])
        if service["Status"]["Name"] == 'None':
            htmlString += "<td>" + "&#9989;" + "</td></tr>"
        elif service["Status"]["Name"] == 'Impacted':
            htmlString += "<td>" + "Impacted" + "</td></tr>"
    for title in titles:
        htmlString += "<tr><td>" + title["Name"] + "</td>"
        print(title["Status"]["Name"])
        if title["Status"]["Name"] == 'None':
            htmlString += "<td>" + "&#9989;" + "</td></tr>"
        elif title["Status"]["Name"] == 'Impacted':
            htmlString += "<td>" + "⚠️" + "</td></tr>"

    return htmlString


@app.route("/")
def hello_world():
    return """<!DOCTYPE html>
    <html>
    <head>
    <style>
    table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 50%;
    margin-left: auto;
    margin-right: auto;
    }

    td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 5px;
    }

    tr:nth-child(even) {
    background-color: #dddddd;
    }

    .active, .collapsible:hover {
    background-color: #555;
    }

    .collapsible {
        background-color: #777;
        color: white;
        cursor: pointer;
        padding: 18px;
        width: 100%;
        border: none;
        text-align: center;
        outline: none;
    }

    .content {
    padding: 0 18px;
    display: none;
    overflow: hidden;
    background-color: #f1f1f1;
    }
    </style>
    </head>
    <body>

    <button type="button" class="collapsible">PSN Services Status</button>
    <div class="content">
    <table>
    """ + psStatus() + """
    </table>
    </div>
    <br>

    <button type="button" class="collapsible">Xbox Services Status</button>

    <div class="content">
    <table>
    """ + xboxStatus() + """
    </table>
    </div>
    <br>

    <button type="button" class="collapsible">Google Services Status</button>

    <div class="content">
    <table>
    """ + googleStatus() + """
    </table>
    </div>
    <br>

    <script>
    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
        content.style.display = "none";
        } else {
        content.style.display = "block";
        }
    });
    }
    </script>

    </body>
    </html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0")

