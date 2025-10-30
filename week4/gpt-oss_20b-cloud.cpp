#include <bits/stdc++.h>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    const long long ITERATIONS = 200000000;
    const long long P1 = 4;
    const long long P2 = 1;

    auto start = std::chrono::high_resolution_clock::now();

    double result = 1.0;
    long long fouri = P1;  // i * P1 for i = 1
    for (long long i = 1; i <= ITERATIONS; ++i) {
        long long j = fouri - P2;   // j = i*P1 - P2
        result -= 1.0 / j;
        j = fouri + P2;             // j = i*P1 + P2
        result += 1.0 / j;
        fouri += P1;                // prepare for next i
    }
    result *= 4.0;

    auto end = std::chrono::high_resolution_clock::now();
    double exec_time = std::chrono::duration<double>(end - start).count();

    std::cout << std::fixed << std::setprecision(12);
    std::cout << "Result: " << result << '\n';
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "Execution Time: " << exec_time << " seconds\n";

    return 0;
}
