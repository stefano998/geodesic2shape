def deg2dms (type,x):
    if type=="lat":
        dx = int(x)
        auxmin = abs((x-dx)*60)
        mx = int(auxmin)
        sx = abs((auxmin-mx)*60)
        hx="N"
        if x < 0:
            hx = "S"
        sx = round (sx,4)
        if sx == 60:
            mx = mx+1
            sx = 0.0
        if mx == 60:
            dx = dx+1
            mx = 0
        strx=str(abs(dx))+"  "+str(mx)+"  "+str(sx)+"  "+str(hx)

    if type=="long":
        dx = int(x)
        auxmin = abs((x-dx)*60)
        mx = int(auxmin)
        sx = abs((auxmin-mx)*60)
        hx="E"
        if x < 0:
            hx = "W"
        sx = round (sx,4)
        if sx == 60:
            mx = mx+1
            sx = 0.0
        if mx == 60:
            dx = dx+1
            mx = 0
        strx=str(abs(dx))+"  "+str(mx)+"  "+str(sx)+"  "+str(hx)

    if type=="az":
        dx = int(x)
        auxmin = abs((x-dx)*60)
        mx = int(auxmin)
        sx = abs((auxmin-mx)*60)
        sx = round (sx,4)
        if sx == 60:
            mx = mx+1
            sx = 0.0
        if mx == 60:
            dx = dx+1
            mx = 0
        strx=str(dx)+"  "+str(mx)+"  "+str(sx)

    return (strx)



