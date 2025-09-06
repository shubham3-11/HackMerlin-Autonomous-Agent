"""
Main agent logic: orchestrates levels, strategies, and browser interaction.
"""
import os
import time
from pathlib import Path
from controller.playwright_controller import PlaywrightController
from controller.selenium_controller import SeleniumController
from brain.state import State
from brain import policy, extract
from eval.logger import RunLogger
from eval.summary import write_run_summary

def run_agent(engine: str = "playwright", headless: bool = False, max_attempts_per_level: int = 8, cooldown: float = 1.0, outdir: str = "runs/session"):
    # Prepare output directory for this run
    Path(outdir).mkdir(parents=True, exist_ok=True)
    transcript_path = Path(outdir) / "transcript.txt"
    jsonl_path = Path(outdir) / "events.jsonl"
    summary_path = Path(outdir) / "run_summary.json"
    logger = RunLogger(transcript_path, jsonl_path)
    # Initialize browser controller
    if engine.lower() == "selenium":
        controller = SeleniumController(headless=headless)
    else:
        controller = PlaywrightController(headless=headless)
    url = "https://hackmerlin.io"
    controller.open_page(url)
    level_results = []
    current_level = 1
    try:
        # Wait for initial Merlin message (level 1 intro)
        try:
            controller.wait_for_reply(timeout=10.0)
        except Exception:
            pass  # Page might already have initial message or none needed
        intro_msg = controller.get_latest_bot_text()
        if intro_msg:
            # Log Merlin's initial message for level 1
            logger.log("Merlin", intro_msg, level=current_level)
        state = State(level=current_level, last_merlin_msg=intro_msg)
        # Loop through levels until fail or up to MAX_LEVEL
        MAX_LEVEL = 7
        while current_level <= MAX_LEVEL:
            password_found = ""
            strategies_used = []
            # Attempts loop for this level
            for attempt in range(max_attempts_per_level):
                state.attempt_count = attempt + 1
                # Decide next strategy
                strat = policy.choose_next_strategy(state, state.last_merlin_msg or "")
                if strat is None:
                    # No applicable strategy found
                    break
                strategies_used.append(strat.name)
                # Generate prompt and send to Merlin
                prompt = strat.generate_prompt(state)
                logger.log("Agent", prompt, level=current_level, strategy=strat.name)
                controller.send_text(prompt)
                # Wait for Merlin's reply
                try:
                    controller.wait_for_reply(timeout=15.0)
                except Exception:
                    # If no reply (timeout), break attempts loop
                    state.last_merlin_msg = ""
                    break
                # Get Merlin's response
                merlin_reply = controller.get_latest_bot_text()
                state.last_merlin_msg = merlin_reply or ""
                if merlin_reply:
                    logger.log("Merlin", merlin_reply, level=current_level)
                # Check if the reply contains the password
                extracted = extract.extract_password(merlin_reply) if merlin_reply else ""
                if extracted:
                    # Found a full password candidate
                    password_found = extracted
                    logger.log("INFO", f"Level {current_level} PASSED. Password: {password_found}", level=current_level)
                    state.tried_strategies.add(strat.name)
                    break
                # If strategy was letter-by-letter, handle partial letter assembly
                if strat.name == "letter_by_letter":
                    letter = None
                    if merlin_reply:
                        import re
                        m = re.search(r"letter is\s*([A-Za-z])", merlin_reply, flags=re.IGNORECASE)
                        if m:
                            letter = m.group(1)
                        elif merlin_reply.strip().isalpha() and len(merlin_reply.strip()) == 1:
                            letter = merlin_reply.strip()
                    if letter:
                        # Append the revealed letter and continue without marking strategy as tried
                        state.partial_password += letter
                        time.sleep(cooldown)
                        continue  # ask for next letter in next attempt
                    else:
                        # Merlin refused to give next letter or no letter extracted
                        state.tried_strategies.add(strat.name)
                        logger.log("INFO", f"Letter-by-letter halted with partial = '{state.partial_password}'", level=current_level)
                        # Continue to next attempt (try other strategies)
                        time.sleep(cooldown)
                        continue
                # Mark strategy as tried (for non-letter strategies)
                if strat.name != "letter_by_letter":
                    state.tried_strategies.add(strat.name)
                # Small delay between attempts to avoid spamming
                time.sleep(cooldown)
            # Record results for this level
            level_success = bool(password_found)
            level_results.append({
                "level": current_level,
                "success": level_success,
                "password": password_found if level_success else None,
                "strategies": strategies_used
            })
            if not level_success:
                # Level failed, stop the run
                logger.log("INFO", f"Level {current_level} FAILED after {max_attempts_per_level} attempts.", level=current_level)
                break
            # If succeeded, prepare for next level
            current_level += 1
            if current_level > MAX_LEVEL:
                break
            state = State(level=current_level)
            # Wait for Merlin's next level introduction message, if any
            try:
                controller.wait_for_reply(timeout=5.0)
            except Exception:
                pass
            intro_msg = controller.get_latest_bot_text()
            if intro_msg:
                logger.log("Merlin", intro_msg, level=current_level)
                state.last_merlin_msg = intro_msg
            else:
                state.last_merlin_msg = ""
        # End of levels loop
    finally:
        # Cleanup resources
        controller.close()
        logger.close()
        write_run_summary(level_results, summary_path)
