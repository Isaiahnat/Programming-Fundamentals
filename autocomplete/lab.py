"""
6.1010 Spring '23 Lab 9: Autocomplete
"""

# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences
import test


class PrefixTree:
    def __init__(self):
        self.value = None
        self.children = {}

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the prefix tree,
        or reassign the associated value if it is already present.
        Raise a TypeError if the given key is not a string.
        """
        
        if not isinstance(key,str):
            raise TypeError
        
        if len(key)==1:
            if key in self.children and self.children[key] is not None:
                next_node = self.children[key]
            else:
                next_node = PrefixTree()
            next_node.set_val(value)
            self.children[key] = next_node

        elif key in self.children:
            next_node = self.children[key]
            if next_node is None:
                next_node = PrefixTree()
            next_node.set_val(value)
            self.children[key] = next_node

        else:
            if not self.children:
                next_node = PrefixTree()
                next_node.add_children(None,key[1])
                self.children[key[0]] = next_node
                next_node.__setitem__(key[1:],value)
        
            else:
    
                target = key[0]
                
                if target in self.children and self.children[target] is not None:
                    next_node = self.children[target]
                    children = next_node.get_children()
                    if key[1] not in children:
                        next_node.add_children(None,key[1])
                    next_node.__setitem__(key[1:],value)
                else:
                    next_node = PrefixTree()
                    next_node.add_children(None,key[1])
                    self.children[target] = next_node
                    next_node.__setitem__(key[1:],value)


    def get_children(self):
        """
        Returns the children dictionary
        """
        return self.children
    
    def add_children(self, child, string):
        """
        Adds a child node to a prefix tree instance
        """
        self.children[string] = child
    
    def set_val(self, val):
        """
        Sets the value of a prefix tree to the given val
        """
        self.value = val

    def get_val(self):
        """
        Return Value
        """
        return self.value
    
    def __getitem__(self, key):
        """
        Return the value for the specified prefix.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key,str):
            raise TypeError
        
        if len(key)==1 and key not in self.children:
            raise KeyError
        
        elif len(key)==1:
            next_node = self.children[key]
            val = next_node.get_val()
            if val is None:
                raise KeyError
            else:
                return val
            
        first = key[0]

        if first not in self.children:
            raise KeyError
        else:
            next_node = self.children[first]
            return next_node.__getitem__(key[1:])

        
    def find_node(self, key):
        """
        Returns node is node is found in prefix tree
        Returns None if not found
        """ 
        if not isinstance(key,str):
            raise TypeError
        

        if key =="":
            return self
        
        if len(key)==1 and key not in self.children:
            return None
        
        elif len(key)==1:
            return self.children[key]
        
        
        first = key[0]
        if first not in self.children:
            return None
        else:
            next_node = self.children[first]
            return next_node.find_node(key[1:])
        


    def __delitem__(self, key):
        """
        Delete the given key from the prefix tree if it exists.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        node = self.find_node(key)
        if node is None:
            raise KeyError
        if node.get_val() is None:
            raise KeyError
        node.set_val(None)

    def __contains__(self, key):
        """
        Is key a key in the prefix tree?  Return True or False.
        Raise a TypeError if the given key is not a string.
        """
        node = self.find_node(key)
        if node is None:
            return False
        val = node.get_val()
        if val is not None:
            return True
        else:
            return False

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this prefix tree
        and its children.  Must be a generator!
        """
        yield from self.recurse("")
        
    def recurse(self, string):
        """
        Helper recursive function for __iter__
        """
        if not self.children and self.value is not None:
            yield (string, self.value)
        
        else:

            if self.value is not None:
                yield (string, self.value)

            for key in self.children:
                newstr = string+key
                next_node = self.children[key]
                yield from next_node.recurse(newstr)
    

        



def word_frequencies(text):
    """
    Given a piece of text as a single string, create a prefix tree whose keys
    are the words in the text, and whose values are the number of times the
    associated word appears in the text.
    """
    tree = PrefixTree()
    sentences = tokenize_sentences(text)
    for sentence in sentences:
        words = sentence.split(" ")
        for word in words:
            try:
                value = tree[word]
                tree[word]+=1
            except:
                tree[word] = 1
    return tree
    



def autocomplete(tree, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is not a string.
    """
    if not isinstance(prefix,str):
        raise TypeError
    
    next_node = tree
    children = tree.get_children()
    for letter in prefix:
        if letter not in children:
            return []
        next_node = children[letter]
        children = next_node.get_children()
    to_check = list(next_node)
    to_check = sorted(to_check, key = lambda x: x[1])

    result = []

    if max_count is None:
        for tup in to_check:
            result.append(prefix+tup[0])
    else:
        length = len(to_check)
        if length>max_count:
            cut = len(to_check)-max_count
            to_check = to_check[cut:]
            for tup in to_check:
                result.append(prefix+tup[0])
        else:
            for tup in to_check:
                result.append(prefix+tup[0])
    return result



def autocorrect(tree, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    complete = autocomplete(tree,prefix,max_count)
    edits = set()
    edits = edits.union(insert_edits(tree,prefix))
    edits = edits.union(delete_edits(tree,prefix))
    edits = edits.union(replace_edits(tree,prefix))
    edits = edits.union(transpose_edits(tree,prefix))
    for i in complete:
        if i in edits:
            edits.remove(i)

    if max_count is None:
        return complete+list(edits)
    else:
        if len(complete)==max_count:
            return complete
        else:
            count = max_count-len(complete)
            edits = list(edits)
            edits.sort(key = lambda x: tree[x],reverse=True)
            return complete+edits[0:count]



def insert_edits(tree, prefix):
    """
    Given a PrefixTree object as well as a prefix, return all 
    valid insert edits
    """
    letters = "abcdefghijklmnopqrstuvwxyz"
    edits = set()
    for index in range(len(prefix)+1):
        for letter in letters:
            teststr = prefix[0:index]+letter+prefix[index:]
            if teststr in tree:
                edits.add(teststr)
    return edits


def delete_edits(tree, prefix):
    """
    Given a PrefixTree object as well as a prefix, return all 
    valid delete edits
    """
    edits = set()
    for index in range(len(prefix)):
        teststr = prefix[0:index]+prefix[index+1:]
        if teststr in tree:
            edits.add(teststr)
    return edits

def replace_edits(tree, prefix):
    """
    Given a PrefixTree object as well as a prefix, return all 
    valid replace edits
    """
    letters = "abcdefghijklmnopqrstuvwxyz"
    edits = set()
    for index in range(len(prefix)):
        for letter in letters:
            teststr = prefix[0:index]+letter+prefix[index+1:]
            if teststr != prefix and teststr in tree:
                edits.add(teststr)
    return edits

def transpose_edits(tree, prefix):
    """
    Given a PrefixTree object as a well as a prefix, return all
    valid transpose edits
    """
    edits = set()
    for index in range(len(prefix)-1):
        teststr = prefix[0:index]+prefix[index+1]+prefix[index]+prefix[index+2:]
        if teststr != prefix and teststr in tree:
            edits.add(teststr)
    return edits

def word_filter(tree, pattern):
    """
    Return list of (word, freq) for all words in the given prefix tree that
    match pattern.  pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    
    def filter_helper(tree,pattern):
        """
        helper function for wordfilter
        """
        result = set()
        children = tree.get_children()

        if len(pattern)==1:
            
            if pattern=="*":
                for key, val in tree:
                    result.add((key,val))

            elif pattern=="?":
                for key in children:
                    if children[key].get_val() is not None:
                        result.add((key,tree[key]))
            else:
                for key in children:
                    if children[key].get_val() is not None and key==pattern:
                        result.add((key,tree[key]))

        else:

            value = pattern[0]
            if value == "?":
                for key in children:
                    for tup in filter_helper(children[key],pattern[1:]):
                        result.add((key+tup[0],tup[1]))

            elif value == "*":
                # if tree==original:
                for tup in filter_helper(tree,pattern[1:]):
                    result.add(tup)
                        
                        
                
                for key in children:
                    for tup in filter_helper(children[key],pattern[1:]):
                        to_add = (key+tup[0],tup[1])
                        result.add(to_add)

                    for tup in filter_helper(children[key],pattern):
                        to_add = (key+tup[0],tup[1])
                        result.add(to_add)
                    
            else:
                if value in children:
                    next_node = children[value]
                    for tup in filter_helper(next_node,pattern[1:]):
                        result.add((value+tup[0],tup[1]))
        return result

    new_pattern = formula_formatter(pattern)
    result = filter_helper(tree,new_pattern)

    # if new_pattern[0]=="*":
    #     check = set()
    #     new = []
    #     for i in result:
    #         if i not in check:
    #             new.append(i)
    #             check.add(i)

    #     return new

    return list(result)



        

def formula_formatter(pattern):
    new_pattern = ""
    length = len(pattern)
    for index in range(length):
        if index == length-1:
            new_pattern+=pattern[index]
        elif pattern[index]=="*":
           if pattern[index+1]!="*":
               new_pattern+="*"
        else:
            new_pattern+=pattern[index]
    return new_pattern





# you can include test cases of your own in the block below.
if __name__ == "__main__":
    doctest.testmod()
    t = PrefixTree()
    # t["cat"] = "kitten"
    # t["car"] = "tricycle"
    # t["carpet"] = "rug"
    # t["barks"] = 8
    # print(t.get_children())
    # while t.get_children():
    #     children = t.get_children()
    #     print(children)
    #     keyss = children.keys()
    #     string = next(iter(keyss))
    #     # print(string)
    #     t = children[string]
    # t["barks"] = 8
    # t["hello"] = 3
    # print(t.get_children())
    # children = t.get_children()
    # keyss = children.keys()
    # string = next(iter(keyss))
    # child = children[string]
    # while child.get_children():
    #     children = child.get_children()
    #     print(children)
    #     keyss = children.keys()
    #     string = next(iter(keyss))
    #     # print(string)
    #     child = children[string]
    # t["hellos"] = 4
    # t["hre"] = 9
    # t["barkz"] = 2
    # print(t.get_children())
    # children = t.get_children()
    # keyss = children.keys()
    # string = next(iter(keyss))
    # child = children[string]
    # while child.get_children():
    #     children = child.get_children()
    #     print(children)
    #     keyss = children.keys()
    #     string = next(iter(keyss))
    #     # print(string)
    #     child = children[string]



    # t['man'] = ''
    # t['m'] = 1
    # t["ma"] = 2
    # t['mat'] = 3
    # print(list(t))
    
    # t['mattress'] = ()
    # t['map'] = 'pam'
    # t['me'] = 'you'
    # t['met'] = 'tem'
    # t['a'] = '?'
    # del t['me']
    # print(test.dictify(t))
    # print(t["me"])
    # print(list(t))
    # print(test.dictify(t))
    # test = word_frequencies("bat bat bark bar")
    # print(autocomplete(test,"ba",2))
    # t = word_frequencies("cats cattle hat car act at chat crate act car act")
    # print(insert_edits(t,'cat'))
    # result = autocorrect(t,'cat',4)

    # with open(test.os.path.join(test.TEST_DIRECTORY, 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
    #         text = f.read()
    # w = word_frequencies(text)
    # print(autocorrect(w,'mon'))
    # string = "abc"
    # print(string[-1])
    t = word_frequencies("man mat mattress map me met a man a a a map man met")
    result = word_filter(t, "*????")
    print(result)
    # print(result)
    # should be [("a", 4), ("man", 3), ("map", 2), ("mat", 1), ("mattress", 1), ("me", 1), ("met", 2)]

    # with open(test.os.path.join(test.TEST_DIRECTORY, 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
    #         text = f.read()
    # w = word_frequencies(text)
    # result = word_filter(w,"**ing**")
    # expected = test.read_expected('frank_filter_%s.pickle' % (3, ))
    # print(len(result))
    # print(len(expected))
    # # if ('ingolstadt', 16) in result:
    # #     print("yes")
    # # else:
    # #     print("no")
    # # thing = set(result)
    # # print(len(thing))
    # for i in expected:
    #     if i not in result:
    #         print(i)
    # # result.append(('ingolstadt', 16))
    # # result.append(('inglorious', 1))
    # # result.append(('ingenuity', 1))
    # # result.append(('ingratitude', 3))
    # print(len(result))
    # print(len(expected))
    


    # with open("Pride.txt", encoding="utf-8") as f:
    #     text = f.read()
    # words = word_frequencies(text)
    # # print(len(list(words)))
    # #count = 0
    # # for i in list(words):
    # #     count+=i[1]
    # # print(count)
    # print(autocorrect(words,"hear"))
    
    
