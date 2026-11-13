# youtube-dlp-transcript-python-script-to-combine-text-
Combine 10 lines of text into paragraphs and merge the time stamps for better readability, like how notegpt does

yt-dlp --skip-download --write-sub --write-auto-sub --sub-format srt www.youryoutubeurl
I used this command to download a playlist of transcripts in srt format

heres a python script to do postprocessing, processing srt format by combining time stamps 5 into 1 for better readability. download python, create a text file called transcript_combine.py inside a directory of your srt files and paste the code, then run the script by double clicking
