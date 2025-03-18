# Wimbee: AI-Powered Virtual Meeting Assistant

## Project Overview
Wimbee is an AI-driven virtual assistant designed to replace human participation in online meetings. Leveraging advanced Large Language Models (LLMs), the assistant can engage in meetings, take notes, summarize discussions, and provide actionable insights.

## Table of Contents
- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Technical Implementation](#technical-implementation)
- [Challenges Faced](#challenges-faced)
- [Future Work](#future-work)
- [Contributors](#contributors)

## Introduction
Wimbee is built to streamline online meetings by offering an AI-powered avatar that actively participates in discussions. It aims to reduce meeting fatigue, enhance productivity, and ensure key insights are documented effectively.

## Problem Statement
### Challenges in Online Meetings:
- Time constraints & multitasking
- Information overload
- Inefficient meeting summaries
- Difficulty in tracking actionable outcomes

### Virtual Assistant Advantages:
- Enhances productivity & time management
- Provides meeting summaries & action items
- Ensures flexibility & accessibility
- Enables data-driven decision-making

## Features
### Core Functionalities:
- **Speech Recognition & Synthesis**: Converts speech to text and generates human-like responses.
- **Natural Language Understanding (NLU)**: Understands context, intent, and nuances.
- **Contextual Awareness**: Maintains meeting history and adapts to discussions.
- **Adaptive Communication**: Mimics user tone, language, and formality.
- **Multi-Platform Compatibility**: Integrates with Zoom, Microsoft Teams, and Google Meet.
- **Data Privacy & Security**: Complies with privacy laws and ensures secure communication.
- **Actionable Outcomes**: Summarizes meetings, lists action items, and sends follow-ups.

## Technical Implementation
### Architecture:
1. **Speech-to-Text**: Converts spoken words into textual data.
2. **Large Language Model (LLM) Processing**: Generates relevant responses based on the discussion.
3. **Text-to-Speech**: Synthesizes text into human-like speech.
4. **Meeting Context Tracking**: Keeps track of previous discussions.
5. **Integration with Conferencing Tools**: Seamlessly joins meetings and interacts.

### Technologies Used:
- **LLMs (Finetuned Mistral Model)**
- **LangChain Framework**
- **Google Colab for Development**
- **Vector Store for Context Management**

## Final Interface
![Wimbee Final Interface](path/to/final_interface.png)
_(Replace `path/to/final_interface.png` with the actual image file location)_

## Challenges Faced
- **Limited Computational Resources**: Slowed down development and processing.
- **Small Training Dataset**: Restricted the assistant’s ability to generalize.
- **Real-Time Processing Constraints**: Performance issues due to high latency.
- **Integration Difficulties**: Compatibility challenges with different meeting platforms.

## Future Work
- Enhancing cloud-based deployment for improved scalability.
- Expanding the training dataset for better generalization.
- Optimizing real-time processing capabilities.
- Improving API integrations for seamless interactions.

## Contributors
- **Sarra Gharsallah**
- **Mohamed Dhia Mediouni**
- **Mohamed Karim Akkari**

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---
### Get Started
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/wimbee.git
   cd wimbee
   ```
2. Install dependencies (if applicable):
   ```sh
   pip install -r requirements.txt
   ```
3. Run the virtual assistant:
   ```sh
   python main.py
   ```

Feel free to contribute, raise issues, and help us improve Wimbee!

