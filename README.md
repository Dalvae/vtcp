# Voice to Clipboard (vtcp)

vtcp is a command-line utility that captures audio from your microphone, transcribes it using Azure Cognitive Services Speech-to-Text, and copies the transcribed text to your clipboard.

## Features

-   Real-time speech recognition
-   Copies transcribed text to clipboard
-   Supports silence detection to automatically stop recording
-   Plays a sound to indicate start and end of recording
-   Uses Azure Cognitive Services for accurate speech-to-text conversion

## Prerequisites

-   Python 3.7 or higher
-   Azure Cognitive Services account
-   Azure Speech Services subscription key and region

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd vtcp
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate  # On Windows
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Azure Credentials:**

    *   Create a `.env` file in the root directory of the project.
    *   Add your Azure Speech Services subscription key and region to the `.env` file:

        ```
        AZURE_SPEECH_KEY=your_key_here
        AZURE_SPEECH_REGION=your_region_here
        ```

        Replace `your_key_here` and `your_region_here` with your actual Azure credentials.  You can obtain these from the Azure portal.

## Usage

Run the `vtcp` command in your terminal:

