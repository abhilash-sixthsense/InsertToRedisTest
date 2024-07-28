import redis
import random
import string
import time
from redis.exceptions import BusyLoadingError

# Connect to Redis
redis_host = 'redis'
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

MAX_USERS = 1800000
RETRY_INTERVAL = 5  # Seconds between retries

def generate_file_paths(user_id, num_files=26):
    return [f"/user/data/path/to/file_{user_id}_number_{i}.txt" for i in range(1, num_files + 1)]

def get_existing_user_count():
    try:
        return len(redis_client.keys('*'))
    except BusyLoadingError:
        raise

def insert_remaining_users(num_users=1800000):
    start_time = time.time()
    
    # Retry until Redis is ready
    while True:
        try:
            existing_count = get_existing_user_count()
            break
        except BusyLoadingError:
            print("Redis is still loading the dataset. Waiting...")
            time.sleep(RETRY_INTERVAL)
    
    print(f"Existing user count: {existing_count}")
    
    # Calculate how many new users can be inserted
    users_to_insert = MAX_USERS - existing_count
    
    if users_to_insert <= 0:
        print("Redis already has the maximum number of users. No new users will be inserted.")
        return
    
    new_entries = 0
    
    for idx in range(1, num_users + 1):
        if new_entries >= users_to_insert:
            break
        
        user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
        # Attempt to set the user ID if it does not already exist
        try:
            result = redis_client.setnx(user_id, ','.join(generate_file_paths(user_id)))
            if result:
                new_entries += 1
        except BusyLoadingError:
            print("Redis is still loading the dataset. Waiting...")
            time.sleep(RETRY_INTERVAL)
            continue
        
        if idx % 10000 == 0 or idx == num_users:
            elapsed_time = time.time() - start_time
            print(f"Processed {idx}/{num_users} users. New entries inserted: {new_entries}. Elapsed time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    insert_remaining_users()
    print("Data insertion completed.")
