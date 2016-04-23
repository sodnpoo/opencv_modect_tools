#youtube upload wrapper
import threading
from youtube_upload import main
import os

def youtube_upload(video_path, title, playlist=None, privacy='private', delete=False, client_secrets=''):
    print (video_path, title, playlist, privacy, delete)
    class Options(object):
        pass

    options = Options()
    options.client_secrets = client_secrets
    options.credentials_file = ''
    options.auth_browser = ''
    options.title = title
    options.privacy = privacy
    options.description = None
    options.publish_at = None
    options.tags = None
    options.title_template = "{title} [{n}/{total}]"
    options.category = None
    options.location = None
    options.default_language = None
    options.default_audio_language = None
    options.recording_date = None

    youtube = main.get_youtube_handler(options)

    video_id = main.upload_youtube_video(youtube, options, video_path, 1, 0)

    print video_id

    if playlist is not None:
        main.playlists.add_video_to_playlist(youtube, video_id, title=playlist, privacy=privacy)

    if delete is True:
        os.remove(video_path)

    return video_id

def bg_youtube_upload(video_path, title, playlist=None, privacy='private', delete=False):
    a = (video_path, title, playlist, privacy, delete)
    t = threading.Thread(target=youtube_upload, args = a)
    t.start()
