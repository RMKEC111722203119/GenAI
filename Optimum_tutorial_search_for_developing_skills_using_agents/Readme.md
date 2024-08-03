

# Select-Stream-AI 🎥

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Usage](#usage)
- [Pages](#pages)
- [Future Updates](#future-updates)
- [Authors](#authors)
- [Contributing](#contributing)
- [License](#license)

## Overview

Select-Stream-AI is an innovative tool designed to help users find the most informative and concise YouTube videos on any topic quickly and optimally. Leveraging advanced AI technologies, Select-Stream-AI searches for YouTube videos, retrieves their transcripts, and analyzes them using cutting-edge language models to provide the best video recommendations for enhanced learning experiences.

## Features

- *YouTube Video Search*: Effortlessly find top videos related to your learning topic using the YouTube Data API.
- *Transcript Retrieval*: Automatically fetch and compile transcripts of selected videos for in-depth analysis.
- *AI-Driven Analysis*: Leverage state-of-the-art language models from Hugging Face and Groq to generate insightful questions and evaluate transcript quality.
- *Optimal Learning Recommendation*: Identify the most comprehensive and concise video, ensuring a fast and efficient learning process tailored to beginners.

## How It Works

1. *Search Query*: Enter your desired learning topic in the search bar.
2. *Video Retrieval*: The app searches YouTube for the top videos related to the query.
3. *Transcript Extraction*: Transcripts of the retrieved videos are fetched and processed.
4. *AI Analysis*: Advanced AI models analyze the transcripts, generate questions, and evaluate the quality of each video.
5. *Best Video Recommendation*: The app recommends the most suitable video based on the AI analysis.

## Installation

### Prerequisites

- Python 3.7+
- Streamlit
- Google API Client
- YouTube Transcript API
- LangChain
- Chroma
- nest_asyncio

### Setup

1. *Clone the Repository*:
    bash
    git clone https://github.com/RMKEC111722203119/GenAI/tree/main/Optimum_tutorial_search_for_developing_skills_using_agents
    
    

2. *Install Dependencies*:
    bash
    pip install -r requirements.txt
    

3. *Set Up API Keys*:
    - Obtain API keys from Google Cloud, Hugging Face, and Groq.
    - Replace the placeholder values in the script with your API keys:
      python
      API_KEY = "YOUR_GOOGLE_API_KEY"
      GROQ_API_KEY = "YOUR_GROQ_API_KEY"
      HUGGINGFACEHUB_API_TOKEN = "YOUR_HUGGINGFACE_API_TOKEN"
      

4. *Run the App*:
    bash
    streamlit run agent.py
    

## Usage

1. *Navigate to the Home Page*: Enter your learning topic in the search bar and click "Find Best Video".
2. *Processing*: The app will process your query, search for relevant YouTube videos, retrieve their transcripts, and analyze them.
3. *Recommendation*: The best video based on the AI analysis will be displayed for you to watch.

## Pages

- *Home*: Main page to enter your learning topic and get video recommendations.
- *Expert Videos*: Curated expert videos and resources.
- *Future Updates*: Information on upcoming features and improvements.
- *About*: Details about the project and authors.

## Future Updates

- *Enhanced AI Models*: Integration of more advanced language models for even better video recommendations.
- *Expanded Video Library*: Additional expert-curated videos and educational content.
- *User Customization*: Options for users to customize their learning experience and video preferences.
- *Improved Interface*: Refined user interface for an even more intuitive experience.

## Authors

- *THARUN KARTHICK*
  - [Email](mailto:karthicktharun11@gmail.com)
- *VIGNESHWARAN*
  - [Email](mailto:vign22112.it@rmkec.ac.in)
- *VIKRAM*
  - [Email](mailto:vikrxmofficial@gmail.com)
- *TEJAKRISHNA*
  - [Email](mailto:teja22105.it@rmkec.ac.in)

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
