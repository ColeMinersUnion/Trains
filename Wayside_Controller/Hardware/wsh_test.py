import pytest
from PyQt6.QtWidgets import QApplication
from HardwareShell import WaysideWindow


@pytest.fixture
def app():
    app = QApplication([])
    yield app
    app.quit()


def test_inital_state(qtbot):
    window = WaysideWindow()
    qtbot.addWidget(window)

    assert window.switch_58 == False
    assert window.switch_62 == False
    assert any(window.occupancy) == False
    assert any(window.maintenance) == False


def test_connection(qtbot):
    window = WaysideWindow()

    qtbot.addWidget(window)

    assert window.connected == False
    window.connect()
    assert window.connected == True
