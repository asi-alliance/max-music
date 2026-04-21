import json
v = json.load(open(chr(39)+chr(118)+chr(111)+chr(114)+chr(111)+chr(110)+chr(111)+chr(105)+chr(95)+chr(49)+chr(57)+chr(101)+chr(100)+chr(111)+chr(46)+chr(106)+chr(115)+chr(111)+chr(110)+chr(39)))
for x in v:
    b=chr(35)*min(int(x[chr(39)+chr(101)+chr(110)+chr(101)+chr(114)+chr(103)+chr(121)+chr(39)]/50),50)
    s=x[chr(39)+chr(115)+chr(116)+chr(101)+chr(112)+chr(39)]
    e=x[chr(39)+chr(101)+chr(110)+chr(101)+chr(114)+chr(103)+chr(121)+chr(39)]
    a=x[chr(39)+chr(97)+chr(116)+chr(116)+chr(114)+chr(97)+chr(99)+chr(116)+chr(111)+chr(114)+chr(39)]
    m=chr(32)+chr(42) if e<50 else chr(39)+chr(39)
    print(chr(115)+chr(116)+chr(101)+chr(112),str(s).rjust(2),b.ljust(50),chr(69)+chr(61),str(int(e)).rjust(6),a,m)
