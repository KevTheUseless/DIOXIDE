#include "build.h"

char buffer[1073741824];

int main(int argc, char **argv)
{
	if (argc < 2)
	{
		printf("Missing argument.\nUsage: ./build <filename> <compiler flags>\nPress any key to continue. . . ");
		getch();
		return 0;
	}
	sprintf(buffer, "g++ %s.cpp -o %s", argv[1], argv[1]);
	for (int i = 2; i < argc; i++)
		sprintf(buffer + strlen(buffer), " %s", argv[i]);
	#if defined(WIN32)
		system("@set path=./compilers/MinGW/bin/;%path%");
	#endif
	system(buffer);
	return 0;
}
