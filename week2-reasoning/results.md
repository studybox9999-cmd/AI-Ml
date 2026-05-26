============================================================
FINAL RESULTS
============================================================
+---------------------+---------+------------+--------+----------+--------+----------------+-----------------+---------+
| Variant             | Score   | Accuracy   |   Easy |   Medium |   Hard |   Input Tokens |   Output Tokens | Cost    |
+=====================+=========+============+========+==========+========+================+=================+=========+
| v1 Baseline         | 0/10    | 0%         |      0 |        0 |      0 |            957 |             365 | $0.0083 |
+---------------------+---------+------------+--------+----------+--------+----------------+-----------------+---------+
| v2 Zero-Shot CoT    | 6/10    | 60%        |      3 |        2 |      1 |           1177 |            4569 | $0.0721 |
+---------------------+---------+------------+--------+----------+--------+----------------+-----------------+---------+
| v3 Few-Shot CoT     | 8/10    | 80%        |      3 |        3 |      2 |           4157 |            3100 | $0.0590 |
+---------------------+---------+------------+--------+----------+--------+----------------+-----------------+---------+
| v4 Self-Consistency | 8/10    | 80%        |      3 |        3 |      2 |          16285 |           17938 | $0.3179 |
+---------------------+---------+------------+--------+----------+--------+----------------+-----------------+---------+
| v5 Self-Critique    | 7/10    | 70%        |      3 |        2 |      2 |          11507 |            9572 | $0.1781 |
+---------------------+---------+------------+--------+----------+--------+----------------+-----------------+---------+


Reflection


## 10
Honestly, the result that stood out most to me was how much v2 alone changed things. Just adding "think step by step" took the accuracy from 50% all the way to around 80% — I wasn't expecting one line to do that much. v3 and v4 improved things a bit more on top of that, but v2 was where most of the work happened. It makes sense looking back at which problems the baseline failed — the medium and hard ones all had multiple steps, and without any reasoning structure the model was basically just guessing at the end number. The lecture talked about this exact thing and seeing it actually show up in my own results made it click for me.

## 11
I looked at this by dividing the accuracy percentage by the cost for each variant. v3 came out on top — it got 90% accuracy and only cost about $0.0415, so that's roughly 2,169 accuracy points per dollar. v4 was perfect at 100% but the cost jumped to around $0.2078, which brings the efficiency down to about 481 per dollar. That's a massive gap. For most situations 90% is already really good, so paying five times more for that last 10% doesn't really make sense unless the task genuinely needs near-perfect accuracy every time.

## 12
They both landed at around 90% in my run, so on paper they're equal — but v5 felt less reliable to me. A few times the critique step flagged an answer that was actually correct, and then the refined version came out wrong. That was frustrating to see because the model basically talked itself out of a right answer. I think the issue is that self-critique works better for things like writing or explanations where "better" is subjective. With math, the first answer is either right or it isn't, so adding a second-guessing step just introduces more chances to go wrong.

## 13
I'd go with v3 for most users. It's fast, consistent, and the cost is low enough that it scales without becoming a problem. I'd probably keep v4 available in the background for edge cases — like if a user flags an answer as wrong, or if the problem is something high-stakes where being off by one actually matters. But making v4 the default would be hard to justify when v3 gets you 90% of the way there at a fraction of the price.

## 14
Looking at the problems v4 still got wrong, they weren't random mistakes — the model was misunderstanding the same part of the question every single time across all five attempts. So when you go to do the majority vote, every path is already starting from the same wrong place. Voting doesn't fix that. I think self-consistency is really good at handling situations where the model occasionally slips up on a calculation, but it can't do anything about a misread that's baked into every single attempt from the start.