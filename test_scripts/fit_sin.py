import numpy as np
import scipy.optimize
import pandas as pd
import matplotlib.pyplot as plt

def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

    guess = np.array([70., 2.*np.pi*guess_freq, 0.,guess_offset])

    def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}

def horizontal_mean_distance(subset_size,step, data):
    means = []
    for i in range(1, step):  # i=1 for 2160, i=2 for 4320, i=3 for 6480
        start_index = 0
        end_index = i * subset_size
        if end_index <= len(data):
            subset = data['azimuth'][:end_index]
            mean_value = subset.mean()
            means.append(mean_value)
        else:
            # If end_index exceeds the length of the data, break the loop
            print(f"Subset size of {end_index} exceeds data length.")
            break

    # Convert means list to a numpy array
    means_array = np.array(means)
    return means_array
    
file_path = "/home/gabriel/Desktop/uniburger/output_data.csv"
df = pd.read_csv(file_path, delimiter=',', nrows=200000)

# Get X and Y values
df.index.name = 'index'
index = df["index"]
zenith = df['zenith']
azimuth = df['azimuth']

# Analyse frequency
index_time = np.linspace(0,(2/11),len(zenith))
results = fit_sin(index, zenith)
results_time = fit_sin(index_time,zenith)
print(f"idex based results: {results}")
print(f"time based results: {results_time}")
fit_function = results["fitfunc"]

A = 42.9612
w = 0.05524759249504118
p = 1.7952215857902365
c = 44.80487438155387
sinpopt = lambda t: A * np.sin(w*t + p) + c


plt.figure(figsize=(14, 6))

# Plot Azimuth
plt.subplot(1, 2, 1)
plt.plot(df['index'], df['azimuth'], 'o', label='Azimuth')
plt.xlabel('Point Index')
plt.ylabel('Azimuth angle (degrees)')
plt.title('Index vs Azimuth')
plt.grid(True)
plt.legend()

# Plot Zenith
plt.subplot(1, 2, 2)
plt.plot(df['index'], df['zenith'], 'o', label='Zenith', color='orange')

# Plot sinus fit
#plt.plot(index,fit_function(index), label="fitted") # original fit
plt.plot(index,sinpopt(index), label="fitted") # change in amplitude
plt.xlabel('Point Index')
plt.ylabel('Zenith angle(degrees)')
plt.title('Index vs Zenith')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Analyse mean distance between horizontal scans
step = 10
mean = horizontal_mean_distance(2160,10,df)
print(mean)
step_array = np.linspace(1,step,len(mean))
plt.plot(step_array, mean)
plt.show()
