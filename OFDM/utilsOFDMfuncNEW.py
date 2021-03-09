import numpy as np

### =================== Synthetic Generation ================ ###

def generate_pilots():
    Pilot_file_name = 'Pilot_' + str(P)
    if os.path.isfile(Pilot_file_name):
        # load file
        bits = np.loadtxt(Pilot_file_name, delimiter=',')
        print('Pilot file loaded!')
    else:
        # write file
        bits = np.random.binomial(n=1, p=0.5, size=(K*mu, ))
        np.savetxt(Pilot_file_name, bits, delimiter=',')
        print('New pilot file created!')
    return modulate(bits)

def generate_rician_channel(K_rice, channel_len):
    channel_taps = channel_len
    fade_var_1D = 1
    K = 10 ** (K_rice/10)
    pdp = np.exp(np.arange(-0.5, -0.5-channel_len*0.5, -0.5))  # Power Delay Profile (PDP)
    pdp = pdp / np.sum(pdp)
    H_ray = np.sqrt(1/2) * ( np.random.randn(channel_taps) + 1j*np.random.randn(channel_taps) )
    H_ric = pdp/np.sqrt(2) * ( np.sqrt(K/(K+1)) + np.sqrt(1/(K+1)) * H_ray ) * fade_var_1D;
    return H_ric / np.linalg.norm(H_ric)   # Must normalise so that total power is unity

def generate_channel_response_set():
    channel_response_file_name = 'rician_pdp_exp1_10.npy'
    if os.path.isfile(channel_response_file_name):
        # load file
        channel_response = np.ndarray.tolist(np.load(channel_response_file_name))
        channel_response_set_train = channel_response[:5000]
        channel_response_set_test = channel_response[5000:]
        print('Channel response file loaded!')
    else:
        # write file
        channel_response_set_train = []
        channel_response_set_test = []
        for K_rice in [-40, -40, -35, -30, -25, -20, -15, -10, 0, 10]:
            for channel_len in range(1, 11):
                channel_response_set_train = channel_response_set_train + [generate_rician_channel(K_rice, channel_len) for _ in range(50)]
        for K_rice in [-40, -40, -35, -30, -25, -20, -15, -10, 0, 10]:
            for channel_len in range(1, 11):
                channel_response_set_test = channel_response_set_test + [generate_rician_channel(K_rice, channel_len) for _ in range(50)]
        channel_response = channel_response_set_train + channel_response_set_test
        np.save(channel_response_file_name, channel_response)
        print('Channel response file created!')
    return channel_response_set_train, channel_response_set_test


### =================== Main OFDM Functions ================ ###

def modulate(bits, mu=2):                                        
    bit_r = bits.reshape((int(len(bits)/mu), mu))                  
    return (2*bit_r[:,0]-1)+1j*(2*bit_r[:,1]-1)     

def IFFT(X, n_fft):
    return np.fft.ifft(X, n_fft)

def add_CP(signal, cp_len):
    cp = signal[:,-cp_len:]  # Take the last cp_len samples
    return np.hstack([cp, signal])

def parallel_to_serial(signal):
    return signal.reshape(-1)

def add_clipping(x, CL=1):
    sigma = np.sqrt(np.mean(np.square(np.abs(x))))  # root-mean-square of signal
    CL = CL*sigma
    x_clipped = x
    clipped_idx = abs(x_clipped) > CL
    x_clipped[clipped_idx] = np.divide(x_clipped[clipped_idx]*CL, abs(x_clipped[clipped_idx]))
    return x_clipped
    
def channel_H(signal, snrDB, channelResponse):
    convolved = np.convolve(signal, channelResponse)[:len(signal)]
    signal_power = np.mean(abs(convolved**2))
    sigma2 = signal_power * 10**(-snrDB/10)  
    noise = np.sqrt(sigma2/2) * (np.random.randn(*convolved.shape)+1j*np.random.randn(*convolved.shape))
    return convolved + noise

def serial_to_parallel(signal, n_fft, cp_len):
    row_count = n_fft + cp_len
    return signal.reshape((len(signal)//row_count, row_count))

def remove_CP(signal, n_fft):
    return signal[:, -n_fft:]  # Take the last n_fft samples

def FFT(X, n_fft):
    return np.fft.fft(X, n_fft)