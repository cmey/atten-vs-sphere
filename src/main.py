import matplotlib.pyplot as plt
import numpy as np

distance = np.arange(20) * 1e-2  # [m]

# wave is spreading spherically in space, energy spreading loss goes with r^2, amp with r
# see: https://ccrma.stanford.edu/~jos/pasp/Spherical_Waves_Point_Source.html
# We account for 2-way loss here (double distance).
spreading_loss_factor = 1 / (2 * distance)
plt.plot(distance, 10 * np.log(1 * spreading_loss_factor), label='Spreading Loss')

# attenuation coefficient of soft tissue
# from: https://pubs.rsna.org/doi/pdf/10.1148/radiographics.13.3.8316679
# We account for 2-way loss here (double distance).
atten_coeff_db = 0.75 * 1e2 * 1e-6  # [dB/m/Hz]
for freq in np.arange(1e6, 10e6, 2e6):
    atten_db = atten_coeff_db * distance * 2 * freq
    plt.plot(distance, -atten_db, label='{:g} Hz atten.'.format(freq))

plt.xlabel('Distance to target [m]')
plt.ylabel('Attenuation of received signal [dB]')
plt.legend()

plt.show()

