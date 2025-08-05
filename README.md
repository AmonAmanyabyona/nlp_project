# text_and_speech_nlp_system
This repo is for an AI assistant system that enables the user to interact with the quotes database using text or audio input 

if you want to test the whole interaction all you need is an .env file where you will store GITHUB_TOKEN=........... and then run the streamlit full_flowV1.py for the gpt-4o model.
Then for the llama model to see the interaction run the streamlit ui full_flowV2.py for it to work smoothly you will need to set the api key as below:
client = together.Together(api_key="")  in the script named second_model.py

If these steps are followed the system should be able to work smoothly
