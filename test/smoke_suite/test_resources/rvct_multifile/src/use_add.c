#include <e32def.h>
#include "add.h"

typedef unsigned char bool; // Just there to trap compiler error if --cpp was used

void use_add()
{
	TInt z = add(5,6);
}



