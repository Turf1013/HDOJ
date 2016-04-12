(1) binary search the delta length of left value.
we can enumerate all the possible factor of two sources due to expressions,
then we can get all the possible result.
we nearsearch the trie and insert into then update the ending-point of trie.

After all possible result nearsearch, then we dfs the trie
to find the most fit rvalue.

we enumerate the factor of left value using order-dfs:
'*' then '0-9' (without leading zero), no need to make '0-9' to '*'.

max-enumerate = 11**4 = 14641
possible-result = 100*100 = 10000
h(trie) = 4
n(binary-search) = 4
nearseach = 16

=====================
18:38 binary search is not write,
because somehow, lvalue may need 3 change but we can keep rvalue still,
or change 2 but we change 2 rvalue.
just enumerate for 0 to 4 seems right.