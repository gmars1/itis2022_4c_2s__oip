TASK1_TARGET_LIST = "task1/target_list.txt"
TASK1_CRAWLED = "task1/crawled"
TASK1_INDEX = "task1/index.txt"

TASK2_TOKENS = "task2/tokens.txt"
TASK2_LEMMAS = "task2/lemmas.txt"

TASK2_TOKENS_FOLDER = "task2/tokens/"
TASK2_LEMMAS_FOLDER = "task2/lemmas/"


class FilesFacade:
    def get_links(self, filename: str = TASK1_TARGET_LIST) -> list[str]:
        """Load links from file"""
        with open(filename) as f:
            links = [line for line in f]
        return links
        
    # def get_crawled(self):
        
    
    # def get_index(self):
        
        
