import math as m


def solve_inv (a,b,lat1,long1,lat2,long2):
    f=(a-b)/a
    lat1=m.radians(lat1)
    long1=m.radians(long1)
    lat2=m.radians(lat2)
    long2=m.radians(long2)

    if lat1==lat2 and long1==long2: #solve a bug (when p1=p2)
        az1=0
        az2=az1
        s=0
        return (az1,az2,s)

    if m.fabs(lat1-m.pi/2)<1e-16:   #solve a bug (when abs(lat1)=pi/2)
        lat1=m.pi/2-1e-12
    if m.fabs(lat1+m.pi/2)<1e-16:
        lat1=m.pi/2+1e-12

    if abs(lat2-m.pi/2)<1e-16:  #solve a bug (when abs(lat2)=pi/2)
        lat2=m.pi/2-1e-12
    if abs(lat2+m.pi/2)<1e-16:
        lat2=m.pi/2+1e-12

    auxlong = abs(long2-long1); #solve a bug (when lat1=lat2=0)
    if lat1==0 and lat2==0:
        az1=m.pi/2; az2=3*m.pi/2;
        if auxlong>m.pi: 
            az1=3*m.pi/2;az2=m.pi/2;
        az1=m.degrees(az1)
        az2=m.degrees(az2)
        s=a*auxlong
        return (az1,az2,s)

    L=long2-long1
    if L>m.pi:
        L=-2*m.pi+m.fabs(L)
    if L<-m.pi:
        L=2*m.pi-m.fabs(L)
    U1=m.atan((1-f)*m.tan(lat1))
    U2=m.atan((1-f)*m.tan(lat2))
    lda=L
    aux=lda+1
    while abs(lda-aux)>1e-12:
        sw=m.sqrt((m.cos(U2)*m.sin(lda))**2+(m.cos(U1)*m.sin(U2)-m.sin(U1)*m.cos(U2)*m.cos(lda))**2)
        cw=m.sin(U1)*m.sin(U2)+m.cos(U1)*m.cos(U2)*m.cos(lda)
        w=m.atan2(sw,cw)
        sa=m.cos(U1)*m.cos(U2)*m.sin(lda)/sw
        ca2=1-sa**2
        c2wm=cw-2*m.sin(U1)*m.sin(U2)/ca2
        C=(f/16)*ca2*(4+f*(4-3*ca2))
        aux=lda
        lda=L+(1-C)*f*sa*(w+C*sw*(c2wm+C*cw*(-1+2*c2wm**2)))
    u2=ca2*(a**2-b**2)/b**2
    A=1+(u2/16384)*(4096+u2*(-768+u2*(320-175*u2)))
    B=(u2/1024)*(256+u2*(-128+u2*(74-47*u2)))
    dw=B*sw*(c2wm+(B/4)*(cw*(-1+2*c2wm**2)-(B/6)*c2wm*(-3+4*m.sin(w)**2)*(-3+4*c2wm**2)))
    s=b*A*(w-dw)
    tan_az1=m.cos(U2)*m.sin(lda)/(m.cos(U1)*m.sin(U2)-m.sin(U1)*m.cos(U2)*m.cos(lda))
    tan_az2=m.cos(U1)*m.sin(lda)/(-m.sin(U1)*m.cos(U2)+m.cos(U1)*m.sin(U2)*m.cos(lda))
    az1=m.atan(tan_az1)
    az2=m.atan(tan_az2)
    if tan_az1>0 and L<0:
        az1=m.pi+az1
    if tan_az1<0 and L>0:
        az1=m.pi+az1
    if tan_az1<0 and L<0:
        az1=2*m.pi-m.fabs(az1)
    if tan_az2>0 and -L<0:
        az2=m.pi+az2
    if tan_az2<0 and -L>0:
        az2=m.pi+az2
    if tan_az2<0 and -L<0:
        az2=2*m.pi-m.fabs(az2)

    auxlat = abs(lat2-lat1); #solve a bug (when long1=long2)
    if long1==long2:
        az1=0; az2=m.pi;
        if auxlat>m.pi/2: 
            az1=3*m.pi/2;az2=m.pi/2
    
    az1=m.degrees(az1)
    az2=m.degrees(az2)
    
    return (az1,az2,s)
    
