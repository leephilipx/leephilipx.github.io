import numpy as np

# def generate_map(method='QPSK'):
#     if (method == 'QPSK'):
#         mapping_table = {
#             (0, 0): 1+1j,
#             (0, 1): -1+1j,
#             (1, 0): 1-1j,
#             (1, 1): -1-1j
#         }
#     demapping_table = {v: k for k, v in mapping_table.items()}
#     return mapping_table, demapping_table

def modulate(bits, mu=2):                                        
    bit_r = bits.reshape((int(len(bits)/mu), mu))                  
    return (2*bit_r[:,0]-1)+1j*(2*bit_r[:,1]-1)     

# def modulate(bits, mapping_table, mod_order=2):
#     bits = bits.reshape(len(bits)//mod_order, mod_order)
#     return np.array([mapping_table[tuple(b)] for b in bits])

def pad_and_reshape(X, n_data):
    return X.reshape(len(X)//n_data, n_data)

def IFFT(X, n_fft):
    return np.fft.ifft(X, n_fft)

def add_CP(signal, cp_len):
    cp = signal[-cp_len:]  # Take the last cp_len samples
    return np.hstack([cp, signal])

def PS(signal):
    return signal.reshape(-1)

def rician(x_s, K_rice, n_fft, channel_taps=3, fade_var_1D=1):
    pdp = np.array([.6, .3, .1])  # Power Delay Profile (PDP)
    K = 10 ** (K_rice/10)
    H_ray = np.sqrt(1/2) * ( np.random.randn(channel_taps) + 1j*np.random.randn(channel_taps) )
    H_ric = pdp * ( np.sqrt(K/(K+1)) + np.sqrt(1/(K+1)) * H_ray ) * fade_var_1D;
    H_ric = H_ric / np.linalg.norm(H_ric)   # Must normalise so that total power is unity
    return np.convolve(x_s, H_ric)[:len(x_s)]

def add_awgn(x_s, snrDB):
    data_pwr = np.mean(abs(x_s**2))
    noise_pwr = data_pwr/(10**(snrDB/10))
    noise = 1/np.sqrt(2) * ( np.random.randn(len(x_s)) + 1j*np.random.randn(len(x_s)) ) * np.sqrt(noise_pwr)
    # snr_meas = 10 * np.log10(np.mean(abs(x_s**2))/np.mean(abs(noise**2)))   # Measure SNR
    return x_s + noise

def fading_channel(x_s, snrDB, K_rice, n_fft=64):
    x_s = rician(x_s, K_rice, n_fft)
    return add_awgn(x_s, snrDB)

def serial_to_parallel(signal, n_fft, cp_len):
    row_count = n_fft + cp_len
    return signal.reshape((len(signal)//row_count, row_count))

def remove_CP(signal, n_fft):
    return signal[-n_fft:]  # Take the last n_fft samples

def FFT(X, n_fft):
    return np.fft.fft(X, n_fft)

# def demodulate(X, demapping_table, n_data, fft_remainder):
#     # Array of possible constellation points
#     constellation = np.array([i for i in demapping_table.keys()])
#     # Calculate distance of each RX point to each possible point
#     dists = abs(X.reshape((-1, 1)) - constellation.reshape((1, -1)))
#     # For each element in QAM, choose the index in constellation 
#     # that belongs to the nearest constellation point
#     const_index = dists.argmin(axis=1)
#     # Get back the real constellation point
#     hardDecision = constellation[const_index]
#     # Remove fft remainder
#     hardDecision = hardDecision[:len(hardDecision)-fft_remainder]
#     # Transform the constellation point into the bit groups
#     return np.hstack([demapping_table[C] for C in hardDecision]), hardDecision


### =================== Supplementary ================ ###

# def Clipping (x, CL):
#     sigma = np.sqrt(np.mean(np.square(np.abs(x))))
#     CL = CL*sigma
#     x_clipped = x  
#     clipped_idx = abs(x_clipped) > CL
#     x_clipped[clipped_idx] = np.divide((x_clipped[clipped_idx]*CL),abs(x_clipped[clipped_idx]))
#     return x_clipped

# def PAPR(x):
#     Power = np.abs(x)**2
#     PeakP = np.max(Power)
#     AvgP = np.mean(Power)
#     PAPR_dB = 10*np.log10(PeakP/AvgP)
#     return PAPR_dB

# def addCP(OFDM_time, CP, CP_flag, mu, K):
    
#     if CP_flag == False:
#         # add noise CP
#         bits_noise = np.random.binomial(n=1, p=0.5, size=(K*mu, ))
#         codeword_noise = Modulation(bits_noise, mu)
#         OFDM_data_nosie = codeword_noise
#         OFDM_time_noise = np.fft.ifft(OFDM_data_nosie)
#         cp = OFDM_time_noise[-CP:]
#     else:
#         cp = OFDM_time[-CP:]               # take the last CP samples ...
#     #cp = OFDM_time[-CP:] 
#     return np.hstack([cp, OFDM_time])  # ... and add them to the beginning

# def equalize(OFDM_demod, Hest):
#     return OFDM_demod / Hest

# def get_payload(equalized):
#     return equalized[dataCarriers]


# def PS(bits):
#     return bits.reshape((-1,))