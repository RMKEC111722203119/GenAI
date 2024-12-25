import streamlit as st
import json
import time
from phi.agent import Agent
from phi.tools.youtube_tools import YouTubeTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.model.google import Gemini 

# Configure page
st.set_page_config(
    page_title="SelectStream Planner",
    page_icon="📚",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .title {
        text-align: center;
        color: #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("<h1 class='title'>📚 SelectStream Planner</h1>", unsafe_allow_html=True)
st.markdown("---")

# Create two columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    api_key = st.text_input("Enter your Gemini API Key 🔑", type="password")
    
with col2:
    st.markdown("### Need an API key?")
    st.markdown("Get it from [Google AI Studio](https://aistudio.google.com/)")

query = st.text_area("What would you like to learn about? 🤔", height=100)

if st.button("🚀 Get Study Resources", type="primary"):
    if not api_key or not query:
        st.error("Please provide both API key and query!")
    else:
        try:
            with st.spinner('🎯 Creating your personalized study plan...'):
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate progress steps
                status_text.text("🔍 Searching for resources...")
                progress_bar.progress(25)
                time.sleep(1)
                
                status_text.text("📚 Analyzing content...")
                progress_bar.progress(50)
                
                # Create agent and get response
                study_partner = Agent(
                    name="SelectStream Planner",
                    model=Gemini(id="gemini-2.0-flash-exp", api_key=api_key),
                    tools=[DuckDuckGo(), YouTubeTools()],
                    markdown=True,
                    description="You are a study planner who assists users in finding resources, answering questions, and providing explanations on various topics.",
                    instructions=[
                        "Use DuckDuckgo to search for relevant information on the given topic and verify information from multiple reliable sources.",
                        "Break down complex topics into digestible chunks and provide step-by-step explanations with practical examples.",
                        "Share shortest path and curated learning resources including documentation, tutorials, articles, research papers, and community discussions.",
                        "Recommend high-quality YouTube videos and online courses that match the user's learning style and proficiency level.",
                        "Suggest hands-on projects and exercises to reinforce learning, ranging from beginner to advanced difficulty.",
                        "Always Create personalized study plans with clear milestones, deadlines, and progress tracking.",
                        "Provide tips for effective learning techniques, time management, and maintaining motivation.",
                        "Recommend relevant communities, forums, and study groups for peer learning and networking.",
                        "Always add the sources at the end",
                        "Always use tools before answering"
                    ],
                    show_tool_calls=True,
                    debug_mode=True,
                    
                )
                
                status_text.text("✍️ Generating study plan...")
                progress_bar.progress(75)
                
                response = study_partner.print_response(query)
                response = study_partner.get_chat_history()
                
                status_text.text("✨ Finalizing results...")
                progress_bar.progress(100)
                time.sleep(1)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Display results in a nice container
                with st.container():
                    st.success("🎉 Your study plan is ready!")
                    response_json = json.loads(response)
                    st.markdown("### 📋 Study Plan")
                    st.markdown(response_json[1]['content'])
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("### 💡 Tips")
st.info("For better results, be specific about your learning goals and current knowledge level!")


