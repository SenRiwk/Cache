#Riwk Sen

class Node:
    def __init__(self, content):
        self.value = content
        self.next = None

    def __str__(self):
        return ('CONTENT:{}\n'.format(self.value))

    __repr__=__str__


class ContentItem:
    '''
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content3 = ContentItem(1005, 18, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content4 = ContentItem(1005, 18, "another header", "111110")
        >>> hash(content1)
        0
        >>> hash(content2)
        1
        >>> hash(content3)
        2
        >>> hash(content4)
        1
    '''
    def __init__(self, cid, size, header, content):
        self.cid = cid
        self.size = size
        self.header = header
        self.content = content

    def __str__(self):
        return f'CONTENT ID: {self.cid} SIZE: {self.size} HEADER: {self.header} CONTENT: {self.content}'

    __repr__=__str__

    def __eq__(self, other):
        if isinstance(other, ContentItem):
            return self.cid == other.cid and self.size == other.size and self.header == other.header and self.content == other.content
        return False

    def __hash__(self):
        total = 0

        for letter in self.header:
            single_num = ord(letter)
            total += single_num
        return (total%3)

        



class CacheList:
    ''' 

        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content3 = ContentItem(1005, 180, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content4 = ContentItem(1006, 18, "another header", "111110")
        >>> content5 = ContentItem(1008, 2, "items", "11x1110")
        >>> lst=CacheList(200)
        >>> lst
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
        >>> lst.put(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> lst.put(content2, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> lst.put(content4, 'mru')
        'INSERTED: CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110'
        >>> lst.put(content5, 'mru')
        'INSERTED: CONTENT ID: 1008 SIZE: 2 HEADER: items CONTENT: 11x1110'
        >>> lst.put(content3, 'lru')
        "INSERTED: CONTENT ID: 1005 SIZE: 180 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> lst.put(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> 1006 in lst
        True
        >>> contentExtra = ContentItem(1034, 2, "items", "other content")
        >>> lst.update(1008, contentExtra)
        'UPDATED: CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content'
        >>> lst
        REMAINING SPACE:170
        ITEMS:3
        LIST:
        [CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content]
        [CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]


        # I GET A DIFFERENT ANSWER FOR THIS PART (THIS IS WHAT I GET)
        [CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        [CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110]


        <BLANKLINE>
        >>> lst.clear()
        'Cleared cache!'
        >>> lst
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
    '''
    def __init__(self, size):
        self.head = None
        self.maxSize = size
        self.remainingSpace = size
        self.numItems = 0

    def __str__(self):
        listString = ""
        current = self.head
        while current is not None:
            listString += "[" + str(current.value) + "]\n"
            current = current.next
        return 'REMAINING SPACE:{}\nITEMS:{}\nLIST:\n{}'.format(self.remainingSpace, self.numItems, listString)  

    __repr__=__str__

    def __len__(self):
        return self.numItems
    
    def put(self, content, evictionPolicy):
        #Is the size of the entry greater than the size of the Cache List?
        if int(content.size) > int(self.maxSize):
            return 'Insertion not allowed'

        #Is the size of the entry less than the remaining size?
        if int(content.size) < int(self.remainingSpace):
            new = Node(content)
            new.next = self.head
            self.head = new
            self.remainingSpace -= content.size
            self.numItems += 1
            return f'INSERTED: {content}'

        #Is the content already in the list?

            #Is the content already the head?
        if self.head.value.cid == content.cid:
            return f'Content {content.cid} already in cache, insertion not allowed'

            #Is the content anywhere else?
        prev = self.head
        current = self.head.next
        after = self.head.next.next
        while current != None:
            if current.value.cid == content.cid:
                prev.next = after
                current.next = self.head
                self.head = current
                return f'Content {content.cid} already in cache, insertion not allowed'
            else:
                if after == None:
                    break
                else:
                    prev = prev.next
                    current = current.next
                    after = after.next

        #Does the list need to be freed up for the content to be added?
        while self.remainingSpace < content.size:
            if evictionPolicy == 'mru':
                space_of_mru = self.head.value.size
                self.remainingSpace += space_of_mru
                self.numItems -= 1
                self.mruEvict()
            if evictionPolicy == 'lru':
                find_last = self.head
                while find_last.next != None:
                    find_last = find_last.next
                space_of_lru = find_last.value.size
                self.remainingSpace += space_of_lru
                self.numItems -= 1
                self.lruEvict()
        new_node = Node(content)
        new_node.next = self.head
        self.head = new_node
        self.remainingSpace -= content.size
        self.numItems += 1
        return f'INSERTED: {content}'
                
            
        
        

    

    def __contains__(self, cid):
        #Is the content already the head?
        if self.head.value.cid == cid:
            return True

            #Is the content anywhere else?
        prev = self.head
        current = self.head.next
        after = self.head.next.next
        while current != None:
            if current.value.cid == cid:
                prev.next = after
                current.next = self.head
                self.head = current
                return True
            else:
                if after == None:
                    return False
                else:
                    prev = prev.next
                    current = current.next
                    after = after.next


    def update(self, cid, content):
        #Is the cid not in the linked list?
        if self.__contains__(cid) == False:
            return 'Cache miss!'

        #Is the cid already the head?
        if self.head.value.cid == cid:
            pass

        #Then the cid must be someplace after the head; move it to the front
        else:
            prev = self.head
            present = self.head.next
            after = self.head.next.next
            while present != None:
                print(present.value.cid)
                if present.value.cid == cid:
                    prev.next = after
                    present.next = self.head
                    self.head = present
                    break
                else:
                    if after == None:
                        break
                    else:
                        prev = prev.next
                        present = present.next
                        after = after.next
        #Is the content addition exceeding the space
        if self.remainingSpace + self.head.value.size - content.size < 0:
            return 'Cache miss!'
        #Then the current content will be replaced with the new content
        self.remainingSpace = self.remainingSpace + self.head.value.size - content.size
        next_connect = self.head.next
        self.head = Node(content)
        self.head.next = next_connect
        return f'UPDATED: {content}'



    def mruEvict(self):
        #Is there no entries?
        if self.head == None:
            return
        #Is there only 1 entry?
        if self.head.next == None:
            self.head = None
            return
        self.head = self.head.next
        return

    
    def lruEvict(self):
        #Is there no entries?
        if self.head == None:
            return
        #Is there only 1 entry?
        if self.head.next == None:
            self.head = None
            return
        current = self.head
        while current.next.next != None:
            current = current.next
        current.next = None

    
    def clear(self):
        while self.head.next != None:
            self.remainingSpace += self.head.next.value.size
            self.numItems -= 1
            self.head.next = self.head.next.next
        self.remainingSpace += self.head.value.size
        self.numItems -= 1
        self.head = None
        
        return "Cleared Cache"


class Cache:
    """

        >>> cache = Cache()
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1003, 13, "Content-Type: 0", "0xD")
        >>> content3 = ContentItem(1008, 242, "Content-Type: 0", "0xF2")

        >>> content4 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content5 = ContentItem(1001, 51, "Content-Type: 1", "110011")
        >>> content6 = ContentItem(1007, 155, "Content-Type: 1", "10011011")

        >>> content7 = ContentItem(1005, 18, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content8 = ContentItem(1002, 14, "Content-Type: 2", "<html><h2>'PSU'</h2></html>")
        >>> content9 = ContentItem(1006, 170, "Content-Type: 2", "<html><button>'Click Me'</button></html>")

        >>> cache.insert(content1, 'lru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> cache.insert(content2, 'lru')
        'INSERTED: CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD'
        >>> cache.insert(content3, 'lru')
        'Insertion not allowed'

        >>> cache.insert(content4, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> cache.insert(content5, 'lru')
        'INSERTED: CONTENT ID: 1001 SIZE: 51 HEADER: Content-Type: 1 CONTENT: 110011'
        >>> cache.insert(content6, 'lru')
        'INSERTED: CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011'

        >>> cache.insert(content7, 'lru')
        "INSERTED: CONTENT ID: 1005 SIZE: 18 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> cache.insert(content8, 'lru')
        "INSERTED: CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>"
        >>> cache.insert(content9, 'lru')
        "INSERTED: CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>"
        >>> cache
        L1 CACHE:
        REMAINING SPACE:177
        ITEMS:2
        LIST:
        [CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:45
        ITEMS:1
        LIST:
        [CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011]
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:16
        ITEMS:2
        LIST:
        [CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>]
        [CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>]
        <BLANKLINE>
        <BLANKLINE>
    """

    def __init__(self):
        self.hierarchy = [CacheList(200), CacheList(200), CacheList(200)]
        self.size = 3
    
    def __str__(self):
        return ('L1 CACHE:\n{}\nL2 CACHE:\n{}\nL3 CACHE:\n{}\n'.format(self.hierarchy[0], self.hierarchy[1], self.hierarchy[2]))
    
    __repr__=__str__


    def clear(self):
        for item in self.hierarchy:
            item.clear()
        return 'Cache cleared!'

    
    def insert(self, content, evictionPolicy):
        hash_place = content.__hash__()
        return self.hierarchy[hash_place].put(content, evictionPolicy)


    def __getitem__(self, content):
        hash_place = content.__hash__()

        if self.hierarchy[hash_place].head == None:
            return 'Cache miss!'

        if self.hierarchy[hash_place].__contains__(content.cid) == False:
            return 'Cache miss!'
        else:
            return self.hierarchy[hash_place].head.value



    def updateContent(self, content):
        hash_place = content.__hash__()

        if self.hierarchy[hash_place].head == None:
            return 'Cache miss!'

        if self.hierarchy[hash_place].__contains__(content.cid) == False:
            return 'Cache miss!'
        else:
            return self.hierarchy[hash_place].update(content.cid, content)


   
