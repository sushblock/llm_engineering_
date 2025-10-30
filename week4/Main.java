public final class Main {
private static final int A = 4;
private static final int B = 1;

public static void main(String[] args) {
final int iterations = 200_000_000;
final long startNanos = System.nanoTime();

double result = 1.0;
final int a = A;
final int b = B;

// Fast dependency-reducing form: result += (a/(i*a - b) - a/(i*a + b))
for (int i = 1; i <= iterations; i++) {
final int denom1 = i * a - b;
final int denom2 = i * a + b;
// Reciprocal division
result += (a / (double) denom1) - (a / (double) denom2);
}

final long endNanos = System.nanoTime();
final double elapsedSeconds = (endNanos - startNanos) / 1_000_000_000.0;

System.out.printf("Result: %.12f%n", result);
System.out.printf("Execution Time: %.6f seconds%n", elapsedSeconds);
}
}