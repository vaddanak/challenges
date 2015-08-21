#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
#include <sys/errno.h>
#include <math.h>

/*
  This program iterates the unit square under the iteration
  x' = x + y
  y' = y + y*epsilon*sin(2pi*x)
  with both calculations modulo 1.0.

  The system iterates a series of points whose initial positions form
  an nx by ny regular grid on the unit square.  Each point is iterated
  "n_iter" many times.

 */

int main
(
 int argc,
 char **argv
 )
{
  long nxl = 100L;
  long nyl = 100L;
  long n_iter = 100L;
  double epsilon = 0.0;

  const double twopi = 2.0*M_PI;

  long ix = 0L;
  long iy = 0L;
  double x = 0.0;
  double y = 0.0;
  double xx = 0.0;
  double yy = 0.0;
  long count = 0L;
  double junk = 0.0; /* Used to discard integer part in modf() */

  /* Process the user's command line arguments. */
  if (argc != 2)
    {
      fprintf(stderr, "Wrong number of arguments!\n1 expected, %d found.\nUsage: %s epsilon\n", (argc-1), argv[0]);
      exit(1);
    }

  epsilon = strtod(argv[1], NULL);
  if (0 != errno)
    {
      perror("Invalid epsilon: ");
      exit(1);
    }

  /* Run */
  printf("%ld,%f\n", n_iter, epsilon);
  for (ix = 0L; ix < nxl; ix += 1L)
    {
      for (iy = 0L; iy < nyl; iy += 1L)
	{
	  x = ((double)ix)/((double)nxl);
	  y = ((double)iy)/((double)nyl);
	  for (count=0L; count < n_iter; count += 1L)
	    {
	      xx = modf(1.0 + x + y, &junk);
	      yy = modf(1.0 + y + epsilon*y*sin(twopi*x), &junk);
	      x = xx;
	      y = yy;
	    }
	  printf("%f,%f\n", x, y);
	}
    }

  /* All done! */
  exit(0);
}
