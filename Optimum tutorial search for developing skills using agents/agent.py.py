import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFaceHub
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool
from langchain_groq import ChatGroq
import json
import nest_asyncio
import os

nest_asyncio.apply()

API_KEY = "AIzaSyASpU0qAf8xcDgZ6Wqdw-Ts8WJftF0cDFU"
GROQ_API_KEY = "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"
HUGGINGFACEHUB_API_TOKEN = "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"

def ytsearch(search_query):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    try:
        search_response = youtube.search().list(
            q=search_query,
            part='id,snippet',
            maxResults=2,
            type='video'
        ).execute()

        video_details = [{
            'videoId': item['id']['videoId'],
            'title': item['snippet']['title'],
            'channelTitle': item['snippet']['channelTitle']
        } for item in search_response['items']]

        transcriptions = []
        for video in video_details:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video['videoId'])
                transcriptions.append({
                    'title': video['title'],
                    'channelTitle': video['channelTitle'],
                    'transcript': transcript
                })
            except Exception as e:
                print(f"An error occurred while retrieving the transcript for video {video['videoId']}: {e}")
                transcriptions.append({
                    'title': video['title'],
                    'channelTitle': video['channelTitle'],
                    'transcript': None
                })

        video1_transcript = ""
        video2_transcript = ""

        if transcriptions[0]['transcript'] is not None:
            video1_transcript = " ".join([line['text'] for line in transcriptions[0]['transcript']])

        if len(transcriptions) > 1 and transcriptions[1]['transcript'] is not None:
            video2_transcript = " ".join([line['text'] for line in transcriptions[1]['transcript']])

        return video1_transcript, video2_transcript, video_details

    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return None, None, []

def process_transcript_and_query(transcript, query):
    model_name = "BAAI/bge-base-en-v1.5"
    huggingfacehub_api_token = HUGGINGFACEHUB_API_TOKEN

    docs = [{'page_content': transcript}]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=20)
    chunks = text_splitter.split_documents(docs)

    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=HUGGINGFACEHUB_API_TOKEN, model_name=model_name
    )

    vectorstore = Chroma.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 2}
    )

    llm = HuggingFaceHub(
        repo_id="huggingfaceh4/zephyr-7b-alpha",
        model_kwargs={"temperature": 0.5, "max_length": 64, "max_new_tokens": 512},
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
    )

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="refine", retriever=retriever)
    response = qa.run(query)
    return response

def process(search_query):
    global video_transcript1, video_transcript2
    video_transcript1, video_transcript2, video_details = ytsearch(search_query)

    if not video_details:
        st.error("No video details found. Please try a different query.")
        return

    query = f"provide 10 questions on {search_query}"

    process_pdf_and_query_tool1 = Tool(
        name='Process PDF and Query 1',
        func=lambda q: process_transcript_and_query(video_transcript1, q),
        description="Useful for processing a transcript and answering a query based on its contents."
    )

    process_pdf_and_query_tool2 = Tool(
        name='Process PDF and Query 2',
        func=lambda q: process_transcript_and_query(video_transcript2, q),
        description="Useful for processing a transcript and answering a query based on its contents."
    )

    tools = [process_pdf_and_query_tool1, process_pdf_and_query_tool2]

    llm = ChatGroq(model="llama3-8b-8192", groq_api_key=GROQ_API_KEY)
    chat = ChatGroq(model="mixtral-8x7b-32768", groq_api_key=GROQ_API_KEY)

    system_message = "You are a helpful assistant."
    human_message = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system_message), ("human", human_message)])

    chain = prompt | chat
    questions = chain.invoke({"text": query}).content

    tool_query = f"""
    Use the provided tools to answer the following ten questions about {search_query}. For each question, identify and specify the best tool to use. Provide the response in the following format:

    The best tool for [Question] is [Tool Name].

    Only provide the answers in this format, without any additional information or explanations.

    {questions}
    """

    llm_with_tools = llm.bind_tools(tools)
    answers = llm_with_tools.invoke(tool_query).content

    final_query = f"give one word answer which is better query1 or query2. Expected output: query1 or query2 {answers}"
    final_answer = chat.invoke(final_query).content.strip()

    if final_answer == "query1":
        result = video_details[0]
    else:
        result = video_details[1]

    
    opid=result['videoId']
    st.video(f"https://www.youtube.com/watch?v={opid}")

st.set_page_config(page_title="AI-Enhanced YouTube Video Selector", page_icon="🎥", layout="wide")

page = st.sidebar.selectbox(
    "Navigate",
    ["Home", "Expert Videos", "Future Updates", "About"]
)

st.sidebar.subheader("Leave Your Feedback 💬")
comment = st.sidebar.text_area("Your Comment:")
if st.sidebar.button("Submit Comment"):
        if comment:
            st.success("Thank you for your feedback! 🙌")
            # Here you would handle the comment submission, e.g., saving to a database or file
        else:
            st.error("Please enter a comment before submitting.")
            
            

if page == "Home":
    st.title("Select-Stream AI 🎥")
    st.write(
        """
        Welcome to the **Select-Stream AI 🎥**! This tool is designed to help you find the most informative and concise YouTube videos on any topic quickly and optimally.

       
        """
    )

    query = st.text_input("What You Wanna Learn Today? 🤔")

    if st.button("Find Best Video"):
        if query:
            st.write("Processing your query...")
            process(query)
            st.write("Best video details will be displayed here.") 
        else:
            st.error("Please enter a search query.")

   

elif page == "Expert Videos":
    st.title("Expert Videos and Resources 🎓")
    st.write(
        """
        ### Curated Expert Videos

        This section features expert-curated videos designed to enhance your learning experience. Stay tuned as we add more valuable content here!

        """
    )

    st.subheader("Featured Videos")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("#### Video 1: Placeholder for Future Videos")
        st.video("https://youtu.be/G5GB6zhKm7s?si=fkPc4eDaudNyU--M")
    with col2:
        st.markdown("""
        **Open-Source Links:**
        - coming soon...
        - coming soon...
        - coming soon...
        """)

    col3, col4 = st.columns([2, 1])
    with col3:
        st.write("#### Video 2: Placeholder for Future Videos")
        st.video("https://youtu.be/G5GB6zhKm7s?si=fkPc4eDaudNyU--M")
    with col4:
        st.markdown("""
        **Open-Source Links:**
         - coming soon...
         - coming soon...
         - coming soon...
        """)

    col5, col6 = st.columns([2, 1])
    with col5:
        st.write("#### Video 3: Placeholder for Future Videos")
        st.video("https://youtu.be/G5GB6zhKm7s?si=fkPc4eDaudNyU--M")
    with col6:
        st.markdown("""
          **Open-Source Links:**
         - coming soon...
         - coming soon...
         - coming soon...
        """)

elif page == "Future Updates":
    st.title("Future Updates 🚀")
    st.write(
        """
        ### Upcoming Features and Improvements

        We are continuously working to enhance the AI-Enhanced YouTube Video Selector. Here's a glimpse of what's coming next:

        - 🧠 **Enhanced AI Models:** Integration of more advanced language models for even better video recommendations.
        - 📚 **Expanded Video Library:** Additional expert-curated videos and educational content.
        - 🎛️ **User Customization:** Options for users to customize their learning experience and video preferences.
        - 🖥️ **Improved Interface:** Refined user interface for an even more intuitive experience.

        Stay tuned for more updates as we strive to provide you with the best tools for optimized learning!
        """
    )

elif page == "About":
    st.title("About 📘")
    st.write(
        """
        ## AI-Enhanced YouTube Video Selector for Optimal Learning

        Supercharge your learning experience with our AI-powered YouTube video selector, designed to help beginners quickly and optimally find the best content on any topic. This innovative Python script integrates advanced technologies from Google, Hugging Face, and Groq to search for YouTube videos, retrieve their transcripts, and analyze them using cutting-edge language models.

        ### Features:
        - 🔍 **YouTube Video Search:** Effortlessly find top videos related to your learning topic using the YouTube Data API.
        - 📝 **Transcript Retrieval:** Automatically fetch and compile transcripts of selected videos for in-depth analysis.
        - 🤖 **AI-Driven Analysis:** Leverage state-of-the-art language models from Hugging Face and Groq to generate insightful questions and evaluate transcript quality.
        - 🚀 **Optimal Learning Recommendation:** Identify the most comprehensive and concise video, ensuring a fast and efficient learning process tailored to beginners.

        Boost your learning efficiency with this intelligent tool that brings precision and speed to video analysis. Perfect for students, educators, and anyone eager to enhance their knowledge with the best available content on YouTube.

        ### Author:
        - [VIGNESHWARAN](vign22112.it@rmkec.ac.in)
        - [THARUN KARTHICK](karthicktharun11@gmail.com)

        ### Contact:
        - [LinkedIn](https://www.linkedin.com/in/vigneshwaranit)
        - [GitHub](https://github.com/RMKEC111722203119?tab=repositories)

       
        """
    )
