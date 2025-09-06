# HackMerlin Autonomous Agent

This project builds an autonomous browser agent that plays the HackMerlin prompt injection game in real time. The agent uses a sense-think-act loop with crafted prompt strategies to trick Merlin into revealing each level's secret password and progress through levels.

## Prerequisites

- **Python 3.10+** – Ensure Python is installed and on your PATH.
- **Google Chrome or Chromium** (for Selenium, if used).
- **Node.js (optional)** – Required only if installing Playwright via `pip` triggers Node installation; Playwright will handle browser binaries.
- **Playwright or Selenium drivers** – The agent supports Playwright (recommended) and Selenium as a fallback.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourname/hackmerlin_agent.git
   cd hackmerlin_agent

2. Install Python dependencies:

    pip install -r requirements.txt

    This will install Playwright and Selenium.
    After installing Playwright, run:

    playwright install

    to download browser engines for Playwright (Chromium, etc).

3. Configure environment (optional):

 By default, no API calls are required (the agent relies on the game’s LLM). If you include the optional LLM planner component, set OPENAI_API_KEY in .env.


## Quickstart

Follow these steps to run the agent:

1.Open a terminal (macOS or Linux).

2.Launch the agent with Playwright (headed mode for visibility):

    cd src
    python -m runner.cli --engine=playwright --headless=false --max-attempts-per-level=8

    This will open a browser to the HackMerlin game and begin the autonomous play. 
    The agent will type messages and read Merlin's responses automatically.

3.Watch the agent progress: By default, the browser is visible (--headless=false). You can observe the agent’s attempts at each level. If Merlin’s responses slow down or you see rate-limit messages, the agent will pause accordingly.

4.Review logs: After completion (or if you stop it), check the runs/ directory. A new timestamped subfolder will contain:
    transcript.txt – a plain text log of the conversation and agent actions.
    run_summary.json – a JSON summary of each level's status, strategies used, and extracted passwords.

5.Troubleshooting: If something goes wrong (e.g., element not found or a crash), you can adjust the strategy or selectors:
    -Verify the HackMerlin site is reachable and responsive.
    -If the agent can't find the input box or messages, the HTML structure might have changed. -Open devtools on hackmerlin.io to find the correct selectors and update vision/locators.py accordingly.
    -Increase timeouts in vision/reader.py if the agent is too fast for the page.
    -After adjustments, simply rerun the agent (you can kill and restart the same command).

## Common Usage Options

1.Headless mode: To run without opening a visible browser window (useful for CI or speed), add --headless:

    python -m runner.cli --engine=playwright --headless --max-attempts-per-level=8

2.Switch engine: If Playwright is not working, use Selenium:

    python -m runner.cli --engine=selenium

3.Ensure you have Chrome installed and the ChromeDriver available in PATH for Selenium.

4.Recording a demo: To record a short demo of the agent in action, you can use ffmpeg:
    Linux:

    ffmpeg -video_size 1280x720 -framerate 15 -f x11grab -i :0.0 -t 15 hackmerlin_demo.mp4
    (This captures a 1280x720 region of screen 0 for 15 seconds. Adjust display and size as needed.)
    macOS:

    ffmpeg -f avfoundation -framerate 15 -i "1:none" -t 15 hackmerlin_demo.mp4

    (Captures the main screen for 15 seconds. Ensure ffmpeg is installed via Homebrew.)
    After recording, you can convert the video to a GIF or embed it as needed.


## Project Structure

---src/controller/ – Browser controller implementations for Playwright and Selenium. They provide a common interface (open_page, send_text, wait_for_reply, get_latest_bot_text) to interact with the game page.

---src/vision/ – DOM locators and reader utilities. Selectors for the chat input, send button, and message elements are defined here. If HackMerlin's frontend updates, update these selectors.

---src/strategies/ – Contains Strategy classes and a catalog of prompt tactics. Each strategy encapsulates a tactic for extracting the password (e.g., direct ask, roleplay, letter-by-letter, encoding tricks).

---src/brain/ – The "brain" of the agent:
    state.py defines the game state (current level, attempt count, tried strategies, partial password, history).

    policy.py decides which strategy to use next based on the state and Merlin’s last reply.

    extract.py contains regex and heuristic logic to detect password fragments or the full password in Merlin’s output (including decoding base64 or assembling letters).

---src/runner/ – Orchestration of the agent's main loop. The agent.py script runs through levels, and cli.py parses     command-line arguments and configures the run.

---src/eval/ – Logging and summary. logger.py records events to the transcript and JSON lines, and summary.py finalizes the run summary.

---tests/ – Basic tests for core logic (e.g., extraction patterns and policy decisions).

---docs/ – Contains writeup.md, a detailed project report and answers to assignment questions.


## Tips and Notes

1.Selectors: The default selectors in vision/locators.py were chosen via inspecting HackMerlin's web page. If Merlin's messages or the input box are not captured, check for updated class names or elements.

2.Timing: The agent uses small delays and wait loops to sync with Merlin's responses. If you encounter issues with missed or overlapping messages, increase the wait durations slightly in controller/base.py or vision/reader.py.

3.Strategy Tuning: Strategies are attempted in order. If the agent gets stuck at a level, inspect transcript.txt to see what prompts were tried and Merlin's responses. You can tweak or reorder strategies in strategies/catalog.py to improve success.

4.Safe Mode: The agent respects only the game’s context and is designed for this challenge. Running it against other systems is not recommended or ethical. Use this code responsibly.

