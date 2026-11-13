import sys
import re
from pathlib import Path

# Returns a Path object of the script's directory
script_dir = Path(__file__).resolve().parent
print("Script dir", script_dir)

#Check if arguments were passed (excluding the script name itself)
if len(sys.argv) > 1:
    how_many_lines_to_combine = sys.argv[1]
    directory = sys.argv[2] #cli argument as directory
else:
    how_many_lines_to_combine = 10
    directory = script_dir #default to script directory as directory

directory_path = Path(directory) #convert string to path?
print("Directory path", directory_path)

for file_path in directory_path.glob("*.srt"): #only get srt files
    print("File " + str(file_path))
    timestamps_and_text_only = ""
    combined_output_text = ""

    with (file_path.open("r", encoding="utf-8") as file):
        SKIP_NEXT_LINE = False
        for index, line in enumerate(file):

            if line == "\n":
                SKIP_NEXT_LINE = True #skips the paragraph break
            elif SKIP_NEXT_LINE == True:
                SKIP_NEXT_LINE = False  # skips the stamp number
            else:
                timestamps_and_text_only += (line)
                # add only timestamps and text to file

        transcript = timestamps_and_text_only
        #print(transcript)
        stamp_list = list(re.finditer(
            r"\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d",
            transcript))
        #get time stamp locations and turn into list from iterator

        for n,stamp in enumerate(stamp_list):
            #print("stamp",n, (stamp.span())[0])
            if n % how_many_lines_to_combine == 0:
                if n != 0:
                    combined_output_text += "\n"
                if n + how_many_lines_to_combine > len(stamp_list) - 1:
                    x = len(stamp_list) - n - 1

                    combined_output_text += transcript[stamp.span()[0]:stamp.span()[0] + 17]
                    # first part of timestamp
                    combined_output_text += transcript[stamp_list[n + x].span()[0] + 17:stamp_list[n + x].span()[0] + 29]
                    # second part of timestamp
                    combined_output_text += "\n"
                    # add newline break after every timestamp
                else:
                    combined_output_text += transcript[stamp.span()[0]:stamp.span()[0] + 17]
                    # first part of timestamp
                    combined_output_text += transcript[stamp_list[n + how_many_lines_to_combine].span()[0] + 17:stamp_list[n + how_many_lines_to_combine].span()[0] + 29]
                    # second part of timestamp
                    combined_output_text += "\n"
                    # add newline break after every timestamp
            if n + 1 > len(stamp_list) - 1:
                #if this is the final stamp
                combined_output_text += transcript[stamp.span()[0] + 29:] #final text
            else:
                #all other stamps
                #print(transcript[stamp.span()[0] + 29:stamp_list[n + 1].span()[0]].index('\n'))
                if n % how_many_lines_to_combine == 0:
                    pass
                #do not add space to first line of each paragraph
                else:
                    combined_output_text += " "
                combined_output_text += transcript[stamp.span()[0] + 29:stamp_list[n + 1]
                .span()[0]].strip().replace("\n", " ").replace("\xa0", "")
                #text between stamps, stripped of leading and trailing spaces, removing any line breaks and removing nbsp
                #line breaks

                if ((n + 1) % how_many_lines_to_combine == 0) & (n != 0):
                    combined_output_text += "\n"
                #add newline break after end of every paragraph

        with open((str(file_path)+".txt"), "w", encoding="utf-8") as file:
            file.write(combined_output_text)
            #create new file