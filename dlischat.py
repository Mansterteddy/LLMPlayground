import os
import json
import requests
import sseclient
import gradio as gr

dlisbot_endpoint = os.environ["DLIS_CLIENT_ENDPOINT"]

def get_token():
    verify_endpoint = "https://login.microsoftonline.com/72f988bf-86f1-41af-91ab-2d7cd011db47/oauth2/v2.0/token"
    verify_scope = "e65e832b-d26e-4d59-be94-d261cd10435c/.default"

    verify_client_id = os.environ["DLIS_CLIENT_ID"]
    verify_client_secret = os.environ["DLIS_CLIENT_SECRET"]

    verify_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    verify_request = {
        "client_id": verify_client_id,
        "client_secret": verify_client_secret,
        "scope": verify_scope,
        "grant_type": "client_credentials"
    }
    
    verify_response = requests.post(verify_endpoint, data=verify_request, headers=verify_headers)
    verify_token = verify_response.json()["access_token"]

    return verify_token

def predict(message, history):
    try:
        #print("message: ", message)
        verify_token = get_token()
        response = requests.post(dlisbot_endpoint, headers={'Content-Type': 'application/json', "Authorization": "Bearer " + verify_token}, json=json.loads(message), stream=True)

        stream_res = ""
        client = sseclient.SSEClient(response)
        for event in client.events():
            stream_res += event.data
            yield stream_res

    except GeneratorExit:
        print("Generator Exit")
    finally:
        print("stream closed!")

gr.ChatInterface(predict, 
        examples=["{\"question\": \"what is deep learning?\"}", 
                    "{\"question\": \"what is dlis?\", \"func\": \"qa\"}", 
                    "{\"question\": \"Tell me the quota of T4 on DUB\", \"func\": \"capacity\"}"],
                
        ).queue().launch(server_name="0.0.0.0", server_port=7000)
