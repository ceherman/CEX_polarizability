def mylj126wall(r,bubble,epsilon,sigma):
    mylambda = bubble - sigma*(2**(1/6))
    cutoffE = 2*epsilon*(sigma**6)*((sigma**6)/2 + 1.0 )
    frac = sigma/(r-mylambda)
    ener = 4.0*epsilon*(frac**6)*((frac**6)+1.0) - cutoffE
    return ener

def forcelj126wall(r,bubble,epsilon,sigma,mylambda):
    frac = sigma/(r-mylambda)
    force = - 24.0 * (epsilon/sigma) *(frac**7) * ( -2.0 * (frac**6) + 1.0 )  
    return force