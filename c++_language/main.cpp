#include <iostream>

int main()
{
  int number;
  scanf("%d", &number);
  printf("%d\n", number / 100 + number / 10 % 10 + number % 10);
}