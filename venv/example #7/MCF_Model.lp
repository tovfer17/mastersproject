\ Model netflow
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  5 flow[netflix,c,f] + 6 flow[netflix,f,b] + 7 flow[netflix,b,g]
   + 2 flow[netflix,d,g] + flow[netflix,a,d] + 4 flow[netflix,f,laptop]
   + 8 flow[netflix,a,e] + 4 flow[netflix,c,e] + 3 flow[netflix,g,mobile]
   + 5 flow[instagram,c,f] + 6 flow[instagram,f,b] + 7 flow[instagram,b,g]
   + 2 flow[instagram,d,g] + flow[instagram,a,d]
   + 4 flow[instagram,f,laptop] + 8 flow[instagram,a,e]
   + 4 flow[instagram,c,e] + 3 flow[instagram,g,mobile]
Subject To
 cap[c,_f]: flow[netflix,c,f] + flow[instagram,c,f] <= 90
 cap[f,_b]: flow[netflix,f,b] + flow[instagram,f,b] <= 50
 cap[b,_g]: flow[netflix,b,g] + flow[instagram,b,g] <= 46
 cap[d,_g]: flow[netflix,d,g] + flow[instagram,d,g] <= 140
 cap[a,_d]: flow[netflix,a,d] + flow[instagram,a,d] <= 130
 cap[f,_laptop]: flow[netflix,f,laptop] + flow[instagram,f,laptop] <= 40
 cap[a,_e]: flow[netflix,a,e] + flow[instagram,a,e] <= 112
 cap[c,_e]: flow[netflix,c,e] + flow[instagram,c,e] <= 120
 cap[g,_mobile]: flow[netflix,g,mobile] + flow[instagram,g,mobile] <= 100
 node[netflix,c]: - flow[netflix,c,f] - flow[netflix,c,e]
   = -1.785714285714286
 node[netflix,d]: - flow[netflix,d,g] + flow[netflix,a,d]
   = 1.785714285714286
 node[netflix,e]: flow[netflix,a,e] + flow[netflix,c,e]
   = 0.3720238095238095
 node[netflix,f]: flow[netflix,c,f] - flow[netflix,f,b]
   - flow[netflix,f,laptop] = 0.4092261904761905
 node[netflix,g]: flow[netflix,b,g] + flow[netflix,d,g]
   - flow[netflix,g,mobile] = 0.1711309523809524
 node[instagram,c]: - flow[instagram,c,f] - flow[instagram,c,e]
   = -3.273809523809524
 node[instagram,d]: - flow[instagram,d,g] + flow[instagram,a,d] = 0.46875
 node[instagram,e]: flow[instagram,a,e] + flow[instagram,c,e]
   = 0.037202380952381
 node[instagram,f]: flow[instagram,c,f] - flow[instagram,f,b]
   - flow[instagram,f,laptop] = 0.0267857142857143
 node[instagram,g]: flow[instagram,b,g] + flow[instagram,d,g]
   - flow[instagram,g,mobile] = 1.785714285714286
Bounds
End
