from ghost.payloads.base import Payload

class GhostCourier:
    """
    Handles the human-like delivery of payloads, using the StealthEngine
    for timing and the StepWalker for interaction.
    """
    def __init__(self, step_walker, stealth_engine):
        self.step_walker = step_walker
        self.stealth_engine = stealth_engine

    def deliver_text_message(self, text_area_element, message, time_slip_window=None):
        """
        Delivers a text message to a text area element.
        """
        print(f"Courier: Delivering message...")
        self.step_walker.human_like_typing(text_area_element, message, time_slip_window)
        # In a real scenario, you'd find and click the 'send' button.
        print("Courier: Message delivered.")
        self.stealth_engine.wait()

    def deliver_payload_file(self, file_input_element, payload: Payload, time_slip_window=None):
        """
        Delivers a file-based payload.
        """
        if not payload.is_file_based:
            raise ValueError("Payload is not file-based.")

        print(f"Courier: Delivering file payload '{payload.name}'...")
        file_path = payload.get_content() # This would return the path to the file

        # Selenium's send_keys on a file input element handles the upload dialog.
        self.step_walker.human_like_typing(file_input_element, file_path, time_slip_window)

        print("Courier: File payload delivered.")
        self.stealth_engine.wait()
