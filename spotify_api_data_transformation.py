import json
import boto3
from io import StringIO
import pandas as pd


def album(data):
    album_list = []
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_url = row['track']['album']['external_urls']['spotify']
        album_elements = {'album_id':album_id, 'album_name':album_name, 'album_release_date':album_release_date, 'album_total_tracks':album_total_tracks,'album_url':album_url}
        
        album_list.append(album_elements)
        
    return album_list
    
def artist(data):
    artist_list =[]
    for row in data['items']:
            for key, value in row.items():
                if key == "track":
                    for artist in value['artists']:
                        artist_elements = {'artist_id':artist['id'], 'artist_name':artist['name'], 'artist_url':artist['href']}
                        
                        artist_list.append(artist_elements)
                        
    return artist_list
    
def track(data):
    track_list =[]
    for row in data['items']:
        track_id = row['track']['id']
        track_name = row['track']['name']
        track_duration = row['track']['duration_ms']
        track_url = row['track']['external_urls']['spotify']
        track_popularity = row['track']['popularity']
        album_id = row['track']['album']['id']
        artist_id = row['track']['album']['artists'][0]['id']
        
        track_element = {'track_id':track_id, 'track_name':track_name, 'track_duration':track_duration, 'track_url':track_url, 'track_popularity':track_popularity, ' album_id': album_id, 'artist_id':artist_id} 
    
        track_list.append(track_element)
        
    return track_list
    
    
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    Bucket = "spotifyetl-de-project"
    Key = "raw_data/to_process"
    
    data = []
    spotify_keys = []
    
    for file in s3.list_objects(Bucket=Bucket, Prefix=Key)['Contents']:
        file_key = file['Key']
        if file_key.split('.')[-1] == "json":
            response = s3.get_object(Bucket=Bucket, Key=file_key)
            content = response['Body']
            jsonObject = json.loads(content.read())
            data.append(jsonObject)
            spotify_keys.append(file_key)
            
    for data in data:
            album_list = album(data)
            artist_list = artist(data)
            track_list = track(data)
            
            album_df = pd.DataFrame.from_dict(album_list)
            artist_df = pd.DataFrame.from_dict(artist_list)
            track_df = pd.DataFrame.from_dict(track_list)
            
            album_df = album_df.drop_duplicates(subset=['album_id'])
            artist_df = artist_df.drop_duplicates(subset=['artist_id'])
            track_df = track_df.drop_duplicates(subset=['track_id'])
            
            album_df['album_release_date'] = pd.to_datetime(album_df['album_release_date'], errors='coerce')
            
            track_key = "transformed_data/track_data/track_transformed" + ".csv"
            track_buffer=StringIO()
            track_df.to_csv(track_buffer, index=False)
            track_content = track_buffer.getvalue()
            s3.put_object(Bucket=Bucket, Key=track_key, Body=track_content)
            
            album_key = "transformed_data/album_data/album_transformed" + ".csv"
            album_buffer=StringIO()
            album_df.to_csv(album_buffer, index=False)
            album_content = album_buffer.getvalue()
            s3.put_object(Bucket=Bucket, Key=album_key, Body=album_content)
            
            artist_key = "transformed_data/artist_data/artist_transformed" + ".csv"
            artist_buffer=StringIO()
            artist_df.to_csv(artist_buffer, index=False)
            artist_content = artist_buffer.getvalue()
            s3.put_object(Bucket=Bucket, Key=artist_key, Body=artist_content)
            
    s3_resource = boto3.resource('s3')
    for key in spotify_keys:
        copy_source = {
                'Bucket':Bucket,
                'Key': key
        }
        s3_resource.meta.client.copy(copy_source, Bucket, 'raw_data/processed/' + key.split("/")[-1])
        s3_resource.Object(Bucket, key).delete()
            
            
            
   
