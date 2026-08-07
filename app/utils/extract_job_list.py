
file_path = "/home/ali/Desktop/job-application-tracker/app/utils/popular_jobs_list.txt"
def opener(file_path):
    with open(file=file_path, mode='r')\
            as file:
            popular_jobs = file.readlines()
            return popular_jobs
        
def store_in_list(file):
    li = list()
    for line in file:
        li.append(
            line.split('- ')[1].strip()
        )
    return li

def main():
    popular_jobs = opener(file_path)
    popular_job_list = store_in_list(popular_jobs)
    return popular_job_list

if __name__ == "__main__":
    print(main())