# Text Summarization Tool

A GUI-based text summarization tool that converts large chunks of text into concise summaries, running inside a Docker container.

## Features

-   User-friendly Tkinter GUI interface.
-   Text input via direct paste or file upload.
-   Extractive summarization algorithm using NLTK.
-   Adjustable summary length (number of sentences).
-   Displays input and summary statistics in the terminal.
-   Dockerized for easy setup and consistent execution.

## Requirements

-   Docker Desktop
-   An X Server for GUI forwarding (e.g., X410 or VcXsrv on Windows)
-   Python 3.10 (for running from source or understanding the code)
-   `nltk` (for running from source)

## Project Structure

```
TextSummarizationTool/
├── text_summarizer.py      # Main Python application with Tkinter GUI
├── Dockerfile              # Instructions to build the Docker image
├── docker-compose.yml      # Configuration to run the Docker container
├── requirements.txt        # Python dependencies for the application
└── README.md               # This documentation file
```

## Running the Application (Docker - Recommended)

These instructions are for running the Tkinter GUI application from within a Docker container, with the GUI displayed on your host machine.

**1. Prerequisites:**

   a.  **Install Docker Desktop:** Download and install from [Docker's official website](https://www.docker.com/products/docker-desktop).

   b.  **Install an X Server (for Windows/macOS users needing GUI display from Docker):**
       *   **Windows:** Install X410 (from Microsoft Store) or [VcXsrv](https://sourceforge.net/projects/vcxsrv/).
       *   **macOS:** Install [XQuartz](https://www.xquartz.org/).
       *   **Linux:** You likely already have an X server running.

   c.  **Start your X Server:** Ensure X410, VcXsrv, or XQuartz is running before proceeding.

**2. Configure `DISPLAY` Environment Variable (Host Machine):**

   Open a terminal/PowerShell on your host machine and set the `DISPLAY` variable. The value might differ based on your OS and X Server setup.

   *   **For Windows with X410/VcXsrv (using WSL2 backend for Docker):**
       ```powershell
       $env:DISPLAY="host.docker.internal:0.0"
       ```
       Alternatively, you might need your machine's IP address:
       ```powershell
       # Find your machine's local IP, e.g., 192.168.1.100
       $env:DISPLAY="192.168.1.100:0.0"
       ```
       *Ensure your X Server is configured to allow connections (e.g., disable access control in X410/VcXsrv or add an exception to your firewall for TCP port 6000).*

   *   **For macOS with XQuartz:**
       The `DISPLAY` variable is often set up automatically by XQuartz. If issues arise, you might need to use your Mac's IP:
       ```bash
       export DISPLAY=$(ipconfig getifaddr en0):0
       ```

   *   **For Linux:**
       Usually, this is already set. You can check with `echo $DISPLAY`. It's often `:0` or `:1`.
       If Docker is running as root and your user is different, you might need to handle `xauth` permissions or use `DISPLAY=$(hostname):0.0`.

**3. Clone the Repository (if you haven't already):**

   ```bash
   git clone <repository_url>
   cd TextSummarizationTool
   ```

**4. Build and Run with Docker Compose:**

   In the project's root directory (where `docker-compose.yml` is located), run:

   ```bash
   docker-compose up --build
   ```

   This command will:
   *   Build the Docker image based on the `Dockerfile` (if it's the first time or if files changed).
   *   Start a container based on that image.
   *   The Tkinter application GUI should appear on your host desktop.

**5. Using the Application:**

   *   The Text Summarization Tool window will appear.
   *   Use the "Upload Text File" button to load text from a `.txt` file or paste text directly into the "Input Text" area.
   *   Adjust the "Summary Length" slider to set the desired number of sentences for the summary.
   *   Click "Generate Summary". The summary will appear in the "Summary" area.
   *   Check the terminal where `docker-compose up` is running for input/summary statistics.

**6. Stopping the Application:**

   *   Press `Ctrl+C` in the terminal where `docker-compose up` is running.
   *   To remove the container (and network if created), run:
       ```bash
       docker-compose down
       ```

## Running from Source (Alternative - for development/testing)

1.  **Clone the repository and navigate into it.**
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Download NLTK data (one-time setup):**
    Open a Python interpreter and run:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    ```
5.  **Run the application:**
    ```bash
    python text_summarizer.py
    ```

## Troubleshooting Docker GUI Issues

-   **`_tkinter.TclError: couldn't connect to display`**: This is the most common issue.
    *   Ensure your X Server (X410, VcXsrv, XQuartz) is running on the host.
    *   Verify the `DISPLAY` environment variable is correctly set on the host *before* running `docker-compose up` and that it's correctly passed to the container (as configured in `docker-compose.yml`).
    *   Check X Server access control settings. For X410/VcXsrv, you might need to disable access control or allow connections from your Docker network IP range.
    *   Ensure your firewall is not blocking TCP connections to your X Server (usually on port 6000 + display number, e.g., 6000 for `:0.0`).
-   **WSL2 & Docker Desktop (Windows):** Ensure WSL integration is enabled in Docker Desktop settings for your distribution.
