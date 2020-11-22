#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#define RUN 1

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
	if (!argv[1])
	{
		printf("Missing argument.\nUsage: ./build <filename>\nPress any key to continue. . . ");
		getch();
		return 0;
	}
	sprintf(buffer, "g++ %s.cpp -o %s", argv[1], argv[1]);
	for (int i = 3; i < argc; i++)
		sprintf(buffer + strlen(buffer), " %s", argv[i]);
	printf("%s\n", buffer);
	#if defined(WIN32)
		system("@set path=./MinGW/bin/;%path%");
	#endif
	system(buffer);
	if (strtol(argv[2], NULL, 10) == RUN)
	{
		#if defined(WIN32)
			sprintf(buffer, "%s", argv[1]);
		#else
			sprintf(buffer, "./%s", argv[1]);
		#endif
		int exitcode = system(buffer);
		printf("Process terminated with return code %d.\n", exitcode);
		printf("Press any key to continue. . . ");
		getch();
	}
	return 0;
}
