
#include <iostream>
#include <chrono>

double calculate(int iterations, double param1, double param2) {
    double result = 1.0;
    for (int i = 1; i <= iterations; ++i) {
        double j1 = i * param1 - param2;
        result -= (1.0 / j1);
        double j2 = i * param1 + param2;
        result += (1.0 / j2);
    }
    return result;
}

int main() {
    auto start_time = std::chrono::high_resolution_clock::now();
    
    double result = calculate(200000000, 4.0, 1.0) * 4.0;
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    
    printf("Result: %.12f\n", result);
    printf("Execution Time: %.6f seconds\n", duration.count() / 1000000.0);
    
    return 0;
}
