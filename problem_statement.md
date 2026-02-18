Time Limit: **4 seconds**

Memory Limit: **32 MB**

On a line there are $n$ outposts at integer coordinates $a_1, a_2, \dots, a_n$ (sorted non-decreasing) and $m$ lantern posts at integer coordinates $b_1, b_2, \dots, b_m$ (sorted non-decreasing).

If a lantern at coordinate $x$ is turned on with radius $s \ge 0$, it illuminates all outposts whose coordinates lie in the segment $[x-s, x+s]$. All turned-on lanterns must use the same integer radius $s$.

Lanterns can only be turned on in bursts:

- You may perform at most $t$ bursts.
- In one burst, you choose a contiguous block of lantern indices $[l..r]$ (1-based) and turn on all lanterns $b_l, b_{l+1}, \dots, b_r$.
- The activation effort of a burst equals its length $r-l+1$.
- The total activation effort is the sum of burst lengths over all bursts, and it must be at most $k$.
  (Bursts may overlap; overlapping indices still contribute again to the effort.)

Find the minimum integer radius $s$ such that it is possible to illuminate every outpost under these rules.

**Input Format:-**

The first line contains four integers $n, m, k, t$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains $m$ integers $b_1, b_2, \dots, b_m$.

**Output Format:-**

Print one integer: the minimum possible radius $s$.

**Constraints:-**

- $1 \le n, m \le 100000$
- $1 \le k \le m$
- $1 \le t \le 30$
- $-10^9 \le a_i, b_j \le 10^9$
- Arrays $a$ and $b$ are sorted non-decreasing
**Examples:-**
 - **Input:**
```
4 2 1 1
0 0 1 1
0 2
```

 - **Output:**
```
1
```

 - **Input:**
```
4 3 2 2
-3 -1 1 3
-2 0 2
```

 - **Output:**
```
1
```

**Note:-**  

In the first example, we may use one burst (since $t=1$) and the total effort must be at most $k=1$, so we can turn on exactly one lantern.  
Choosing the lantern at $x=0$ with radius $s=1$ illuminates the segment $[-1,1]$, which covers all outposts at coordinates $0,0,1,1$. Hence the minimum possible radius is $1$.

In the first example, we can use up to $t=2$ bursts with total effort at most $k=2$.  
With radius $s=1$, turn on lanterns at $x=-2$ and $x=2$ using two bursts of length $1$ each (total effort $2$). They illuminate $[-3,-1]$ and $[1,3]$, covering all outposts $-3,-1,1,3$. Therefore the minimum radius is $1$.