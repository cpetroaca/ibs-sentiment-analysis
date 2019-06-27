class Sentiment:
    def __init__(self, type):
        self._type = type
        self._count = 0
        self._posts_list = list()
    
    def inc(self):
        self._count += 1
    
    def add_post(self, post):
        self.inc()
        if len(self._posts_list) <= 10:
            self._posts_list.append(post)
            
            if len(self._posts_list) == 10:
                self._posts_list.sort(key=self.sortScore, reverse=True)
        
            return
        
        score = post['score']
        if abs(score) > abs(self._posts_list[9]['score']):
            self._posts_list[9] = post
    
    def sortScore(self, element):
        return element['score']