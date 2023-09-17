import numpy as np
import scipy.stats as st
def data_add(input):
    #analyze new data with respect to a 95% confidence interval on previous data
    #this function should be used in the future to call stored values form storage location
    gen_vals =np.random.normal(input, input*.05, size=(25,))  #generate sample data
    return gen_vals

def conf_int(old, new):
    #old = array of old values, new = new data point

    #select the most recent 10 values for analysis
    gen_data = old[-10:]
    interv = st.t.interval(0.95, df=len(gen_data) - 1, loc=np.mean(gen_data), scale=st.sem(gen_data))
    if (new<interv[1]) & (new>interv[0]):
        return True
    else:
        return False