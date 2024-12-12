import sys
from PyQt6.QtCore import QCoreApplication, QTimer
from TMmodel import TrainModel

def test_train_model():
    app = QCoreApplication(sys.argv)

    # Initialize TrainModel with mock route info
    route_info = [
        [1, 500, 60],  # Block ID, Block Length (meters), Speed Limit (km/h)
        [2, 700, 50],
        [3, 800, 40]
    ]

    train = TrainModel(route_info)
    train.parseRouteInfo()

    # Connect signals to monitor outputs
    def on_velocity_updated(velocity):
        print(f"Velocity Updated: {velocity:.2f} m/s")

    def on_acceleration_updated(acceleration):
        print(f"Acceleration Updated: {acceleration:.2f} m/s^2")

    def on_total_mass_updated(mass):
        print(f"Total Mass Updated: {mass:.2f} kg")

    def on_station_name_updated(name):
        print(f"Station Name Updated: {name}")

    def on_block_change(block_id):
        print(f"Block Changed: {block_id}")

    train.velocity_updated.connect(on_velocity_updated)
    train.acceleration_updated.connect(on_acceleration_updated)
    train.total_mass_updated.connect(on_total_mass_updated)
    train.station_name_updated.connect(on_station_name_updated)
    train.block_change.connect(on_block_change)

    # Test velocity calculation with various power inputs
    def test_velocity():
        print("\nTesting velocity calculation:")
        train.set_power(10000)  # Low power
        train.set_power(60000)  # Medium power
        train.set_power(120000)  # Max power
        train.set_power(0)  # No power

    # Test brake toggles
    def test_brakes():
        print("\nTesting brakes:")
        train.toggleServiceBrake()
        train.set_power(60000)  # Test braking while power is applied
        train.toggleServiceBrake()

        train.toggleEmergencyBrake()
        train.set_power(60000)  # Test emergency braking while power is applied
        train.toggleEmergencyBrake()

    # Test light toggles
    def test_lights():
        print("\nTesting lights:")
        train.toggleInteriorLights()
        train.toggleExteriorLights()

    # Test door toggles
    def test_doors():
        print("\nTesting doors:")
        train.toggleLeftDoors()
        train.toggleRightDoors()

    # Test failure scenarios
    def test_failures():
        print("\nTesting failures:")
        train.toggleEngineFailure()
        train.set_power(60000)
        train.toggleEngineFailure()

        train.toggleBrakeFailure()
        train.toggleServiceBrake()
        train.set_power(60000)
        train.toggleBrakeFailure()

        train.toggleSignalFailure()
        train.setTemperature(75)
        train.toggleSignalFailure()

    # Test beacon info
    def test_beacon():
        print("\nTesting beacon:")
        beacon_info = [1, "Central Station"]
        train.beaconInformation(beacon_info)

    # Run tests
    test_velocity()
    test_brakes()
    test_lights()
    test_doors()
    test_failures()
    test_beacon()

    # Quit after tests
    QTimer.singleShot(1000, app.quit)
    app.exec()

if __name__ == "__main__":
    test_train_model()
