#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

#define BUILD		0
#define RUN			1
#define BUILDRUN	2

#if defined(WIN32)
	#include <conio.h>
#else
	/* 
	 * Code from https://stackoverflow.com/questions/3276546/how-to-implement-getch-function-of-c-in-linux 
	 * by user Shobhit, edited by user Isaac.
	 */
	#include <termios.h>
	#include <unistd.h>

	/* reads from keypress, doesn't echo */
	int getch(void)
	{
		struct termios oldattr, newattr;
		int ch;
		tcgetattr( STDIN_FILENO, &oldattr );
		newattr = oldattr;
		newattr.c_lflag &= ~( ICANON | ECHO );
		tcsetattr( STDIN_FILENO, TCSANOW, &newattr );
		ch = getchar();
		tcsetattr( STDIN_FILENO, TCSANOW, &oldattr );
		return ch;
	}
#endif

char buffer[1073741824];

int main(int argc, char **argv)
{
	if (argc < 3)
	{
		printf("Missing argument.\nUsage: ./build <runflag> <filename> <compiler flags>\nPress any key to continue. . . ");
		getch();
		return 0;
	}
	int runflag = strtol(argv[1], NULL, 10);
	if (runflag == BUILD || runflag == BUILDRUN)
	{
		sprintf(buffer, "g++ %s.cpp -o %s", argv[2], argv[2]);
		for (int i = 3; i < argc; i++)
			sprintf(buffer + strlen(buffer), " %s", argv[i]);
		#if defined(WIN32)
			system("@set path=./MinGW/bin/;%path%");
		#endif
		system(buffer);
	}
	if (runflag == RUN || runflag == BUILDRUN)
	{
		#if defined(WIN32)
			sprintf(buffer, "%s", argv[2]);
		#else
			sprintf(buffer, "./%s", argv[2]);
		#endif
		clock_t t0 = clock();
		int exitcode = system(buffer);
		clock_t t1 = clock();
		printf("\nProcess terminated with return code %d after %f seconds.\n", exitcode, ((double) (t1 - t0) / CLOCKS_PER_SEC));
		printf("Press any key to continue. . . ");
		getch();
	}
	return 0;
}
