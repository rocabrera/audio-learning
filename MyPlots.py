import numpy as np
import matplotlib.pyplot as plt


def plot_complex_exponential(A, f, phi, fs):
    
    T   = 1/fs
    t   = np.arange(0, 1, T)
    cexp = np.exp(1j*(2*np.pi*f*t+phi))    
    
    real_cexp = np.real(cexp)
    imag_cexp = np.imag(cexp)
    
    ys     = [real_cexp, imag_cexp]
    titles = ["Parte real", "Parte imaginária"]
    fig, axs = plt.subplots(2,1,figsize = (20,6))
    
    for y, title, ax in zip(ys, titles, axs.flatten()):
        
        ax.scatter(t,y, label = "Amostras", c = 'k')
        ax.plot(t,y, label = '"Dados reais"', c='r')
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
        axs[0].set_ylabel("Magnitude",fontsize = 16)

        axs[1].stem(ks, np.angle(X_k, deg=True))
        axs[1].set_ylabel("Graus",fontsize = 16)

        for ax in axs.flatten():
            ax.set_xlabel("Frequência",fontsize = 16)
            ax.set_xlim(-N/2, N/2-1)
            

        plt.suptitle("Discrete Fourier Transform",fontsize = 22)
        plt.tight_layout()
        plt.show()
    
    return X_k