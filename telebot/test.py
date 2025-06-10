#python test.py

def shortest_word_function(words):
    shortest_word = words[0] 
    shortest_length = len(shortest_word) 
    for word in words: 
        if shortest_length > len(word): 
            shortest_length = len(word) 
            shortest_word = word 
    return shortest_word 
    
s = input();
lst = s.split()
print(shortest_word_function(lst));
