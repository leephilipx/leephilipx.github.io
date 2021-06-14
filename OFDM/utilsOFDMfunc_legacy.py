import numpy as np
import scipy.interpolate

### =================== Conventional Methods ================ ###

# Auto increment number of bits to be divisible by modulation order
def generate_bits(n_bits, mod_order=2):
    n_bits = (np.ceil(n_bits/mod_order) * mod_order).astype(int)
    return np.random.binomial(n=1, p=0.5, size=(n_bits, )), n_bits

def generate_map(method='QPSK'):
    if (method == 'QPSK'):
        mapping_table = {
            (0, 0): 1+1j,
            (0, 1): -1+1j,
            (1, 0): 1-1j,
            (1, 1): -1-1j
        }
    demapping_table = {v: k for k, v in mapping_table.items()}
    return mapping_table, demapping_table

# QPSK end value used as default for pilot value
def generate_pilot(n_fft, pilot_count):
    pilotCarriers = np.round(np.linspace(0, n_fft-1, pilot_count)).astype(int)
    dataCarriers = np.delete(np.arange(n_fft), pilotCarriers)
    pilotValue = np.array([-1-1j], dtype=complex)
    return [pilotCarriers, pilotValue, dataCarriers]

def modulate(bits, mapping_table, mod_order=2):
    bits = bits.reshape(len(bits)//mod_order, mod_order)
    return np.array([mapping_table[tuple(b)] for b in bits])

def pad_and_reshape(X, n_data):
    fft_remainder = (n_data - (len(X) % n_data)) % n_data
    X_padded = np.hstack([X, np.zeros(fft_remainder, )])
    X_blocks = np.reshape(X_padded, (len(X_padded)//n_data, n_data))
    return X_blocks, fft_remainder

def add_pilot(X_blocks, pilotData):
    X_blocks_pilot = np.zeros((X_blocks.shape[0], len(pilotData[2]) + len(pilotData[0])), dtype=complex)
    X_blocks_pilot[:, pilotData[2]] = X_blocks
    X_blocks_pilot[:, pilotData[0]] = pilotData[1]
    return X_blocks_pilot

def IFFT(X, n_fft):
    return np.fft.ifft(X, n_fft)

def add_CP(signal, cp_len):
    cp = signal[:, -cp_len:]  # Take the last cp_len samples
    return np.hstack([cp, signal])

def parallel_to_serial(signal):
    return signal.reshape(-1)

## Main transmitter function
def transmitter(n_bits, mod_order=2, method='QPSK', n_fft=64):
    
    # Generate new stuff
    Tx, n_bits = generate_bits(n_bits)
    mapping_table, demapping_table = generate_map(method)
    pilotData = generate_pilot(n_fft, n_fft//8)  # Number of pilot carriers
    
    # Modulate into symbols and convert to time domain
    X = modulate(Tx, mapping_table, mod_order)
    X_blocks, fft_remainder = pad_and_reshape(X, len(pilotData[2]))
    X_blocks_pilot = add_pilot(X_blocks, pilotData)
    x_s = IFFT(X_blocks_pilot, n_fft)
    x_s = add_CP(x_s, n_fft//4)  # Length of cyclic prefix (CP)
    x_s = parallel_to_serial(x_s)
    
    return x_s, Tx, demapping_table, fft_remainder, pilotData
    
 
def channel_H_2(signal, snrDB, channelResponse):
    convolved = np.convolve(signal, channelResponse)[:len(signal)]
    signal_power = np.mean(abs(convolved**2))
    sigma2 = signal_power * 10**(-snrDB/10)  
    noise = np.sqrt(sigma2/2) * (np.random.randn(*convolved.shape)+1j*np.random.randn(*convolved.shape))
    return convolved + noise, np.sqrt(sigma2/2)


def serial_to_parallel(signal, row_count):
    return signal.reshape((len(signal)//row_count, row_count))

def remove_CP(signal, n_fft):
    return signal[:, -n_fft:]  # Take the last n_fft samples

def FFT(X, n_fft):
    return np.fft.fft(X, n_fft)

def LS_estimate(Y_blocks, pilotData):
    pilots = Y_blocks[:, pilotData[0]]  # extract the pilot values from the RX signal
    Hest_at_pilots = pilots / pilotData[1]
    Hest_abs = scipy.interpolate.interp1d(pilotData[0], abs(Hest_at_pilots), kind='linear')(pilotData[2])
    Hest_phase = scipy.interpolate.interp1d(pilotData[0], np.angle(Hest_at_pilots), kind='linear')(pilotData[2])
    Hest = Hest_abs * np.exp(1j*Hest_phase)
    return Y_blocks[:, pilotData[2]] / Hest

def Gen_autocorr(fade_var_1D, l, m, chan_len, FFT_len):
    auto_cor = 0 # autocorrelation initialization
    for auto_cnt in range(chan_len):
        auto_cor = auto_cor + (fade_var_1D * np.exp(-1j*2*np.pi*(l-m)*auto_cnt/FFT_len))
    return auto_cor

def LMMSE_estimate(Y_blocks, pilotData, n_fft, channel_length, noise_var_1D, fade_var_1D):
    pilot_count = len(pilotData[0])
    # Cross correlation matrix
    cross_cor_matrix = np.zeros((n_fft-pilot_count, pilot_count), dtype=complex);
    for i1 in range(n_fft-pilot_count):
        for i2 in range(pilot_count):
            cross_cor_matrix[i1,i2] = Gen_autocorr(fade_var_1D, pilotData[2][i1], pilotData[0][i2], channel_length, n_fft)
    # Autocorrelation Matrix Rh_ls, h_ls
    R_input = np.zeros((pilot_count, pilot_count), dtype=complex)
    for i1 in range(pilot_count):
        for i2 in range(pilot_count):
            R_input[i1,i2] = Gen_autocorr(fade_var_1D, pilotData[0][i1], pilotData[0][i2], channel_length, n_fft)
    X = np.diag(pilotData[1] * np.ones((pilot_count,), dtype=complex))
    auto_cor_matrix = R_input + noise_var_1D * np.linalg.inv(np.matmul(X, np.matrix(X).H))
    # Weight matrix    
    weight_matrix = np.divide(cross_cor_matrix, np.tile(auto_cor_matrix, ((n_fft-pilot_count)//pilot_count, 1)))
    # LMMSE-based Pilot Aided Channel Estimation (PACE)
    filter_input = Y_blocks[:, pilotData[0]].T / pilotData[1]
    H_est_lmmse = np.matmul(weight_matrix, filter_input)
    return (Y_blocks[:, pilotData[2]].T / H_est_lmmse).T

def demodulate(X, demapping_table, n_data, fft_remainder):
    # Array of possible constellation points
    constellation = np.array([i for i in demapping_table.keys()])
    # Calculate distance of each RX point to each possible point
    dists = abs(X.reshape((-1, 1)) - constellation.reshape((1, -1)))
    # For each element in QAM, choose the index in constellation 
    # that belongs to the nearest constellation point
    const_index = dists.argmin(axis=1)
    # Get back the real constellation point
    hardDecision = constellation[const_index]
    # Remove fft remainder
    hardDecision = hardDecision[:len(hardDecision)-fft_remainder]
    # Transform the constellation point into the bit groups
    return np.hstack([demapping_table[C] for C in np.squeeze(hardDecision)]), hardDecision

def receiver_LS(y_s, fft_remainder, demapping_table, pilotData, n_fft=64):
    y_s = serial_to_parallel(y_s, n_fft + n_fft//4)
    y_s = remove_CP(y_s, n_fft)
    Y_blocks = FFT(y_s, n_fft)
    X_hat_ls = LS_estimate(Y_blocks, pilotData)
    Rx_ls, X_blocks_ls = demodulate(X_hat_ls, demapping_table, len(pilotData[2]), fft_remainder)
    return Rx_ls

def receiver_LMMSE(y_s, fft_remainder, demapping_table, pilotData, noise_var_1D, fade_var_1D=0.5, n_fft=64, channel_length=6):
    y_s = serial_to_parallel(y_s, n_fft + n_fft//4)
    y_s = remove_CP(y_s, n_fft)
    Y_blocks = FFT(y_s, n_fft)  
    X_hat_lmmse = LMMSE_estimate(Y_blocks, pilotData, n_fft, channel_length, noise_var_1D, fade_var_1D)
    Rx_lmmse, X_blocks_lmmse = demodulate(X_hat_lmmse, demapping_table, len(pilotData[2]), fft_remainder)
    return Rx_lmmse
 


def ofdm_gen_BER_2(snrDB, K_rice, channel_len, params):
    while (True):
        input_samples = []
        input_labels = []
        for _ in range(1):
            channel_response = generate_rician_channel(K_rice, channel_len)
            bits = np.random.binomial(n=1, p=0.5, size=(params['n_bits'], ))
            signal_output = ofdm_simulate(bits, params['pilotSymbols'], snrDB, channel_response, params)  
            input_labels.append(bits[:params['n_bits_out']])
            input_samples.append(signal_output)
        batch_x = np.asarray(input_samples)
        batch_y = np.asarray(input_labels)
        yield batch_x, batch_y