1.At first I did not know where to start and how to implement pthread_create.
After I read through piazza. I started to understand that I have to use multiple threads to run through the loops in the function.
Moreover, I learned how to use pthread_create and pthread_join.
2.I declare lots of global variables, since it makes my thread function to communicate with main function.
If I declare those variables in my thread function, I will have to declare them several times, which may slow down the program.
3.After I finish my modification, there is a [check] Error 1.
I scanned through my code over and over again, and finally found out that the width and length for this program is 131 which is not divisible by 2, 4, and 8.
Therefore, there is an error when I calculated how many loops a thread should run, since I ignored the remainder.
4.After the above modification, there is still a clock skew error.
However, it works correctly after I restarted my putty.

