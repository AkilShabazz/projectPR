'''
Class that uses the formalism of Destexhe(1997) to compute the Hodgkin-Huxley states of an ionic channel.

Author - Renato Naville Watanabe
'''



import math


def compValOn(v0, alpha, beta, t, t0):
    '''
    Time course of the state during the pulse for the *inactivation* states
    and before and after the pulse for the *activation* states.

    The value of the state \f$v\f$ is computed according to the following
    equation:

    \f{equation}{
        v(t) = v_0\exp[-\beta(t-t_0)]
    \f} 
    where \f$t_0\f$ is the time at which the pulse changed
    the value (on to off or off to on) and \f$v_0\f$ is value
    of the state at that time.
    '''
    return v0 * math.exp(beta * (t0 - t))

def compValOff(v0, alpha, beta, t, t0):
    '''
    Time course of the state during the pulse for the *activation* states
    and before and after the pulse for the *inactivation* states.

    The value of the state \f$v\f$ is computed according to the following
    equation:

    \f{equation}{
        v(t) = 1 + (v_0 - 1)\exp[-\alpha(t-t_0)]
    \f} 
    where \f$t_0\f$ is the time at which the pulse changed
    the value (on to off or off to on) and \f$v_0\f$ is value
    of the state at that time.
    '''
    return 1.0 + (v0 - 1.0)  *  math.exp(alpha * (t0 - t))

class PulseConductanceState(object):
    '''
    Implements the Destexhe pulse approximation of the solution of 
    the states of the Hodgkin-Huxley neuron model.
    '''
    def __init__(self, kind, conf, pool,index):
        '''
        Initializes the pulse conductance state.

        Variables:
            kind - type of the state(m, h, n, q).
            conf - an instance of the Configuration class with the functions to correctly parameterize the model. See the Configuration class.
            pool - the pool that this state belongs.
            index - the index of the unit that this state belongs.                    
        '''
        self.kind = kind
        self.value = float(0)
        
        
        self.v0 = 0.0
        self.t0 = float(0)
        
        self.state = False
        
        self.beta_ms1 = float(conf.parameterSet('beta_' + kind, pool, index))
        self.alpha_ms1 = float(conf.parameterSet('alpha_' + kind, pool,index))
        self.PulseDur_ms = float(conf.parameterSet('PulseDur_' + kind, pool, index)) 
        
        if (self.kind == 'm'):
            self.actType = 'activation'
        if (self.kind == 'h'):
            self.actType = 'inactivation'
        if (self.kind == 'n'):
            self.actType = 'activation'
        if (self.kind == 'q'):
            self.actType = 'activation'

        if (self.actType == 'activation'):
            self.computeValueOn = compValOn
            self.computeValueOff = compValOff            
        else:
            self.computeValueOn = compValOff
            self.computeValueOff = compValOn         


    def changeState(self, t):
        '''
        Void function that modify the current situation (true/false)
        of the state.

        - Inputs:
            + **t**: current instant, in ms.
        '''
        self.t0, self.v0, self.state = t, self.value, not self.state


    def computeStateValue(self, t):
        '''
        Compute the state value by using the approximation of Destexhe (1997) to
        compute the Hodgkin-Huxley states.

        - Input:
            + **t**: current instant, in ms.
        '''

        if self.state:
            if (t - self.t0 > self.PulseDur_ms):
                self.changeState(t)
                self.value = self.computeValueOn(self.v0, self.alpha_ms1, self.beta_ms1, t, self.t0)
            else: self.value = self.computeValueOff(self.v0, self.alpha_ms1, self.beta_ms1, t, self.t0)
        else: self.value = self.computeValueOn(self.v0, self.alpha_ms1, self.beta_ms1, t, self.t0)

    
    