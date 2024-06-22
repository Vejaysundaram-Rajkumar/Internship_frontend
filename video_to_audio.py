import moviepy.editor 
import os

def converter(path,filename):
    cvt_vd = moviepy.editor.VideoFileClip(path)
    ext_ad= cvt_vd.audio
    
    output_directory = "D:\\projects\\Internship_frontend\\uploads"
    # Create the full output file path
    name = os.path.join(output_directory, filename.split('.')[0] + "_audio.mp3")
    ext_ad.write_audiofile(name)
    cvt_vd.close()
    ext_ad.close()
    return name