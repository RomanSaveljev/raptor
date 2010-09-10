#ifndef INTEGERPAIR_H
#define INTEGERPAIR_H

class IntegerPair
{
public:
    IntegerPair();
    IntegerPair(int num, int sort);
    bool operator<(const IntegerPair&) const;
    int getSortBy(void) const;
    int getNumber(void);

private:
    int number;
    int sortBy;
};

#endif // INTEGERPAIR_H

