#include <stdio.h>
int
main (void)
{
  char n = '\n';
  char b = '\\';
  char q = '"';
  char const *p = "#include <stdio.h>%cint%cmain (void)%c{%c char n = '%cn';%c char b = '%c%c';%c char q = '%c';%c char const *p = %c%s%c;%c printf (p, n, n, n, n, b, n, b, b, n, q, n, q, p, q, n, n, n, n);%c return 0;%c}%c";
  printf(p, n, n, n, n, b, n, b, b, n, q, p, q, n, n, n, n);
  return 0;
}

