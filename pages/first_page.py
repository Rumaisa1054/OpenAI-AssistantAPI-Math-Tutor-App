
import os
import streamlit as st
from openai import OpenAI
import time
from clarifai.client.model import Model
from clarifai.client.input import Inputs
from clarifai.client.auth import create_stub
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.client.user import User
from clarifai.modules.css import ClarifaiStreamlitCSS
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from google.protobuf import json_format, timestamp_pb2

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

st.title("Clarifai NextGen Nexus App")

message_before = {}
def main1(client,prompt):
    assistantId = "asst_oteb8wHPdYVFZgkAGZP6fp3l"
    '''
    #Creating an assistant
        assistant = client.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a personal math tutor. Write and run code to answer math questions.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo"
    )
    '''
    #Creating a Thread
    thread = client.beta.threads.create()
    
    #Adding message to Thread
    message = client.beta.threads.messages.create(
          thread_id=thread.id,
          role="user",
          content= prompt
    )
    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistantId,
        instructions="Please address the user as Rumaisa."
    )
    
    #Run and Displaying the response
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    while run.status != "completed":
      time.sleep(1)
      run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
      )
                
    # Retrieving the messages
    messages = client.beta.threads.messages.list(
      thread_id=thread.id
    )
    arr = {}
    for message in reversed(messages.data):
        message_before[message.role] = message.content[0].text.value
        arr[message.role] = message.content[0].text.value
    return arr
  
def main():

    Question = st.text_input("Enter a Question")
    with st.sidebar:
        #Clarifai credentials
        st.subheader( "Add your OPENAI API")
        api = st.text_input("CLARIFAI PAT " , type='password')
    if not api:
        st.warning("PLease enter api to continue")
    else:
        client = OpenAI(api_key=api)
        if (st.button("Submit")) and Question:
          with st.spinner("Wait... Generating response..."):
            response = main1(client, Question)
        if response:
            for role, message in response.items():
                st.markdown(message)
if __name__ == '__main__':
    main()
