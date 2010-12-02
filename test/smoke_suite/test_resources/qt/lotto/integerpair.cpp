#include "integerpair.h"

#include <iostream>

IntegerPair::IntegerPair(): number(0), sortBy(0)
{
}

IntegerPair::IntegerPair(int num, int sort): number(num), sortBy(sort)
{
}

int IntegerPair::getSortBy(void) const
{
    return sortBy;
}

int IntegerPair::getNumber(void)
{
    return number;
}

bool IntegerPair::operator<(const IntegerPair& c) const
{
    return sortBy < c.getSortBy();
}
