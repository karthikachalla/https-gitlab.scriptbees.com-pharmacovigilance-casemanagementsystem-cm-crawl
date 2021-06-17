def compound_intrest(p,t,r):
    print('The Pricipal Value:',p)
    print('Time period:',t)
    print('Rate of intrest:',r)
    amount=p*(1+(r/100))**t
    ci=amount-p
    print('The Compound Intrest is:',ci)
    return ci
print(compound_intrest(10000,10.5,5))