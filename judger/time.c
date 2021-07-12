#include "build.h"

char buffer[1073741824];

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        printf("Missing argument.\nUsage: ./run <filename>\nPress any key to continue. . . ");
        getch();
        return 0;
    }
    sprintf(buffer, "%s", argv[1]);
    clock_t t0 = clock();
    freopen("tmp.txt", "w", stdout);
    int exitcode = system(buffer);
    clock_t t1 = clock();
    printf("\nProcess terminated with return code %d after %f seconds.\n", exitcode, ((double) (t1 - t0) / CLOCKS_PER_SEC));
    printf("Press any key to continue. . . ");
    getch();
}
