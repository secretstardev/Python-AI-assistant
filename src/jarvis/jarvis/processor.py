from jarvis.action_controller import ActionController
from jarvis.assistant_utils import start_up, assistant_response, call_wolframalpha


class Processor:
    def __init__(self):
        self.action_controller = ActionController()
        self.client = wolframalpha.Client(WOLFRAMALPHA_API['key'])

    def run(self):
        start_up()
        while True:
            self._process()
            self.action_controller.shutdown_check()

    def _process(self):
        # Check if the assistant is waked up
        if self.action_controller.wake_up_check():

            # Record user voice and create a voice transcipt
            self.action_controller._get_voice_transcript()

            # Extract actions and update the actions (state of action controller)
            self.action_controller._get_user_actions()

            # Checks is ther is an action to execute them
            if self.action_controller.actions:
                self.action_controller._execute()
            else:
                # If there is not an action the assistant make a request in
                # Wolframalpha api for response
                call_wolframalpha(self.action_controller.latest_voice_transcript)