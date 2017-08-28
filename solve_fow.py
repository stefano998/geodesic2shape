import math as m
from deg2dms import deg2dms

def solve_fow (a,b,lat1,long1,az1,s):
    f=(a-b)/a
    lat1=m.radians(lat1)
    long1=m.radians(long1)
    az1=m.radians(az1)
    U1=m.atan((1-f)*m.tan(lat1))
    w1=m.atan(m.tan(U1)/m.cos(az1))
    sa=m.cos(U1)*m.sin(az1)
    ca2=1-sa**2;
    u2=ca2*(a**2-b**2)/b**2
    A=1+(u2/16384)*(4096+u2*(-768+u2*(320-175*u2)))
    B=(u2/1024)*(256+u2*(-128+u2*(74-47*u2)))
    w=s/(b*A)
    aux=w+1
    while m.fabs(w-aux)>1e-12:
        aux=w
        wm=(2*w1+w)/2
        dw=B*m.sin(w)*(m.cos(2*wm)+(B/4)*(m.cos(w)*(-1+2*((m.cos(2*wm))**2))-(B/6)*m.cos(2*wm)*(-3+4*(m.sin(w))**2)*(-3+4*(m.cos(2*wm))**2)))
        w=(s/(b*A))+dw
        
    lat2=m.atan((m.sin(U1)*m.cos(w)+m.cos(U1)*m.sin(w)*m.cos(az1))/((1-f)*m.sqrt((sa)**2+(m.sin(U1)*m.sin(w)-m.cos(U1)*m.cos(w)*m.cos(az1))**2)))
    lda=m.atan2((m.sin(w)*m.sin(az1)),(m.cos(U1)*m.cos(w)-m.sin(U1)*m.sin(w)*m.cos(az1)))
    C=(f/16)*ca2*(4+f*(4-3*ca2))
    L=lda-(1-C)*f*sa*(w+C*m.sin(w)*(m.cos(2*wm)+C*m.cos(w)*(-1+2*(m.cos(2*wm))**2)))
    if L>m.pi:
        L=-2*m.pi+m.fabs(L)
    if L<=-m.pi:
        L=2*m.pi-m.fabs(L)
    long2=L+long1
    if long2>m.pi+1e-12:
        long2=-2*m.pi+m.fabs(long2)
    if long2<-m.pi-1e-12:
        long2=2*m.pi-m.fabs(long2)
    az2=m.atan2(sa,(-m.sin(U1)*m.sin(w)+m.cos(U1)*m.cos(w)*m.cos(az1)))
    if az2<0:
        az2=2*m.pi+az2
    lat2=m.degrees(lat2)
    long2=m.degrees(long2)
    az2=m.degrees(az2)
    return (lat2, long2, az2)

    
