import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class StepWalker:
    """
    Simulates human-like interaction with a web page, now with the
    ability to schedule actions for specific time windows.
    """
    def __init__(self, driver, persona, stealth_engine):
        self.driver = driver
        self.persona = persona
        self.stealth_engine = stealth_engine
        self.actions = ActionChains(self.driver)

    def _wait_for_time_slip(self, desired_window=None):
        """
        Pauses execution until the current time is within the desired window.
        'desired_window' is a tuple of (start_hour, end_hour) in UTC.
        """
        if desired_window:
            start_hour, end_hour = desired_window
            current_hour_utc = int(time.strftime("%H", time.gmtime()))

            while not (start_hour <= current_hour_utc < end_hour):
                print(f"Time-Slip: Waiting for operational window ({start_hour}:00 - {end_hour}:00 UTC)...")
                time.sleep(60) # Sleep for a minute before checking again
                current_hour_utc = int(time.strftime("%H", time.gmtime()))

    def human_like_typing(self, element, text, time_slip_window=None):
        """
        Types text into an element with human-like delays, respecting time-slip windows.
        """
        self._wait_for_time_slip(time_slip_window)

        typing_rhythm = self.persona.get('typing_rhythm', {})
        wpm = typing_rhythm.get('wpm', 60)
        mistake_rate = typing_rhythm.get('mistake_rate', 0.03)

        for char in text:
            delay = 60 / (wpm * 5)
            time.sleep(delay * random.uniform(0.8, 1.2))

            if random.random() < mistake_rate:
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                element.send_keys(wrong_char)
                time.sleep(delay * 2)
                element.send_keys(Keys.BACKSPACE)
                time.sleep(delay * 1.5)

            element.send_keys(char)

        self.stealth_engine.wait()

    def human_like_click(self, element, time_slip_window=None):
        """
        Moves to an element and clicks it, respecting time-slip windows.
        """
        self._wait_for_time_slip(time_slip_window)

        self.actions.move_to_element(element).perform()
        self.stealth_engine.wait()
        element.click()
        self.stealth_engine.wait()

    def human_like_scroll(self, scrolls=3, time_slip_window=None):
        """
        Scrolls the page in a human-like manner, respecting time-slip windows.
        """
        self._wait_for_time_slip(time_slip_window)

        for _ in range(scrolls):
            self.driver.execute_script("window.scrollBy(0, {});".format(random.randint(200, 500)))
            time.sleep(random.uniform(0.1, 0.4))
        self.stealth_engine.wait()
