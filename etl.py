import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import datetime


def process_song_file(cur, filepath):
    
    """
    This Function is created for ingesting songs folder data
    
    -> With this function the insertion in the song table is done
    
    -> Insertion in artist table is also performed by this function
    
    """
    # open song file
    print(filepath)
    df = pd.read_json(filepath,typ='Series')
    #df.show()

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This Function is created for ingesting logs folder data
    
    -> With this function the insertion in the songplays,time and users table is done.
     
     -> Every file is read one by one and suitable records for table
     are inserted
    
    """
    # open log file
    df = pd.read_json(filepath,lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'],unit='ms')
    # insert time data records
    time_data =[t,t.dt.hour,t.dt.day,t.dt.week,t.dt.month,t.dt.year,t.dt.weekday]
    #column names for dataframe
    column_labels = ['start_time','hour','day','week','month','year','weekday']
    emdi={}
    for i in range(len(column_labels)):
        emdi[column_labels[i]]=time_data[i]
    time_df = pd.DataFrame(data=emdi)

    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except:
            print("Errored DATA: ",row)
            
        

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
            
        #fetches the result from cursor
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
        
        #print(songid," ",artistid)
        # insert songplay record
        k=pd.to_datetime(row.ts ,unit='ms')
        #print("I am K : ",k," ",songid," ",artistid)
        songplay_data = (k,row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        try:
            cur.execute(songplay_table_insert, songplay_data)
        except:
            print("Errored DATA: ",songplay_data)
            
#below command is for testing
#         if songid is not None: 
#             print(songplay_data)
            
        
#         cur.execute("""SELECT DISTINCT song_id,artist_id from songplays """)
#         res=cur.fetchall()
#         #print(songid," ",artistid)
#         for i in res:
#             print(i)
            
        


def process_data(cur, conn, filepath, func):
    """
    This function gets all the files present in a path.
    and call the function which is required.
    for further loading of data into the tables
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()