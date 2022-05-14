#include "dick_search.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int count_char(char text[], char c)
{
    int length, count = 0;
    length = strlen(text);
    for (size_t i = 0; i < length; i++)
    {
        if (text[i] == c)
        {
            count += 1;
        }
    }
    return count;
}
char **lines_from_file(char path[], int *size)
{
    long numbytes;
    FILE *f;
    char *buffer;
    f = fopen(path, "r");

    /* quit if the file does not exist */
    // if(f == NULL)
    //     return -1;

    /* Get the number of bytes */
    fseek(f, 0L, SEEK_END);
    numbytes = ftell(f);

    // printf("Bytes: %ld\n", numbytes);
    fseek(f, 0L, SEEK_SET);

    buffer = (char *)calloc(numbytes, sizeof(char));
    // if(buffer == NULL)
    //     return -1;

    fread(buffer, sizeof(char), numbytes, f);
    fclose(f);
    int nol = count_char(buffer, '\n') + 1; // number of linebreaks plus one for last line
    // printf("nol: %d\n", nol);
    *size = nol;
    char **line_points = (char **)calloc(nol, sizeof(char *));
    char *tmp = strtok(buffer, "\n");
    int j = 0;
    while (tmp != NULL)
    {
        line_points[j++] = tmp;
        tmp = strtok(NULL, "\n");
    }
    // free(mem_point);

    return line_points;
}

int word_in_dictionary_file(char word[], char path[])
{
    char **line_points = (char **)calloc(1, sizeof(char *));
    int x = 700;
    int *length = &x; // secure memory address with the x
    int found = 0;

    line_points = lines_from_file(path, length);

    for (size_t i = 0; i < *length; i++)
    {
        if (!strcmp(word, line_points[i])) //0 means its the same
        {
            found = 1;
        }
    }
    free(line_points[0]); // free the buffer memory
    free(line_points);        // free the pointers memory
    return found;
}

// int main(int argc, char const *argv[])
// {
//     printf("result: %d\n",word_in_dictionary_file("oder nicht","./fat_test.txt"));
//     return 0;
// }
