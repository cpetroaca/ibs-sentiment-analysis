class SentimentResult:
    def __init__(self):
        self._count = 0
        self._posts_list = list()
    
    def inc(self):
        self._count += 1
    
    def add_post(self, post):
        self.inc()
        self._posts_list.append(post)
    
    def trim_list(self):
        self._posts_list.sort(key=self.sortScore, reverse=True)
        list_len = len(self._posts_list)
        delete_posts_cnt = list_len - 10
        self._posts_list = self._posts_list[:list_len - delete_posts_cnt]
        
    def sortScore(self, element):
        return abs(element['score'])