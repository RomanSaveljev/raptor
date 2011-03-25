// Trace compile macro and header
#include "OstTraceDefinitions.h"
#ifdef OST_TRACE_COMPILER_IN_USE
#include "trace_before_targetTraces.h"
#endif

#include "e32def.h"

char test[] = "test traces before target";

TInt E32Main()
{
	OstTrace0( TRACE_NORMAL, PLACE0, "Test TRACES before TARGET keyword" );
	return 0;
}
