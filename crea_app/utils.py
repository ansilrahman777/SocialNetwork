import http.client
import json
from django.conf import settings
from urllib.parse import quote

def send_otp_via_sms(mobile, otp):
    print("FUNCTION CALLED")
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = str(settings.MSG91_API_KEY)  
    headers = {'content-type': "application/json"}
    
    if not mobile.startswith("91"):
        mobile = "91" + mobile  

    otp_encoded = quote(otp)
    message_encoded = quote(f'Your otp is {otp}')
    mobile_encoded = quote(mobile)
    authkey_encoded = quote(authkey)
    sender_encoded = quote(settings.MSG91_SMS_SENDER_ID)
    template_id_encoded = quote(settings.MSG91_SMS_TEMPLATE_ID)  
   
    url = f"http://control.msg91.com/api/sendotp.php?otp={otp_encoded}&message={message_encoded}&mobile={mobile_encoded}&authkey={authkey_encoded}&sender={sender_encoded}&template_id={template_id_encoded}&country=91"
   
    # print(f"Request URL: {url}")

    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read().decode()  
    
    # print(f"Response from MSG91: {data}")

    return json.loads(data)  









