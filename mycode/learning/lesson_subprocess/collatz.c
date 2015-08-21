#include <stdio.h>

/* A program to run through the numbers, counting how long it takes
the Collatz process to reach 1. 
*/

int main()
{
  long long start = 1L;
  long long number = 0L;
  long long counter = 0L;
  long long limit = 100000000L;

  while (start < limit)
  {
    number = start;
    counter = 0L;

    while (number != 1L)
    {
      /* printf("\t%lld\n", number); */
      counter++;
      if (number % 2L == 0L)
      {
        number /= 2L;
      } else {
        number *= 3L;
        number += 1L;
      }
    }

    printf("%lld,%lld\n", start, counter);

    start++;
  }
}
