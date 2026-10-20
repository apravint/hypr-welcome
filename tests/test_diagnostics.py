import unittest
from hypr_welcome.diagnostics import get_system_diagnostics

class TestDiagnostics(unittest.TestCase):
    def test_get_diagnostics(self):
        diag = get_system_diagnostics()
        self.assertIsInstance(diag, list)
        self.assertTrue(len(diag) >= 4)
        labels = [item[0] for item in diag]
        self.assertIn("Processor", labels)
        self.assertIn("GPU Acceleration", labels)
        self.assertIn("Active Displays", labels)

if __name__ == "__main__":
    unittest.main()
