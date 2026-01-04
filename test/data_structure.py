import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from data_structure import LinkedList

def test():
    ll = LinkedList()
    ll.add_link("https://example.com/job1")
    ll.add_link("https://example.com/job2")
    print("Links after adding:")
    print(ll.get_links())
    
    print("Removing job1...")
    print(ll.remove_link("https://example.com/job1"))
    print("Links after removing job1:")
    print(ll.get_links())
    
    ll.clear_links()
    print("Links after clearing:")
    print(ll.get_links())




if __name__ == "__main__":
    test()
