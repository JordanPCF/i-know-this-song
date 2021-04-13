from spotify import get_user_playlists
from genius import get_songs_from_lyrics
from data_collector import get_song_set
from playlist import Playlist
import json
import re
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    
    connection_id = event["requestContext"].get("connectionId")
    body = event["body"]
    body = json.loads(body) # if body is not None else '{"Error": "Need to set this default value"}')
    domain = event.get('requestContext', {}).get('domainName')
    stage = event.get('requestContext', {}).get('stage')
    apig_management_client = boto3.client(
                'apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')
                
    status_code = 200
    
    if body['requestType'] == 'playlists':
        playlists = get_user_playlists()
        message = f"{playlists}".encode('utf-8')
        logger.info(f"playlist message: {message}")
        
        try: 
            send_response = apig_management_client.post_to_connection(Data=message, ConnectionId=connection_id)
            logger.info(f"Posted message to connection {connection_id}, got response {send_response}")
        except ClientError:
            logger.exception(f"Couldn't post to connection {connection_id}")
            status_code = 450
        except apig_management_client.exceptions.GoneException:
            logger.info(f"Connection {connection_id} is gone, removing.")
            status_code = 460
            
    elif body['requestType'] == 'lyrics':
        # TODO: abstract this code out elsewhere, clean it up
        # currently solving for ONE playlist given, as a string (PLAYLIST_NAME: ID)
        playlists_ = re.findall(r'(.+):\ (\w+)', body['playlists'])
        logger.info(f"playlists_ = {playlists_}")
        playlist = Playlist(playlists_[0][0], playlists_[0][1])
        set_of_songs = get_song_set([playlist])
        
        message = ""
        genius_songs = get_songs_from_lyrics(body['lyrics'])
        for song in genius_songs:
            if song in set_of_songs:
                message = f"Found match! {song}".encode('utf-8')
                
        if message == "":
            message = "No matches found".encode('utf-8')
        logger.info(f"lyric match message: {message}")
        
        try: 
            send_response = apig_management_client.post_to_connection(Data=message, ConnectionId=connection_id)
            logger.info(f"Posted message to connection {connection_id}, got response {send_response}")
        except ClientError:
            logger.exception(f"Couldn't post to connection {connection_id}")
            status_code = 450
        except apig_management_client.exceptions.GoneException:
            logger.info(f"Connection {connection_id} is gone, removing.")
            status_code = 460
    
    return status_code
