import numpy as np
import matplotlib.pyplot as plt


def plot_complex_exponential(A, f, phi, fs):
    
    Ts    = 1/fs
    Tr    = 1/(f*100)
    ts    = np.arange(0, 1+Ts, Ts)
    tr    = np.arange(0, 1+Tr, Tr)
    cexps = np.exp(1j*(2*np.pi*f*ts+phi))    
    cexpr = np.exp(1j*(2*np.pi*f*tr+phi))    
    
    real_cexpr = np.real(cexpr)
    imag_cexpr = np.imag(cexpr)
    
    real_cexps = np.real(cexps)
    imag_cexps = np.imag(cexps)
    
    ys     = [(real_cexps, real_cexpr), (imag_cexps, imag_cexpr)]
    titles = ["Parte real", "Parte imaginária"]
    fig, axs = plt.subplots(2,1,figsize = (20,6))
    
    for y, title, ax in zip(ys, titles, axs.flatten()):
        y_sample, y_real = y
        ax.scatter(ts, y_sample, label = "Amostras", c = 'k')
        ax.plot(tr, y_real, label = '"Dados reais"', c='r')
        ax.set_xlabel("Tempo (s)", fontsize = 14)
        ax.set_ylabel("Amplitude",fontsize = 14)
        ax.set_title(title,fontsize = 22)
        ax.legend(fontsize=16) 
        
    plt.tight_layout()
    plt.show()
    
    
def plot_DFT(input_signal, plot=True):
    
    X_k = []
    
    N  = len(input_signal)
    ns = np.arange(-N/2, N/2)
    ks = np.arange(-N/2, N/2)
    
    for k in ks:
        s_k = np.exp(-1j*(2*np.pi*k)/N * ns)
        X_k.append(sum(input_signal*s_k))
        
    if plot:
        fig, axs = plt.subplots(1,2,figsize = (20,6))

        axs[0].stem(ks, np.abs(X_k))
        axs[0].set_ylabel("Decibels",fontsize = 16)

        axs[1].stem(ks, np.unwrap(np.angle(X_k,deg=True),discont=180))
        axs[1].set_ylabel("Graus",fontsize = 16)

        for ax in axs.flatten():
            ax.set_xlabel("Frequência",fontsize = 16)
            ax.set_xlim(-N/2, N/2-1)
            
        plt.suptitle("Discrete Fourier Transform",fontsize = 22)
        plt.tight_layout()
        plt.show()
    
    return X_k