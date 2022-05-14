#include <stdio.h>
#include <string.h>
#include <sys/time.h>
#include <math.h>
#include <windows.h>
#include "dick_search.h"

#define max_arr_length 200

void *char_to_pool_index(char[], int[]);
void print_num_arr(int[], int);
int check_arrays(int[], int[], int);
void prep_guess(int[], int);
double get_elapsed_time(struct timeval, struct timeval);
int guess_small_abc(char[], int);
void estimate_small_abc(int);
int guess_small_word(char[]);
void clear();

void clear()
{
#if defined(__linux__) || defined(__unix__) || defined(__APPLE__)
    system("clear");
#endif

#if defined(_WIN32) || defined(_WIN64)
    system("cls");
#endif
}

void *char_to_pool_index(char the_string[], int *point)
{

    for (size_t i = 0; i < strlen(the_string); i++)
    {
        // printf("iteration %d: ", i);
        point[i] = the_string[i] - 97;
        // printf("%d\n", point[i]);
    }
    return point;
}
void print_num_arr(int *new_array, int length)
{
    for (size_t i = 0; i < length; i++)
    {
        printf("%d ", new_array[i]);
    }
    printf("\n");
}

int check_arrays(int one[], int two[], int size)
{
    for (size_t i = 0; i < size; i++)
    {
        if (one[i] != two[i])
        {
            return 0;
        }
    }
    return 1;
}

void prep_guess(int one[], int length)
{
    for (size_t i = 0; i < length; i++)
    {
        one[i] = -1;
    }
}

double get_elapsed_time(struct timeval x1, struct timeval x2)
{
    double x1_us, x2_us, diff;

    x1_us = (double)x1.tv_sec * 1000000 + (double)x1.tv_usec;
    x2_us = (double)x2.tv_sec * 1000000 + (double)x2.tv_usec;

    diff = (double)x2_us - (double)x1_us;
    return diff / 1000000;
}

void estimate_small_abc(int length)
{
    struct timeval start_t, end_t;
    double secs;
    gettimeofday(&start_t, NULL);
    char test_word[] = "mmmmmm"; // 6 characters in middle of abc
    guess_small_abc(test_word, 0);
    gettimeofday(&end_t, NULL);
    secs = get_elapsed_time(start_t, end_t);
    secs = secs / pow(26, 6); // seconds per character
    secs = secs * pow(26, length);
    printf("ETA: %lf seconds\n", secs);
}
// estimate: 0=> no estimation
// pool ranges from 97 to 122 for a-z
int guess_small_abc(char passw[], int estimate)
{
    if (estimate)
    {
        printf("-> Brute Force\n");
        estimate_small_abc(strlen(passw));
    }
    int passw_index[strlen(passw)];
    int cur_index[max_arr_length];
    int max_value = 25;
    int cur_length = 1;
    int i = 0;
    int length = sizeof(passw_index) / sizeof(*passw_index);

    prep_guess(cur_index, max_arr_length);

    char_to_pool_index(passw, passw_index);

    while (!check_arrays(cur_index, passw_index, length))
    {
        cur_index[0] += 1;
        if (cur_index[0] > max_value)
        {
            i = 0;
            while (cur_index[i] > max_value)
            {
                if (cur_index[i + 1] == -1)
                {
                    cur_length += 1;
                    cur_index[i + 1] == 0;
                }
                cur_index[i + 1] += 1; // overflow to bigger digit
                cur_index[i] = 0;      // reset on lower digit
                i += 1;
            }
        }
    }
    return 0;
}

int guess_small_words(char passw[])
{
    FILE *f;
    char path[] = "./fat_words.txt";
    char word[max_arr_length];
    f = fopen(path, "r");
    printf("-> Dictionary ");
    if (f == NULL)
    {
        printf("{NO DICTIONARY FOUND}\n");
        guess_small_abc(passw, 1);
        return 0;
    }
    fclose(f);
    if (!word_in_dictionary_file(passw, path))
    {
        printf(" {NOT FOUND}\n");
        guess_small_abc(passw, 1);
        return 0;
    }

    printf("\nThe word is %s\n", passw);
    fclose(f);
}
int main(int argc, char const *argv[])
{
    struct timeval start_time, end_time;
    clear();
    printf("Please put in your password!\n");
    char passw[max_arr_length];
    scanf("%s", &passw);
    printf("guessing %s\n", passw);
    gettimeofday(&start_time, NULL);
    guess_small_words(passw); // start with dictionary search => {not found} => start with brute force
    gettimeofday(&end_time, NULL);
    printf("finished guessing in %lf seconds\n", get_elapsed_time(start_time, end_time));
    return 0;
}