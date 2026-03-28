import os

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_PATH = 'images/attenuation_plot.png'
DISTANCE_CM = np.linspace(0.1, 20, 200)
REFERENCE_DISTANCE_CM = 0.1
ALPHA_BLOOD_DB_PER_CM_MHZ = 0.2
ALPHA_ICE_TISSUE_MIX_DB_PER_CM_MHZ = 0.4
FREQUENCIES_MHZ = [1, 3, 5, 7]


def build_plot(output_path=OUTPUT_PATH, show=True):
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    # wave is spreading spherically in space, energy spreading loss goes with r^2, amp with r
    # see: https://ccrma.stanford.edu/~jos/pasp/Spherical_Waves_Point_Source.html
    # We normalize to 0 dB at the starting distance (0.1 cm) to show the relative drop-off.
    # For pulse-echo, point-source spreading applies on the outbound and return paths,
    # so receive amplitude scales like (1/r) * (1/r) = 1/r^2 rather than 1/(2r).
    spreading_loss_db = 20 * np.log10(REFERENCE_DISTANCE_CM / DISTANCE_CM)
    ax.plot(
        DISTANCE_CM,
        2 * spreading_loss_db,
        color='black',
        linestyle='--',
        linewidth=1.6,
        label='Re-scattered Spreading (1/r², 2-way)',
    )

    # attenuation coefficient of soft tissue reference:
    # from: https://pubs.rsna.org/doi/pdf/10.1148/radiographics.13.3.8316679
    blood_color = '#9aa4b2'
    mix_colors = plt.get_cmap('viridis')(np.linspace(0.15, 0.95, len(FREQUENCIES_MHZ)))

    for color, freq_mhz in zip(mix_colors, FREQUENCIES_MHZ):
        atten_blood = ALPHA_BLOOD_DB_PER_CM_MHZ * freq_mhz * DISTANCE_CM * 2
        ax.plot(
            DISTANCE_CM,
            -atten_blood,
            color=blood_color,
            linestyle='--',
            linewidth=1.1,
            alpha=0.7,
            label=f'Blood: {freq_mhz} MHz',
        )

        atten_ice_mix = ALPHA_ICE_TISSUE_MIX_DB_PER_CM_MHZ * freq_mhz * DISTANCE_CM * 2
        ax.plot(
            DISTANCE_CM,
            -atten_ice_mix,
            color=color,
            linestyle='-',
            linewidth=2.3,
            label=f'ICE Tissue Mix: {freq_mhz} MHz',
        )

    ax.set_xlabel('Imaging Depth [cm]')
    ax.set_ylabel('Attenuation [dB]')
    ax.set_title('Ultrasound Attenuation (2-Way Path)')
    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)

    if show:
        plt.show()

    return fig, ax


if __name__ == '__main__':
    build_plot()
