import requests
import configparser

'''
config = configparser.ConfigParser()
config.read('tokens.ini')

def search_apple_music(artist, track):
  """
  Searches for a track by artist on Apple Music and returns the URL.

  Args:
      artist (str): Name of the artist.
      track (str): Name of the track.

  Returns:
      str: URL of the track on Apple Music or None if not found.
  """
  # Replace with your VALID Apple Music developer token (no spaces around it)
  token = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNzE4MDUyMDUxLCJleHAiOjE3MjUzMDk2NTEsInJvb3RfaHR0cHNfb3JpZ2luIjpbImFwcGxlLmNvbSJdfQ.nC_CMYwimOXXzbgMjaiqTSRM9pw_8eXp1byKSIw9ZbC62OqSc-6PaZrdBtWhzcMx7SNQuhq98x_-JhAwzd3h2Q"

  url = "https://api.music.apple.com/v1/catalog/us/search"
  headers = {"Authorization": f"Bearer {token.strip()}", 'Content-Type': 'application/json'}
  params = {"term": f"{artist} {track}", "types": ["songs"]}

  response = requests.get(url, headers=headers, params=params)

  if response.status_code == 200:
    data = response.json()
    if data["results"]["songs"]["data"]:
      # Get the first result (assuming it's the relevant track)
      track_data = data["results"]["songs"]["data"][0]
      return track_data["url"]
  else:
    print(f"Error searching Apple Music: {response.status_code}")
    return None

# Example usage (replace with your VALID token)
track_url = search_apple_music("The Beatles", "Let It Be")
if track_url:
  print(f"Track URL: {track_url}")
else:
  print("Track not found on Apple Music")
'''

'''
import requests

def search_apple_music(artist, track):
  """
  Searches for an artist's track on Apple Music (using iTunes Search API)

  Args:
      artist (str): Name of the artist
      track (str): Name of the track

  Returns:
      str: URL of the track on Apple Music or None if not found
  """
  url = f"https://itunes.apple.com/search?term={artist}+{track}&entity=album"
  response = requests.get(url)
  
  if response.status_code == 200:
    data = response.json()
    results = data.get("results", [])
    # Check if any results found
    if results:
      # Assuming the first result is the desired track
      return results[0]["collectionViewUrl"]
  
  return None

print(search_apple_music('kanye+west','ye'))'''