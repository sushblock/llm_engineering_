public class Main {
private static final long A = 1664525L;
private static final long C = 1013904223L;
private static final long MASK = 0xffffffffL;

private long value;

LCG(long seed) {
this.value = seed;
}

long next() {
this.value = (A * this.value + C) & MASK;
return this.value;
}
}

private static long maxSubarraySum(int n, long seed, int minVal, int maxVal) {
LCG lcg = new LCG(seed);
int range = maxVal - minVal + 1; // 21
long currentSum = 0;
long maxSum = Long.MIN_VALUE;
for (int i = 0; i < n; i++) {
long rnd = lcg.next();
int val = (int) (rnd % range) + minVal;
currentSum = Math.max(val, currentSum + val);
if (currentSum > maxSum) {
maxSum = currentSum;
}
}
return maxSum;
}

private static long totalMaxSubarraySum(int n, long initialSeed, int minVal, int maxVal) {
LCG lcg = new LCG(initialSeed);
long total = 0;
for (int i = 0; i < 20; i++) {
long seed = lcg.next();
total += maxSubarraySum(n, seed, minVal, maxVal);
}
return total;
}

public static void main(String[] args) {
int n = 10000;
long initialSeed = 42L;
int minVal = -10;
int maxVal = 10;

long start = System.nanoTime();
long result = totalMaxSubarraySum(n, initialSeed, minVal, maxVal);
long end = System.nanoTime();

double elapsed = (end - start) / 1_000_000_000.0;

System.out.println("Total Maximum Subarray Sum (20 runs): " + result);
System.out.printf("Execution Time: %.6f seconds%n", elapsed);
}
}