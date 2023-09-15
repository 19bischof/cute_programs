# https://www.youtube.com/watch?v=c33AZBnRHks original video
# so idea is find 5 words that have each 5 letters and all letters are unique for a total of 25 letters
import time
start_t  = time.perf_counter()
bucket = 0
def convert_word_to_binary(word):
    buck = 0
    key_map =  {
  'a': 1,
  'b': 2,
  'c': 3,
  'd': 4,
  'e': 5,
  'f': 6,
  'g': 7,
  'h': 8,
  'i': 9,
  'j': 10,
  'k': 11,
  'l': 12,
  'm': 13,
  'n': 14,
  'o': 15,
  'p': 16,
  'q': 17,
  'r': 18,
  's': 19,
  't': 20,
  'u': 21,
  'v': 22,
  'w': 23,
  'x': 24,
  'y': 25,
  'z': 26
    }
    for letter in word.lower():
        x = 1 << key_map[letter]
        if x & buck:
            return None
        buck |= x
    return buck

words = {}

count = 0
with open('words.txt','r') as f:
    for word in f:
        word = word[:-1]
        if len(word) != 5:
            continue
        binary = convert_word_to_binary(word)
        if binary is None:
            continue
        words[binary] = word
        
valid_caches = {} # key = word

def build_valid_matches_for_binary(match_binary):
    # print('build valid for: ', words[match_binary])
    valid = set()
    for binary in words:
        if match_binary & binary == 0:
            valid.add(binary)
            
    valid_caches[match_binary] = valid

x_t = time.perf_counter()
for binary in words:
    build_valid_matches_for_binary(binary)
print(f'time to build cache: {(time.perf_counter() - x_t) * 1000:.2f} ms.')


removed_binaries = set()
all_binaries = set(words.copy().keys())
 
print('number of entries in words dict:', len(words))
def rec(in_use_binaries):
    if len(in_use_binaries) == 5:
        print('Found:',*in_use_binaries)
        found_words = list(map(lambda x: words[x], in_use_binaries))
        print('Or:', *found_words)
        return found_words
    
    if in_use_binaries:
        choices = valid_caches[in_use_binaries[0]].copy()
        for used_binary in in_use_binaries[1:]:
            choices &= valid_caches[used_binary]
    else:
        choices = all_binaries.copy()
        
    for binary in choices:
        if binary in removed_binaries:
            continue
        ret = rec(in_use_binaries + [binary])
        if ret:
            return ret
        
        if len(in_use_binaries) == 0:
            print('removed', words[binary])
            removed_binaries.add(binary)
            
result = rec([])
if not result:
    print('no result :*(') 
print(f'time taken: {(time.perf_counter() - start_t) * 1000:.2f} ms.')
exit()
    
            
