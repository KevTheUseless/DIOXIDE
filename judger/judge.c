#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

#define AC 0
#define WA 1
#define TLE 2
#define MLE 3
#define RE 4

char buffer[1073741824];
char oufLine[1073741824], ansLine[1073741824];

#ifdef WIN32
	#define VIEWER "type"
#else
	#define VIEWER "cat"
#endif

void strip(char *s)
{
	for (int i = strlen(s) - 1; i >= 0; i--)
	{
		if (!isprint(s[i]) || isspace(s[i]))
			s[i] = '\0';
	}
}

int main(int argc, char **argv)
{
	if (argc < 5)
	{
		printf("Missing argument.\nUsage: ./judge <filename> <inputfile> <outputfile> <time limit> <memory limit>\n");
		return -1;
	}

	freopen("output1.temp", "w", stdout);
	sprintf(buffer, "%s %s | procgov --timeout %s -q %s", VIEWER, argv[2], argv[4], argv[1]);
	int ret1 = system(buffer);
	freopen("output2.temp", "w", stdout);
	sprintf(buffer, "%s %s | procgov --timeout %s -q %s", VIEWER, argv[2], argv[5], argv[1]);
	int ret2 = system(buffer);

	if (!ret1)
		return TLE;
	if (!ret2)
		return MLE;
	if (ret1 || ret2)
		return RE;

	FILE *ouf = fopen("output1.temp", "r");
	FILE *ans = fopen(argv[3], "r");

	while (fgets(oufLine, 1073741824, ouf) != NULL && fgets(ansLine, 1073741824, ans) != NULL)
	{
		strip(oufLine);
		strip(ansLine);
		if (oufLine[0] == '\0' && ansLine[0] == '\0')
			continue;
		if (strlen(oufLine) != strlen(ansLine))
			return WA;
		int len = strlen(oufLine);
		for (int i = 0; i < len; i++)
		{
			if (oufLine[i] != ansLine[i])
				return WA;
		}
	}

	fclose(ouf);
	fclose(ans);
	fclose(stdin);
	fclose(stdout);
	return AC;
}