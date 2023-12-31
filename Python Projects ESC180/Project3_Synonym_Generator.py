import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''find keys in dictionary which are same for dot product, then find magnitude for all vectors in the denominator'''
    dot_prod = 0
    mag_vec1 = 0
    mag_vec2 = 0
    for k1, v1 in vec1.items():
        dot_prod += v1 * vec2.get(k1, 0.0)
        mag_vec1 += v1**2
    for k2, v2 in vec2.items():
        mag_vec2 += v2**2
    mag_tot = math.sqrt(mag_vec1 * mag_vec2)
    return dot_prod/mag_tot


def build_semantic_descriptors(sentences):
    '''This function takes in a list sentences which contains lists of strings (words) representing sentences, and returns a dictionary d such that for every word w that appears in at least one of the sentences, d[w] is itself a dictionary which represents the semantic descriptor of w'''
    # input is a list of lists of the words in each sentence
    d = {}
    for sentence in range(len(sentences)):
        for word in sentences[sentence]:
            if word not in d.keys():
                d[word] = {}
            for word2 in sentences[sentence]:
                if word == word2:
                    continue
                if word2 not in d[word].keys():
                    d[word][word2] = 1
                else:
                    d[word][word2] += 1
    return d


def similarity_fn(vec1, vec2):
    pass





def build_semantic_descriptors_from_files(filenames):
    total_list = []
    for file in range(len(filenames)):
        f = open(filenames[file], "r", encoding="latin1")
        text = f.read()
        text = text.lower()
        text = text.replace("!", ".")
        text = text.replace("?", ".")
        text = text.replace(";", " ")
        text = text.replace(",", " ")
        text = text.replace(":", " ")
        text = text.replace("-", " ")
        text = text.replace("--", " ")
        text = text.replace("/", " ")
        sentences = text.split(".")
        for i in range(len(sentences)):
            list = sentences[i].split()
            total_list.append(list)
    sem_desc = build_semantic_descriptors(total_list)
    return sem_desc



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    '''This function takes in a string word, a list of strings choices, and a dictionary semantic_descriptors
which is built according to the requirements for build_semantic_descriptors, and returns the element
of choices which has the largest semantic similarity to word, with the semantic similarity computed using
the data in semantic_descriptors and the similarity function similarity_fn. The similarity function is
a function which takes in two sparse vectors stored as dictionaries and returns a float. An example of such
a function is cosine_similarity. If the semantic similarity between two words cannot be computed, it is
considered to be âˆ’1. In case of a tie between several elements in choices, the one with the smallest index
in choices should be returned (e.g., if there is a tie between choices[5] and choices[7], choices[5] is
returned).'''
    best_choice = choices[0]
    cur_max = -1
    for i in range(len(choices)):
        try:
            cos_sim = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]])
        except:
            cos_sim = -1
        if cos_sim > cur_max:
            cur_max = cos_sim
            best_choice = choices[i]
    return best_choice


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    '''This function takes in a string filename which is the name of a file in the same format as test.txt, and
returns the percentage (i.e., float between 0.0 and 100.0) of questions on which most_similar_word()
guesses the answer correctly using the semantic descriptors stored in semantic_descriptors, using the
similarity function similariy_fn.'''
    f = open(filename, "r", encoding="latin1")
    text = f.read()
    text = text.split("\n")
    for i in range(len(text) - 1):
        text[i] = text[i].split()
    total = 0
    correct = 0
    ans = ""
    question = ""
    choices = []
    check = ""
    for i in range(len(text)- 1):
        question = text[i][0]
        ans = text[i][1]
        choices = [text[i][2], text[i][3]]
        check = most_similar_word(question, choices, semantic_descriptors, similarity_fn)
        if check == ans:
            correct += 1
        total += 1
    return ((correct/total)*100)




if __name__ == "__main__":
    # print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))
    # print(build_semantic_descriptors([["i", "am", "a", "sick", "man"], ["i", "am", "a", "spiteful", "man"], ["i", "am", "an", "unattractive", "man"],["i", "believe", "my", "liver", "is", "diseased"],["however", "i", "know", "nothing", "at", "all", "about", "my", "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]))
    # print(build_semantic_descriptors_from_files(["War and Peace.txt", "Swann's Way.txt"]))
    # print(build_semantic_descriptors_from_files(['tester.txt']))
    sem_descriptors = build_semantic_descriptors_from_files(["War and Peace.txt", "Swann's Way.txt"])
    res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")