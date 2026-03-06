TASK1_TARGET_LIST = "task1/target_list.txt"
TASK1_CRAWLED = "task1/crawled"
TASK1_INDEX = "task1/index.txt"


class FilesFacade:
    def get_links(self, filename: str = TASK1_TARGET_LIST) -> list[str]:
        """Load links from file"""
        with open(filename) as f:
            links = [line for line in f]
        return links
        
    # def get_crawled(self):
        
    
    # def get_index(self):
        
        
