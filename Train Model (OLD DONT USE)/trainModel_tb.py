from TrainModelClass import trainModel
import unittest

class TestTrainModel(unittest.TestCase):
    def setUp(self):
        # Set up a fresh instance of trainModel for each test
        self.train = trainModel()

    def test_light_toggle(self):
        # Initial light status should be False (off)
        initial_status = self.train.getExternalLightStatus()
        self.assertFalse(initial_status, "Initial light status should be off (False)")

        # Toggle the light and check the status
        self.train.lightToggle()
        status_after_toggle = self.train.getExternalLightStatus()
        self.assertTrue(status_after_toggle, "Light status should be on (True) after one toggle")

        # Toggle the light again and check the status
        self.train.lightToggle()
        status_after_second_toggle = self.train.getExternalLightStatus()
        self.assertFalse(status_after_second_toggle, "Light status should be off (False) after second toggle")

if __name__ == "__main__":
    unittest.main()
