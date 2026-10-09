# kept spans in old (full) timeline; (start,end,gap_before_in_new)
KEEP=[(0.75,5.60,0.0),(5.85,12.45,0.14),(16.25,22.90,0.18),(23.80,32.65,0.16),(33.35,36.70,0.16),(37.30,43.50,0.12),
      (44.50,50.20,0.18),(51.05,54.00,0.18),(55.10,58.05,0.14),(64.40,68.50,0.2),(68.85,72.95,0.14),(85.30,91.80,0.2),(92.25,95.15,0.12),
      (108.00,118.20,0.22),(119.00,123.60,0.16),(124.35,130.20,0.2)]
SEGS=[]; cur=0.0
for a,b,g in KEEP:
    cur+=g; SEGS.append((cur,cur+(b-a),a,b)); cur+=b-a
TOTAL=round(cur+0.35,2)
def n2o(t):
    for n0,n1,o0,o1 in SEGS:
        if n0<=t<n1+1e-6: return o0+(t-n0),SEGS.index((n0,n1,o0,o1))
    return SEGS[-1][3],len(SEGS)-1
def o2n(t):
    for n0,n1,o0,o1 in SEGS:
        if o0-0.05<=t<=o1+0.05: return n0+(t-o0)
    return None
if __name__=="__main__": print(TOTAL); [print(s) for s in SEGS]
