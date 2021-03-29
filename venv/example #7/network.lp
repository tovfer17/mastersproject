\ Model maximum network flow
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  flow[s,a] + flow[s,b] + flow[s,c]
Subject To
 node[a]: flow[s,a] - flow[a,d] - flow[a,b] = 0
 node[b]: flow[s,b] + flow[a,b] - flow[b,e] = 0
 node[c]: flow[s,c] - flow[c,e] - flow[c,d] = 0
 node[d]: - flow[d,t] + flow[a,d] + flow[c,d] = 0
 node[e]: - flow[e,t] + flow[b,e] + flow[c,e] = 0
Bounds
 -3 <= flow[s,a] <= 3
 -1 <= flow[s,b] <= 1
 -4 <= flow[d,t] <= 4
 -1 <= flow[s,c] <= 1
 -1 <= flow[e,t] <= 1
 -1 <= flow[a,d] <= 1
 -1 <= flow[a,b] <= 1
 -3 <= flow[b,e] <= 3
 -4 <= flow[c,e] <= 4
 -4 <= flow[c,d] <= 4
End
