

def amp_time_graphic(t, x, ax, xlabel, ylabel, label=None, title=None):
    ax = ax or plt.gca()
    ax.plot(t,x,label=label)    
    plot_style(ax, title, xlabel, ylabel)
    
def freq_1D_graphic(t, x, ax, xlabel, ylabel, label=None, title=None):
    ax = ax or plt.gca()
    ax.stem(t,x,label=label)    
    plot_style(ax, title, xlabel, ylabel)
    
def plot_style(ax, title, xlabel, ylabel):
    if ax:
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    else:
        ax.xlabel(xlabel)
        ax.ylabel(ylabel)
        ax.title(title)