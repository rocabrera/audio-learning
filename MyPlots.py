import numpy as np
import matplotlib.pyplot as plt


def plot_complex_exponential(A, f, phi, fs):
    
    T   = 1/fs
    t   = np.arange(0, 1, T)
    cexp = np.exp(1j*(2*np.pi*f*t+phi))    
    
    real_cexp = list(map(np.real,cexp))
    imag_cexp = list(map(np.imag,cexp))
    
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
    