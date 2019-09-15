import h5py
import numpy as np
import copy

class Dense:
    def __init__(self,kernel,bias):
        self.kernel = kernel
        self.bias = bias

    def call(self,input):
        return np.matmul(input,self.kernel)+self.bias

class Activation:
    def __init__(self,function='relu'):
        if function=='relu':
            self.activation = 'relu'
        else:
            self.activation = 'softmax'
    def call(self,input):
        if self.activation=='relu':
            return np.max(0,input)
        else:
            return

def actual_outputs(weights,image):
    inp = image
    out=[]
    out.append([inp,inp])
    for i in range(len(weights)//2-1):
        w = np.reshape(weights[1+2*i],(1,len(weights[1+2*i])))
        inp = np.matmul(inp, weights[0+2*i])+np.repeat(w,len(inp),axis=0)
        h=copy.deepcopy(inp)
        # for j in range(len(inp)):
        #     inp[j]=np.maximum(0,inp[j])
        inp = np.maximum(0,inp)
        out.append([h,inp])
    w = np.reshape(weights[len(weights)-1], (1,len(weights[len(weights)-1])))
    inp = np.matmul(inp, weights[len(weights)-2]) + np.repeat(w,len(inp),axis=0)
    h=copy.deepcopy(inp)
    acc=0

    expinp = np.exp(inp)
    acc = expinp.sum(axis=1)
    acc = np.reshape(acc,(len(acc),1))
    acc = np.repeat(acc,len(inp[0]),axis=1)
    # for i in inp:
    #     acc+=np.exp(i)
    # for i in range(len(inp)):
    #     inp[i] = np.exp(inp[i])/acc
    inp = np.exp(inp)/acc
    out.append([h,inp])
    return out

def get_weights(file):
    w = []
    hf = h5py.File(file,'r')
    keys = hf.keys()
    # keys = hf.keys()
    for key in keys:
        if key[:5]=='dense':
            kernel = hf[key]['sequential'][key]['kernel:0']
            bias = hf[key]['sequential'][key]['bias:0']
            w.append(np.array(kernel))
            w.append(np.array(bias))
    return w

# get_weights()