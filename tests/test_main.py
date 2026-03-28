import os
import tempfile
import unittest

import matplotlib

matplotlib.use('Agg')

from src.main import build_plot


class MainPlotTests(unittest.TestCase):
    def test_build_plot_creates_expected_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'attenuation_plot.png')

            fig, ax = build_plot(output_path=output_path, show=False)

            self.assertTrue(os.path.exists(output_path))
            self.assertEqual(ax.get_xlabel(), 'Imaging Depth [cm]')
            self.assertEqual(ax.get_title(), 'Ultrasound Attenuation (2-Way Path)')

            legend_labels = [text.get_text() for text in ax.get_legend().get_texts()]
            self.assertIn('Re-scattered Spreading (1/r², 2-way)', legend_labels)
            self.assertIn('ICE Tissue Mix: 7 MHz', legend_labels)
            self.assertIn('Blood: 7 MHz', legend_labels)

            matplotlib.pyplot.close(fig)


if __name__ == '__main__':
    unittest.main()