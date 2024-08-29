# def fib_seq(n):
#     if n <= 0: # Base limit incase of a infinite loop
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         return fib_seq(n - 1) + fib_seq(n - 2)


def fibonacci(n):
  """Calculates the nth Fibonacci number using dynamic programming."""
  if n <= 1:
    return n

  fib = [0, 1]
  for i in range(2, n + 1):
    fib.append(fib[i - 1] + fib[i - 2])
  return fib

# Example usage:
print(fibonacci(10))  # Output: 55
