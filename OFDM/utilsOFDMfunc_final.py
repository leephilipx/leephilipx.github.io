import numpy as np
import os
import tensorflow as tf
from tqdm import tqdm

### =================== Synthetic Generation ================ ###

def generate_pilots(P, mu):
    Pilot_file_name = 'Pilot_' + str(P)
    if os.path.isfile(Pilot_file_name):
        # load file
        bits = np.loadtxt(Pilot_file_name, delimiter=',')
        print('• Pilot file loaded:', Pilot_file_name)
    else:
        # write file
        bits = np.random.binomial(n=1, p=0.5, size=(P*mu, ))
        np.savetxt(Pilot_file_name, bits, delimiter=',')
        print('• New pilot file created:', Pilot_file_name)
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
        print('• Channel response file loaded:', channel_response_file_name)
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
        print('• Channel response file created:', channel_response_file_name)
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

def ofdm_simulate(codeword, pilotSymbols, snrDB, channel_response, params):
    X_block = np.vstack([pilotSymbols, modulate(codeword)])
    xt_block = IFFT(X_block, params['K'])
    if not params['removeCP_bool']: xt_block = add_CP(xt_block, params['CP'])
    xt = parallel_to_serial(xt_block)
    if params['clipping_bool']: xt = add_clipping(xt, CL=1.5)  # Add clipping before transmitting
    xr = channel_H(xt, snrDB, channel_response)
    xr_block = serial_to_parallel(xr, params['K'], 0 if params['removeCP_bool'] else params['CP'])
    if not params['removeCP_bool']: xr_block = remove_CP(xr_block, params['K'])
    return np.concatenate((np.concatenate((np.real(xr_block[0,:]), np.imag(xr_block[0,:]))),
                           np.concatenate((np.real(xr_block[1,:]), np.imag(xr_block[1,:])))))

def ofdm_gen(snrDB, H_type, params, channel_response_set_train, channel_response_set_test):
    while (True):
        input_samples = []
        input_labels = []
        for _ in range(2000):
            if (H_type == 'train'): channel_response = channel_response_set_train[np.random.randint(0, len(channel_response_set_train))]
            elif (H_type == 'test'): channel_response = channel_response_set_test[np.random.randint(0, len(channel_response_set_test))]
            bits = np.random.binomial(n=1, p=0.5, size=(params['n_bits'], ))
            if (params['P'] != params['K']):
                 signal_output = ofdm_simulate(bits, np.hstack([params['pilotSymbols'],
                                               modulate(np.random.binomial(n=1, p=0.5, size=(params['n_bits']-params['P']*params['mu'], )))]),
                                               snrDB, channel_response, params)
            else:
                signal_output = ofdm_simulate(bits, params['pilotSymbols'], snrDB, channel_response, params)  
            input_labels.append(bits[:params['n_bits_out']])
            input_samples.append(signal_output)
        batch_x = np.asarray(input_samples)
        batch_y = np.asarray(input_labels)
        yield batch_x, batch_y


### =================== DL Functions ================ ###



def instantiate_DL_model(params, stack_output_shape=2**3):
    print('Instatiating deep learning model \'channel_estimation_stack\'')
    def bit_err(y_true, y_pred):
        err = 1 - tf.reduce_mean(
            tf.reduce_mean(
                tf.cast(
                    tf.equal(tf.sign(y_pred - 0.5),
                            tf.cast(tf.sign(y_true - 0.5), tf.float32)),
                    dtype=tf.float32)
            ))
        return err
    def serial_stack(input_bits, stack_output_shape, stack_no):
        x = tf.keras.layers.Dense(128, activation='relu', name=f'dense_{stack_no}_1')(input_bits)  
        x = tf.keras.layers.Dense(64, activation='relu', name=f'dense_{stack_no}_2')(x)
        x = tf.keras.layers.Dense(32, activation='relu', name=f'dense_{stack_no}_3')(x)
        output_signal = tf.keras.layers.Dense(stack_output_shape, activation='sigmoid', name=f'dense_{stack_no}_out')(x)
        return output_signal
    stack_count = params['n_bits_out']//stack_output_shape
    input_bits = tf.keras.layers.Input(shape=(params['n_bits']*2, ), name='input')
    output_signal = tf.keras.layers.Concatenate(axis=1, name='concatenate')([serial_stack(input_bits, stack_output_shape, i+1) for i in range(stack_count)])
    model = tf.keras.Model(input_bits, output_signal, name='channel_estimation_stack')
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[bit_err])
    print(f'>> Each stack predicts {stack_output_shape} bits, with a total of {stack_count} stacks predicting {params["n_bits_out"]} total bits!')
    return model


def instantiate_callbacks(temp_path='./temp_checkpoint.h5', initial_learning_rate=0.01, epochs=5):
    def lr_time_based_decay(epoch, lr):
        return lr * 1 / (1 + decay * epoch)
    decay = initial_learning_rate / epochs
    lrs = tf.keras.callbacks.LearningRateScheduler(lr_time_based_decay, verbose=0)
    checkpoint = tf.keras.callbacks.ModelCheckpoint(temp_path, monitor='val_bit_err', verbose=0, save_best_only=True, mode='min', save_weights_only=False)
    return lrs, checkpoint


def ofdm_gen_BER(snrDB, K_rice, channel_len, params):
    while (True):
        input_samples = []
        input_labels = []
        for _ in range(10000):
            channel_response = generate_rician_channel(K_rice, channel_len)
            bits = np.random.binomial(n=1, p=0.5, size=(params['n_bits'], ))
            signal_output = ofdm_simulate(bits, params['pilotSymbols'], snrDB, channel_response, params)  
            input_labels.append(bits[:params['n_bits_out']])
            input_samples.append(signal_output)
        batch_x = np.asarray(input_samples)
        batch_y = np.asarray(input_labels)
        yield batch_x, batch_y


def evaluate_model(model, snrDB_list, Krice, channel_len, params):
    BER_list = []
    for snrDB in tqdm(snrDB_list):
        X_BER, y_BER = next(ofdm_gen_BER(snrDB, Krice, channel_len, params))
        preds_BER = np.round(model.predict(X_BER)).astype(int)
        BER_list.append(np.mean(np.abs(y_BER - preds_BER)))
    return np.array(BER_list)