from pathlib import Path

file_path = Path(__file__).parent / "popular_status_list.txt"

def opener(file_path):
    with open(file=file_path, mode='r')\
            as file:
            popular_status = file.readlines()
            return popular_status
        
def store_in_list(file):
    li = list()
    for line in file:
        li.append(
            line.split('- ')[1].strip()
        )
    return li

def main():
    popular_status = opener(file_path)
    popular_status_list = store_in_list(popular_status)
    return popular_status_list

if __name__ == "__main__":
    print(main())