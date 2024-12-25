# SelectStream Planner

SelectStream Planner is part of the GenAI project's suite of tools, specifically designed to help students create personalized learning paths and find educational resources. It uses AI to generate study plans and recommend learning materials.

## Features

- 🎯 Personalized study plans with clear milestones
- 📚 Curated learning resources from multiple sources
- 🎥 Relevant YouTube video recommendations
- 🔍 Web search integration via DuckDuckGo
- 📊 Progress tracking suggestions
- 💡 Learning technique recommendations
- 🤝 Community and forum suggestions

## Prerequisites

- Python 3.8+
- Gemini API key (Get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/selectstreamPublisher.git
cd selectstreamPublisher
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run Planner.py
```

2. Enter your Gemini API key in the password field
3. Type your learning query in the text input
4. Click "Get Study Resources" to receive personalized recommendations

## Dependencies

- streamlit
- phi-agent
- python-dotenv

## Project Structure

```
selectstreamPublisher/
├── Planner.py          # Main application file
├── README.md           # Documentation
└── requirements.txt    # Project dependencies
```

## Part of GenAI Project

This tool is a component of the larger [GenAI project](https://github.com/RMKEC111722203119/GenAI), which focuses on developing AI-powered educational tools and tutorials.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on the [SelectStream](https://github.com/RMKEC111722203119/SelectStream-fullstack)
- Uses Google's Gemini AI model
- Built with Streamlit and Phi-agent framework
