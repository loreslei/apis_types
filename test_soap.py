import requests

soap_body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mus="http://example.com/music">
   <soapenv:Header/>
   <soapenv:Body>
      <mus:CreateUser>
         <name>Usuario SOAP</name>
         <age>40</age>
      </mus:CreateUser>
   </soapenv:Body>
</soapenv:Envelope>"""

try:
    r = requests.post('http://127.0.0.1:8004/', data=soap_body, headers={'Content-Type': 'text/xml'})
    print("STATUS", r.status_code)
    print("RESPONSE", r.text)
except Exception as e:
    print(e)
