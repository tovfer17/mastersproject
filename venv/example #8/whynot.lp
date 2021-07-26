\ Model netflow
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  flow[instagram,1.0,2.0] + flow[instagram,1.0,3.0]
   + 2 flow[instagram,2.0,3.0] + 3 flow[instagram,4.0,5.0]
   + 8 flow[instagram,3.0,4.0] + 4 flow[instagram,2.0,4.0]
   + 5 flow[instagram,3.0,5.0]
Subject To
 cap[1.0,_2.0]: flow[instagram,1.0,2.0] + flow[twitter,1.0,2.0]
   + flow[zoom,1.0,2.0] + flow[netflix,1.0,2.0] <= 20
 cap[1.0,_3.0]: flow[instagram,1.0,3.0] + flow[twitter,1.0,3.0]
   + flow[zoom,1.0,3.0] + flow[netflix,1.0,3.0] <= 10
 cap[2.0,_3.0]: flow[instagram,2.0,3.0] + flow[twitter,2.0,3.0]
   + flow[zoom,2.0,3.0] + flow[netflix,2.0,3.0] <= 10
 cap[4.0,_5.0]: flow[instagram,4.0,5.0] + flow[twitter,4.0,5.0]
   + flow[zoom,4.0,5.0] + flow[netflix,4.0,5.0] <= 30
 cap[3.0,_4.0]: flow[instagram,3.0,4.0] + flow[twitter,3.0,4.0]
   + flow[zoom,3.0,4.0] + flow[netflix,3.0,4.0] <= 40
 cap[2.0,_4.0]: flow[instagram,2.0,4.0] + flow[twitter,2.0,4.0]
   + flow[zoom,2.0,4.0] + flow[netflix,2.0,4.0] <= 20
 cap[3.0,_5.0]: flow[instagram,3.0,5.0] + flow[twitter,3.0,5.0]
   + flow[zoom,3.0,5.0] + flow[netflix,3.0,5.0] <= 10
 Continuity(instagram,1.0): = 15
 Continuity(instagram,2.0): flow[instagram,1.0,2.0]
   + flow[instagram,1.0,3.0] = 0
 Continuity(instagram,3.0): - flow[instagram,1.0,2.0]
   + flow[instagram,2.0,3.0] + flow[instagram,2.0,4.0] = 0
 Continuity(instagram,4.0): - flow[instagram,1.0,3.0]
   - flow[instagram,2.0,3.0] + flow[instagram,3.0,4.0]
   + flow[instagram,3.0,5.0] = -15
 Continuity(instagram,5.0): flow[instagram,4.0,5.0]
   - flow[instagram,3.0,4.0] - flow[instagram,2.0,4.0] = 0
 Continuity(twitter,1.0): = 5
 Continuity(twitter,2.0): flow[twitter,1.0,2.0] + flow[twitter,1.0,3.0]
   = 0
 Continuity(twitter,3.0): - flow[twitter,1.0,2.0] + flow[twitter,2.0,3.0]
   + flow[twitter,2.0,4.0] = 0
 Continuity(twitter,4.0): - flow[twitter,1.0,3.0] - flow[twitter,2.0,3.0]
   + flow[twitter,3.0,4.0] + flow[twitter,3.0,5.0] = 0
 Continuity(twitter,5.0): flow[twitter,4.0,5.0] - flow[twitter,3.0,4.0]
   - flow[twitter,2.0,4.0] = -5
 Continuity(zoom,1.0): = 0
 Continuity(zoom,2.0): flow[zoom,1.0,2.0] + flow[zoom,1.0,3.0] = 10
 Continuity(zoom,3.0): - flow[zoom,1.0,2.0] + flow[zoom,2.0,3.0]
   + flow[zoom,2.0,4.0] = 0
 Continuity(zoom,4.0): - flow[zoom,1.0,3.0] - flow[zoom,2.0,3.0]
   + flow[zoom,3.0,4.0] + flow[zoom,3.0,5.0] = 0
 Continuity(zoom,5.0): flow[zoom,4.0,5.0] - flow[zoom,3.0,4.0]
   - flow[zoom,2.0,4.0] = -10
 Continuity(netflix,1.0): = 0
 Continuity(netflix,2.0): flow[netflix,1.0,2.0] + flow[netflix,1.0,3.0]
   = 0
 Continuity(netflix,3.0): - flow[netflix,1.0,2.0] + flow[netflix,2.0,3.0]
   + flow[netflix,2.0,4.0] = 5
 Continuity(netflix,4.0): - flow[netflix,1.0,3.0] - flow[netflix,2.0,3.0]
   + flow[netflix,3.0,4.0] + flow[netflix,3.0,5.0] = 0
 Continuity(netflix,5.0): flow[netflix,4.0,5.0] - flow[netflix,3.0,4.0]
   - flow[netflix,2.0,4.0] = -5
Bounds
End
