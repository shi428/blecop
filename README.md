# BLecOpS

The **B**oilermaker's **Lec**ture **Op**timizing **S**ystem. Written for the [BoilerMake VII Hackathon](https://boilermake-vii.devpost.com/). Recipient of the Wolfram award (awarded to top 20 hacks).

BLecOpS applies [Bootstrapping](https://en.wikipedia.org/wiki/Bootstrapping_(statistics)) to identify a quitest speaking volume and removes portions of video that only contain background noise. This enables more effective consumption of videos where information is tied to the loudest volume source (speaking, usually).

## Inspiration

The fall of my sophomore year, I planned to review 10+ hours worth of lectures to prepare for an exam. As I began to watch and study these recordings, a problem came to reoccur; a significant amount of time of each and every lecture was comprised of "dead time", where the lecturer would spend time writing something on the board, pondering quietly or the beginning/ending of each recording. While I could get around this by fast-forwarding through said parts or watching the lecture on a faster playback rate, this each came with a set of drawbacks as well. The first took attention away, the latter making it harder to understand. We looked to create a program to make this process of watching lectures and studying more effective.

## Methodology

BLecOpS applies bootstrapping to determine the quietest speaking volume in the given lecture. Bootstrapping is asymptotically consistent to the population distribution; we assume that the frequency distribution of volumes in a lecture video is multimodal with the largest peak as the loudest. We model sound sources (lecture speaking, background white nose, audience noise) as seperate distributions with the lecture speaking as both the loudest and most frequent non-constant volume source. By bootstrapping for the maximum, we expect to obtain values centered around the loudest peak -- the distribution of talking volumes. Then to obtain the quietest speaking volume, we take the minimum of these maximums. With this statistic, the program processes the video and denotes sections of the lecture where the volume is quieter than the speaking volume, which we assume to be "dead time", made optimized by Python's [numpy](https://github.com/numpy/numpy). BLecOpS processes the audio by converting the video in a `.wav` file through Python's [wavefile API](https://github.com/python/cpython/blob/master/Lib/wave.py).

Through [`ffmpeg`](https://ffmpeg.org/), BLecOpS converts the video into a more suitable encoding `.mpeg` instead of the more commonly used `.mp4` encoding. Once the program has determined a suitable volume and has denoted sections of the video, it again uses ffmpeg's API to split the video into segments of speaking portions, removing sections of the lecture where nothing is being spoken. BLecOpS uses `ffmpeg` a final time to stitch these clips together into a merged lecture.

## Experimental Data

Original lecture videos were 60 minutes.

| Techniques | Maximum Modified Video Length (minutes) |
|-|-|
| Bootstrapping for the minimum of the maximum volumes, `ffmpeg` splicing on `.mp4` file | 45 |
| Bootstrapping for the minimum of the maximum volumes, `ffmpeg` splicing on `.mpeg` file | 28 |
