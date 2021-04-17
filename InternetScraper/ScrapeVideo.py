from bs4 import BeautifulSoup
from urllib.request import urlopen
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import TranscriptsDisabled#, NoTranscriptFound, NoTranscriptAvailable
from youtube_transcript_api._errors import NoTranscriptFound, NoTranscriptAvailable


class ScrapeVideos:
    def __init__(self):
        pass

    def getTranscipts(self, lsIDs):
        results={}
        for id in lsIDs:
            try:

                r = ScrapeVideo().getTranscriptByLink(id)
                if r == None : continue
                else: results[r[0]] = r[1]
                #TODO THE BELOW except statement does not seem to catch
            except TranscriptsDisabled  or NoTranscriptFound or NoTranscriptAvailable:
                print("skipping id", id)


        return results




class ScrapeVideo:

    def __init__(self):
        pass


    def getTranscriptByLink(self, video_id):
        # html = urlopen(link) #"https://www.youtube.com/watch?v=5_zrHZdhaBU"
        # soup = BeautifulSoup(html, 'html.parser')
        # nameList = soup.findAll("div", {"id": "cp-2"})
        # for name in nameList:
        #     print(name.get_text())

        vectorOfWords=""
        #print(type(transcript_list))

        try:

            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            #transcript_list_Raw = transcript_list.find_transcript(['en'])
            #print(transcript_list.find_transcript([]))
            transcript_list_Raw = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

            for transcript in transcript_list_Raw:
                # the Transcript object provides metadata properties
                #print(transcript)
                vectorOfWords=vectorOfWords+" "+transcript['text']

            print("Am I next getting here?")
            return [video_id, vectorOfWords]
        except Exception:
            print("No English Transcript. For future use add British English")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print(ScrapeVideo().getTranscriptByLink('HY4Sx96UEpM'))
