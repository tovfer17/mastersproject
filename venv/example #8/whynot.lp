\ Model netflow
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  flow(instagram,_1.0,_2.0) + flow(twitter,_1.0,_2.0) + flow(zoom,_1.0,_2.0)
   + flow(netflix,_1.0,_2.0) + flow(instagram,_1.0,_3.0)
   + flow(twitter,_1.0,_3.0) + flow(zoom,_1.0,_3.0)
   + flow(netflix,_1.0,_3.0) + 2 flow(instagram,_2.0,_3.0)
   + 2 flow(twitter,_2.0,_3.0) + 2 flow(zoom,_2.0,_3.0)
   + 2 flow(netflix,_2.0,_3.0) + 4 flow(instagram,_2.0,_4.0)
   + 4 flow(twitter,_2.0,_4.0) + 4 flow(zoom,_2.0,_4.0)
   + 4 flow(netflix,_2.0,_4.0) + 8 flow(instagram,_3.0,_4.0)
   + 8 flow(twitter,_3.0,_4.0) + 8 flow(zoom,_3.0,_4.0)
   + 8 flow(netflix,_3.0,_4.0) + 5 flow(instagram,_3.0,_5.0)
   + 5 flow(twitter,_3.0,_5.0) + 5 flow(zoom,_3.0,_5.0)
   + 5 flow(netflix,_3.0,_5.0) + 3 flow(instagram,_4.0,_5.0)
   + 3 flow(twitter,_4.0,_5.0) + 3 flow(zoom,_4.0,_5.0)
   + 3 flow(netflix,_4.0,_5.0)
Subject To
 cap[0]: flow(instagram,_1.0,_2.0) + flow(twitter,_1.0,_2.0)
   + flow(zoom,_1.0,_2.0) + flow(netflix,_1.0,_2.0) <= 20
 cap[1]: flow(instagram,_1.0,_3.0) + flow(twitter,_1.0,_3.0)
   + flow(zoom,_1.0,_3.0) + flow(netflix,_1.0,_3.0) <= 10
 cap[2]: flow(instagram,_2.0,_3.0) + flow(twitter,_2.0,_3.0)
   + flow(zoom,_2.0,_3.0) + flow(netflix,_2.0,_3.0) <= 10
 cap[3]: flow(instagram,_2.0,_4.0) + flow(twitter,_2.0,_4.0)
   + flow(zoom,_2.0,_4.0) + flow(netflix,_2.0,_4.0) <= 20
 cap[4]: flow(instagram,_3.0,_4.0) + flow(twitter,_3.0,_4.0)
   + flow(zoom,_3.0,_4.0) + flow(netflix,_3.0,_4.0) <= 40
 cap[5]: flow(instagram,_3.0,_5.0) + flow(twitter,_3.0,_5.0)
   + flow(zoom,_3.0,_5.0) + flow(netflix,_3.0,_5.0) <= 10
 cap[6]: flow(instagram,_4.0,_5.0) + flow(twitter,_4.0,_5.0)
   + flow(zoom,_4.0,_5.0) + flow(netflix,_4.0,_5.0) <= 30
 Continuity(instagram,1.0): flow(instagram,_1.0,_2.0)
   + flow(instagram,_1.0,_3.0) = 15
 Continuity(instagram,2.0): - flow(instagram,_1.0,_2.0)
   + flow(instagram,_2.0,_3.0) + flow(instagram,_2.0,_4.0) = 0
 Continuity(instagram,3.0): - flow(instagram,_1.0,_3.0)
   - flow(instagram,_2.0,_3.0) + flow(instagram,_3.0,_4.0)
   + flow(instagram,_3.0,_5.0) = 0
 Continuity(instagram,4.0): - flow(instagram,_2.0,_4.0)
   - flow(instagram,_3.0,_4.0) + flow(instagram,_4.0,_5.0) = -15
 Continuity(instagram,5.0): - flow(instagram,_3.0,_5.0)
   - flow(instagram,_4.0,_5.0) = 0
 Continuity(twitter,1.0): flow(twitter,_1.0,_2.0) + flow(twitter,_1.0,_3.0)
   = 5
 Continuity(twitter,2.0): - flow(twitter,_1.0,_2.0)
   + flow(twitter,_2.0,_3.0) + flow(twitter,_2.0,_4.0) = 0
 Continuity(twitter,3.0): - flow(twitter,_1.0,_3.0)
   - flow(twitter,_2.0,_3.0) + flow(twitter,_3.0,_4.0)
   + flow(twitter,_3.0,_5.0) = 0
 Continuity(twitter,4.0): - flow(twitter,_2.0,_4.0)
   - flow(twitter,_3.0,_4.0) + flow(twitter,_4.0,_5.0) = 0
 Continuity(twitter,5.0): - flow(twitter,_3.0,_5.0)
   - flow(twitter,_4.0,_5.0) = -5
 Continuity(zoom,1.0): flow(zoom,_1.0,_2.0) + flow(zoom,_1.0,_3.0) = 0
 Continuity(zoom,2.0): - flow(zoom,_1.0,_2.0) + flow(zoom,_2.0,_3.0)
   + flow(zoom,_2.0,_4.0) = 10
 Continuity(zoom,3.0): - flow(zoom,_1.0,_3.0) - flow(zoom,_2.0,_3.0)
   + flow(zoom,_3.0,_4.0) + flow(zoom,_3.0,_5.0) = 0
 Continuity(zoom,4.0): - flow(zoom,_2.0,_4.0) - flow(zoom,_3.0,_4.0)
   + flow(zoom,_4.0,_5.0) = 0
 Continuity(zoom,5.0): - flow(zoom,_3.0,_5.0) - flow(zoom,_4.0,_5.0) = -10
 Continuity(netflix,1.0): flow(netflix,_1.0,_2.0) + flow(netflix,_1.0,_3.0)
   = 0
 Continuity(netflix,2.0): - flow(netflix,_1.0,_2.0)
   + flow(netflix,_2.0,_3.0) + flow(netflix,_2.0,_4.0) = 0
 Continuity(netflix,3.0): - flow(netflix,_1.0,_3.0)
   - flow(netflix,_2.0,_3.0) + flow(netflix,_3.0,_4.0)
   + flow(netflix,_3.0,_5.0) = 5
 Continuity(netflix,4.0): - flow(netflix,_2.0,_4.0)
   - flow(netflix,_3.0,_4.0) + flow(netflix,_4.0,_5.0) = 0
 Continuity(netflix,5.0): - flow(netflix,_3.0,_5.0)
   - flow(netflix,_4.0,_5.0) = -5
Bounds
End
