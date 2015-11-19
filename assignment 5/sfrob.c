#include <stdio.h>
#include <stdlib.h>

int frobcmp(char const *a, char const *b)
{
  const char *one = *(const char **)a;
  const char *two = *(const char **)b;
  while (1)
    {
      int cmpFirst = (int) *one;
      int cmpSecond = (int) *two;

      if(cmpFirst == ' ' && cmpSecond == ' ')
	return 0;
      if(cmpFirst == ' ')
	return -1;
      if (cmpSecond == ' ')
	return 1;

      if((cmpFirst ^ 42) > (cmpSecond ^ 42))
	return 1;
      if((cmpFirst ^ 42) < (cmpSecond ^ 42))
	return -1;

      one++;
      two++;
    }
}

int wrap_function(const void *a, const void *b)
{
  return frobcmp(a, b);
}

int main()
{
  int size = 2048;
  int count = 0;
  char *array = (char*)malloc(size);
  int input;

  while(1)
    {
      input = getchar();
      if(input == EOF)
	break;
      array[count] = (char)input;
      count++;
      if(count != size)
	continue;
      size = size * 2;
      array = (char*)realloc(array, size);
      if(array == NULL)
	{
	  fprintf(stderr, "Failed to allocate memory");
	  exit(1);
	}
    }
  if(count == 0)
    exit(0);
  if(array[count - 1] != ' ')
    {
      if(count == size)
	{
	  size = size * 2;
	  array = (char*)realloc (array, size);
	  if(array == NULL)
	    {
	      fprintf(stderr, "Failed to allocate memory");
	      exit(1);
	    }
	}
      array[count] = ' ';
      count++;
    }
  int number = 0;
  int i = 0;
  for(; i < count; i++)
    {
      if(array[i] == ' ')
	number++;
    }
  char **words = (char **)malloc(sizeof(char*)*number);
  if(words == NULL)
    {
      fprintf(stderr, "Failed to allocate memory");
      exit(1);
    }
  char *loop = array;
  int j = 0;
  int k = 0;
  for(; j < number; j++)
    {
      words[k] = loop;
      k++;
      while(*loop != ' ')
	loop++;
      loop++;
    }
  qsort(words, k,  sizeof(char*), wrap_function);
  int l=0;
  for(; l < number; l++)
    {
      char *temp = words[l];
      while(*temp != ' ')
	{
	  printf("%c", *temp);
	  temp++;
	}
      printf("%c", *temp);
    }
  free(array);
  free(words);
  exit(0);
}


