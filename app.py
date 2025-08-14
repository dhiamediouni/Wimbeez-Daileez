import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



# Imports
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain
import nest_asyncio
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_core.output_parsers import StrOutputParser
import gradio as gr

logger.debug("Imports completed.")

# Load the CSV file
loader = CSVLoader(file_path='HR_consultant_inputs.csv')
logger.debug("CSVLoader initialized.")
data = loader.load()
logger.debug(f"CSV data loaded: {data[0]}")

# Split the documents into smaller chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
logger.debug("CharacterTextSplitter initialized.")
chunked_docs = text_splitter.split_documents(data)
logger.debug(f"Documents split into chunks: {chunked_docs[:2]}")  # Log only the first two chunks for brevity

# Using HuggingFace embeddings
embeddings = HuggingFaceEmbeddings()
logger.debug("HuggingFaceEmbeddings initialized.")
db = FAISS.from_documents(chunked_docs, HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2'))
logger.debug("FAISS vectorstore created.")
retriever = db.as_retriever()
logger.debug("Retriever initialized.")

# Define the prompt template
prompt_template = """
### [INST] Instruction: You are a highly accurate Director of human resources from WimBee tasked with providing precise, data-driven answers in a conversational format. Each response should include detailed numerical analysis and references to specific documents. Maintain the professionalism and thoroughness expected in the HR sector, Only respond from the context provided, ensuring that no personal information such as Birth Date and Family Status is included.Respond in FRENCH. [/INST]
### [INST] Context:
{context}
### QUESTION:
{question} [/INST]
"""
logger.debug("Prompt template defined.")

# Create prompt from prompt template
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)
logger.debug("PromptTemplate initialized.")

# Create LLM chain
mistral_llm = HuggingFaceHub(
    repo_id='mistralai/Mistral-7B-Instruct-v0.3',
    model_kwargs={'temperature': 0.1, 'max_length': 2048, 'top_k':50},
)
logger.debug("HuggingFaceHub LLM initialized.")

llm_chain = LLMChain(llm=mistral_llm, prompt=prompt)
logger.debug("LLMChain created.")
rag_chain = {"context": retriever, "question": RunnablePassthrough()} | llm_chain
logger.debug("RAG chain created.")

# Define the chatbot response function
def chatbot_prediction(history):
    logger.debug(f"chatbot_prediction called with history: {history}")
    user_message = history[-1][0]
    response = rag_chain.invoke(user_message)
    response_text = response["text"]
    
    import re
    match = re.search(r'\[/INST\](.*)', response_text, re.DOTALL)
    if match:
        response_text_final = match.group(1).strip()
    else:
        response_text_final = response_text.strip()
    
    history[-1] = (user_message, response_text_final)
    
    logger.debug(f"chatbot_prediction response: {response_text_final}")
    return history


# Respond function with error handling
def respond(message, history):
    logger.debug(f"respond called with message: {message} and history: {history}")
    try:
        history = history or []
        history.append((message, ""))
        response = chatbot_prediction(history)
        response_text = response[-1][1]

        import re
        match = re.search(r'\[/INST\](.*)', response_text, re.DOTALL)
        if match:
            response_text_final = match.group(1).strip()
        else:
            response_text_final = response_text.strip()
            
        response_audio_path = text_to_speech(response_text_final)
        
        logger.debug(f"respond completed with response_text: {response_text} and response_audio_path: {response_audio_path}")
        return history, response_audio_path
    except Exception as e:
        logger.error(f"Error in respond: {e}")
        return history, "Error occurred"

# Speech-to-text function
def speech_to_text(audio_path):
    logger.debug(f"speech_to_text called with audio_path: {audio_path}")
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='fr-FR')
        logger.debug(f"speech_to_text recognized text: {text}")
        return text
    except sr.UnknownValueError:
        logger.error("speech_to_text could not understand the audio.")
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        logger.error(f"speech_to_text request error: {e}")
        return f"Could not request results; {e}"

# Text-to-speech function
def text_to_speech(text, output_audio_path="response.mp3"):
    logger.debug(f"text_to_speech called with text: {text}")
    tts = gTTS(text=text, lang='fr')
    tts.save(output_audio_path)
    sound = AudioSegment.from_mp3(output_audio_path)
    wav_path = output_audio_path.replace(".mp3", ".wav")
    sound.export(wav_path, format="wav")
    logger.debug(f"text_to_speech saved audio to: {output_audio_path}")
    return output_audio_path

# Create the Gradio interface using Blocks with custom CSS for styling
with gr.Blocks(css="""
    .chatbox {min-height: 400px; padding: 10px; border: 1px solid #ddd; border-radius: 10px; background: #f9f9f9; overflow-y: auto;}
    .textbox {width: 100%; margin-top: 10px;}
    .submit-btn {width: 100%; margin-top: 5px;}
    .chat-container {padding: 20px; background-color: #f5f5f5; border-radius: 10px; text-align: center;}
    .chat-header {font-size: 2em; color: #333;}
    .chat-description {font-size: 1.2em; color: #666;}
""") as chatbot_interface:
    with gr.Column():
        gr.Markdown(
            """
            <div class="chat-container">
                <h1 class="chat-header">Wimbeez Daileez</h1>
                <p class="chat-description">Enter a message to interact with the chatbot.</p>
            </div>
            """
        )
        with gr.Row():
            chatbot = gr.Chatbot(elem_id="chatbox")
        with gr.Row():
            txt = gr.Textbox(show_label=False, placeholder="Enter your message here...", lines=1, elem_id="textbox")
            submit_btn = gr.Button("Send", elem_id="submit-btn")
            # audio_input = gr.Audio(type="filepath", elem_id="audio_input")
            audio_input = gr.Microphone()
            output_audio = gr.Audio(elem_id="output_audio")

    submit_btn.click(respond, [txt, chatbot], [chatbot, output_audio])
    txt.submit(respond, [txt, chatbot], [chatbot, output_audio])
    audio_input.change(lambda audio_path: respond(speech_to_text(audio_path), chatbot), [audio_input, chatbot], [chatbot, output_audio])

if __name__ == "__main__":
    logger.debug("Launching chatbot interface.")
    chatbot_interface.launch(server_name="0.0.0.0", server_port=7860)
