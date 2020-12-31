#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

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