#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct term{
char term[200]; // assume terms are not longer than 200
double weight;
} term;

int compare_term_lex(const void *x_void, const void *y_void)
{
    return strcmp((*(term *)x_void).term,(*(term *)y_void).term);
}

void read_in_terms(term **terms, int *pnterms, char *filename)
{
    FILE *fp = fopen(filename,"r");
    char line[200];
    fgets(line, 200, fp);
    int nterms = atoi(line);
    *pnterms = nterms; // storing number of terms
    *terms = (term *)malloc(nterms * sizeof(term));
    //printf("%d", nterms);

    for(int i = 0; i < nterms; i++){
        fgets(line, 200, fp);
        char temp[200];
        int j = 0;
        while (line[j] < 47 || line[j] > 58){
            j++;
        }
        int k = 0;
        while(line[j] > 47  && line[j] < 58){
            temp[k] = line[j];
            k++;
            j++;
        }
        temp[k] = '\0';
        k = 0;
        j++;
        (*terms)[i].weight = atof(temp);
        while(line[j] != '\n' && line[j] != '\0'){
            (*terms)[i].term[k] = line[j];
            j++;
            k++;
        }
    }
    fclose(fp);
    qsort(*terms, nterms, sizeof(term), compare_term_lex);
}

int lowest_match(term *terms, int nterms, char *substr)
{
    int left_most = 0;
    int right_most = nterms;
    char temp[200];
    
    while(1 == 1){
        int mid = (left_most+right_most)/2;
        if((left_most+right_most)%2 == 1){
            mid++;
        }
        int i = 0;
        if(mid == right_most){
            return mid;
        }
        while(substr[i] != '\0'){
            temp[i] = terms[mid].term[i];
            i++;
        }
        temp[i] = '\0';
        if(strcmp(temp,substr) >= 0){
            right_most = mid;
        }
        else{
            left_most = mid;
        }       
    }
}

int highest_match(struct term *terms, int nterms, char *substr)
{
    int left_most = 0;
    int right_most = nterms;
    char temp[200];
    
    while(1 == 1){
        int mid = (left_most+right_most)/2;
        int i = 0;
        if(right_most - left_most == 0){
            return right_most;
        }
        if(right_most - left_most == 1){
            return left_most;
        }
        while(substr[i] != '\0'){
            temp[i] = terms[mid].term[i];
            i++;
        }
        temp[i] = '\0';
        if(strcmp(temp,substr) <= 0){
            left_most = mid;
        }
        else{
            right_most = mid;
        }       
    }
}

int compare_int(const void *x_void, const void *y_void)
{
    return (*(term *)y_void).weight - (*(term *)x_void).weight;
}

void autocomplete(term **answer, int *n_answer, term *terms, int nterms, char *substr)
{
    int left_ind = lowest_match(terms,nterms,substr);
    int right_ind = highest_match(terms,nterms,substr);
    *n_answer = right_ind - left_ind;
    *answer = (term *)malloc(sizeof(term)* (right_ind-left_ind));
    int j = 0;
    for(int i = left_ind; i < right_ind; i++){
        (*answer)[j].weight = (terms)[i].weight;
        strcpy((*answer)[j].term, (terms)[i].term);
        j++;
    }
    qsort(*answer, right_ind - left_ind, sizeof(term), compare_int);

}


/* int main()
{
    term *terms;
    int n_terms;
    read_in_terms(&terms,&n_terms,"cities.txt");
    for(int i = 0; i < n_terms; i++){
        printf("%f\n", terms[i].weight);  
        printf("%s\n", terms[i].term);
    }
    
    //printf("%d\n",lowest_match(terms, n_terms, "Was"));
   // printf("%d\n",highest_match(terms, n_terms, "Was"));
    //printf("%s\n", terms[88675].term);
    term *answer;
    int n_answer;
    autocomplete(&answer, &n_answer, terms, n_terms, "Pol");
    //printf("%f\n",answer[0].weight);
    //printf("%s\n", answer[i].term);
    for(int i = 0; i < n_answer; i++){
        printf("%f\n", answer[i].weight);  
        printf("%s\n", answer[i].term);
    }

    return 0;
}*/