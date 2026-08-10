from pathlib import Path

file_path = Path(__file__).parent / "popular_position_list.txt"

def opener(file_path):
    with open(file=file_path, mode='r')\
            as file:
            populer_position = file.readlines()
            return populer_position
        
def store_in_list(file):
    li = list()
    for line in file:
        li.append(
            line.split('- ')[1].strip()
        )
    return li

def main():
    populer_position = opener(file_path)
    populer_position_list = store_in_list(populer_position)
    return populer_position_list

if __name__ == "__main__":
    print(main())