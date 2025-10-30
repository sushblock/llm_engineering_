// Fast JavaScript port of the given Python code
(function () {
'use strict';

// Linear Congruential Generator (LCG) - identical to the Python version
function lcg(seed, a, c, m) {
let value = seed | 0;
return function () {
// All operations performed as signed 32-bit to match Python's int mod 2**32 behavior
value = Math.imul(a, value) + c;
// Keep value in 32-bit range
value |= 0;
return value >>> 0; // unsigned 32-bit
};
}

// Compute the maximum subarray sum using the same O(n^2) algorithm as the Python code
// to produce identical results.
function maxSubarraySum(arr, minVal, maxVal) {
const n = arr.length;
// Initialize with the smallest possible safe integer (same as Python's float('-inf') semantics)
let maxSum = -Infinity;
let i = 0;
for (; i < n; ++i) {
let currentSum = 0;
let j = i;
for (; j < n; ++j) {
currentSum += arr[j];
if (currentSum > maxSum) maxSum = currentSum;
}
}
return maxSum;
}

// Total of 20 runs using fresh LCG sequences, identical to Python
function totalMaxSubarraySum(n, initialSeed, minVal, maxVal) {
const span = (maxVal - minVal + 1) | 0;
let totalSum = 0;
let g = lcg(initialSeed, 1664525, 1013904223, 0x100000000);
let run = 20;
while (run--) {
const seed = g();
// Build LCG sequence for this run
const gen = lcg(seed, 1664525, 1013904223, 0x100000000);
// Use Int32Array for tight loops
const arr = new Int32Array(n);
let i = 0;
for (; i < n; ++i) {
const v = gen();
arr[i] = (v % span) + minVal;
}
totalSum += maxSubarraySum(arr, minVal, maxVal);
}
return totalSum;
}

// Parameters (kept identical to the Python code)
const n = 10000;
const initialSeed = 42;
const minVal = -10;
const maxVal = 10;

// High-resolution timing
const startTime = (typeof performance !== 'undefined' && performance.now) ? performance.now() : Date.now();
const result = totalMaxSubarraySum(n, initialSeed, minVal, maxVal);
const endTime = (typeof performance !== 'undefined' && performance.now) ? performance.now() : Date.now();

const elapsedMs = endTime - startTime;

// Output in the same format as the Python script
console.log("Total Maximum Subarray Sum (20 runs):", result);
console.log("Execution Time: " + (elapsedMs / 1000).toFixed(6) + " seconds");
})();