#include <e32def.h>
#include "sub.h"

typedef unsigned char bool; // Just there to trap compiler error if --cpp was used

void use_sub()
{
	TInt z = sub(6,1);
}



