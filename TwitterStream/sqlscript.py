import MySQLdb

def main():
    sql = []
    sql.append("""CREATE TABLE IF NOT EXISTS users(user_id BIGINT(20) UNSIGNED, 
            created_at DATETIME, 
            PRIMARY KEY(user_id))ENGINE = InnoDB;
          """)
    sql.append("""CREATE TABLE IF NOT EXISTS user_info(user_id BIGINT(20) UNSIGNED,
            screen_name VARCHAR(25),
            name VARCHAR(100),
            followers int(10) unsigned,
            friends int(10) unsigned,
            description VARCHAR(250),
            image_url VARCHAR(100),
            last_update DATETIME,
            location VARCHAR(100),
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            PRIMARY KEY(user_id, screen_name, name, followers,                       
            description, image_url, location, friends))ENGINE = InnoDB;""")  
    
    sql.append("""CREATE TABLE IF NOT EXISTS tweets(tweet_id BIGINT(20) UNSIGNED PRIMARY KEY,
            tweet_text VARCHAR(1000),
            created_at DATETIME,
            geo_lat DECIMAL(10,5),
            geo_long DECIMAL(10,5),
            user_id BIGINT(10) UNSIGNED,
            tweet_url VARCHAR(250),
            retweet_count int(10),
            original_tweet_id BIGINT(20),
            FOREIGN KEY(user_id) REFERENCES users(user_id))ENGINE = InnoDB;""")
    
    sql.append("""CREATE TABLE IF NOT EXISTS tweet_hashtags(tweet_id BIGINT(20) UNSIGNED PRIMARY KEY,
            tag VARCHAR(500),
            created_at DATETIME,
            user_id BIGINT(20),
            FOREIGN KEY(tweet_id) REFERENCES tweets(tweet_id))ENGINE = InnoDB;""")
            
    sql.append("""CREATE TABLE IF NOT EXISTS tweet_mentions(tweet_id BIGINT(20) UNSIGNED PRIMARY KEY,
            source_user_id BIGINT(20),
            target_user_id BIGINT(20),
            FOREIGN KEY(tweet_id) REFERENCES tweets(tweet_id))ENGINE = InnoDB;""")


    sql.append("""CREATE TABLE IF NOT EXISTS tweet_links(tweet_id BIGINT(20) UNSIGNED PRIMARY KEY,
            user_id BIGINT(20),
            longURL  VARCHAR(1000),
            shortURL VARCHAR(500),
            created_at DATETIME,
            FOREIGN KEY(tweet_id) REFERENCES tweets(tweet_id))ENGINE = InnoDB;""")

    sql.append("""CREATE TABLE IF NOT EXISTS tweet_json_cache(tweet_id BIGINT(20) UNSIGNED PRIMARY KEY, 
            json_raw TEXT, 
            FOREIGN KEY(tweet_id) REFERENCES tweets(tweet_id))ENGINE = InnoDB;""")
            
    sql.append("""CREATE TABLE IF NOT EXISTS user_list(user_id  BIGINT(20) UNSIGNED, list_name VARCHAR(200),
            list_owner VARCHAR(25), PRIMARY KEY(user_id, list_name))ENGINE = InnoDB;""")
  
            
    db_con = MySQLdb.Connect('localhost', 'root', 'password1234', 'tweets')
    cursor = db_con.cursor()
    for command in sql:
        cursor.execute(command)
    print 'Done'
    
if __name__=="__main__":
    main()