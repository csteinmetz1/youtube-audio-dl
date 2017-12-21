# youtube-audio-dl
There are a number of online platforms that download and convert YouTube video streams to mp3 but they tend to be slow, clunky, and ad ridden. This project serves to provide an easy way to automate the download and conversion process. It also automatically peak normalizes the streams since many talks/lectures suffer from low volume.

## Installation 
Clone this repo and install the dependancies listed below.
```
git clone https://github.com/csteinmetz1/youtube-audio-dl
```

## Usage
Place a list of newline delimited YouTube URLs in a `.txt` file. Then simply run the script with the path to that `.txt`. This will download the audio streams in the current working directory.

```
python youtube-audio-dl urls.txt
```

Optionally pass a directory to store the downloaded files. Ensure that this directory exists beforehand.
```
python youtube-audio-dl urls.txt ./downloads
```

## Depedancies
* **pafy** ( [https://github.com/mps-youtube/pafy](https://github.com/mps-youtube/pafy) )
* **ffmpeg** ( [https://www.ffmpeg.org/download.html](https://www.ffmpeg.org/download.html) )
* **ffmpeg-normalize** ( [https://github.com/slhck/ffmpeg-normalize](https://github.com/slhck/ffmpeg-normalize) )
