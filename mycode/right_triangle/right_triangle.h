#ifndef __RIGHT_TRIANGLE_H__
#	define __RIGHT_TRIANGLE_H__



enum LEGS { SIDE1 = 1, SIDE2 = 2, HYPOTENUSE = 4};

double calculateLegLength( double side1, double side2, double hypotenuse,
							size_t givenLegs);













#endif // __RIGHT_TRIANGLE_H__
