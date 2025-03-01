import threading
from inputs import get_gamepad, UnpluggedError


class XboxController:
    def __init__(self):
        # Status
        self.plugged = True

        # Buttons
        self.A = 0
        self.B = 0
        self.X = 0
        self.Y = 0

        self.LB = 0
        self.RB = 0

        self.L3 = 0
        self.R3 = 0

        # Triggers
        self.LT_R = 0
        self.RT_R = 0

        self.LT = 0.0
        self.RT = 0.0

        # Joysticks
        self.LJ_X = 0
        self.LJ_Y = 0
        self.RJ_X = 0
        self.RJ_Y = 0

        self.LJ = (0.0, 0.0)
        self.RJ = (0.0, 0.0)

        # D-pad
        self.D_PAD_X = 0
        self.D_PAD_Y = 0

        self.D_PAD = (0, 0)

        # Create and start the reading thread
        reading_thread = threading.Thread(target=self.read_gamepad, daemon=True)
        reading_thread.start()

    def read_gamepad(self):
        while True:
            try:
                # Get all current events
                events = {event.code: event.state for event in get_gamepad()}

                # Update status
                self.plugged = True

                # Update buttons
                self.A = events.get("BTN_SOUTH", self.A)
                self.B = events.get("BTN_EAST", self.B)
                self.X = events.get("BTN_NORTH", self.X)
                self.Y = events.get("BTN_WEST", self.Y)

                self.LB = events.get("BTN_TL", self.LB)
                self.RB = events.get("BTN_TR", self.RB)

                self.L3 = events.get("BTN_THUMBL", self.L3)
                self.R3 = events.get("BTN_THUMBR", self.R3)

                # Update triggers
                self.LT_R = events.get("ABS_Z", self.LT_R)
                self.RT_R = events.get("ABS_RZ", self.RT_R)

                self.LT = self.LT_R / 256
                self.RT = self.RT_R / 256

                # Update joysticks
                self.LJ_X = events.get("ABS_X", self.LJ_X)
                self.LJ_Y = events.get("ABS_Y", self.LJ_Y)
                self.RJ_X = events.get("ABS_RX", self.RJ_X)
                self.RJ_Y = events.get("ABS_RY", self.RJ_Y)

                self.LJ = (self.LJ_X / 32768, self.LJ_Y / 32768)
                self.RJ = (self.RJ_X / 32768, self.RJ_Y / 32768)

                # Update D-pad
                self.D_PAD_X = events.get("ABS_HAT0X", self.D_PAD_X)
                self.D_PAD_Y = events.get("ABS_HAT0Y", self.D_PAD_Y)

                self.D_PAD = (self.D_PAD_X, -self.D_PAD_Y)

            except UnpluggedError:
                self.plugged = False
