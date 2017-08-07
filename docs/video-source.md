# Video source

Performance recordings on the SNH48 Live channel come directly from on-demand recordings provided by [live.snh48.com](http://live.snh48.com/).

Each VOD page, e.g. <http://live.snh48.com/Index/invedio/id/250>, embeds three M3U8 streams directly in the HTML, corresponding to qualities "超清", "高清" and "普清". The highest quality "超清" stream, currently at 1080p (details below), matches the regex `https?://ts.snh48.com/[^"]*chaoqing[^"]*\.m3u8(?=")`, e.g.,

    http://ts.snh48.com/vod/z1.chaoqing.9999/20170630/594b43460cf2d32bde50ba48.mp4/playlist.m3u8

so it should be very easy to extract. Once we have the .m3u8 file, the rest is trivial. Personally, I use a massive number of concurrent Wget processes to download the segments (made easy with GNU Parallel), then join them with FFmepg. See [`download`](../bin/download) for my implementation.

Note that if you remove `/playlist.m3u8` from the aforementioned URL, e.g.

    http://ts.snh48.com/vod/z1.chaoqing.9999/20170630/594b43460cf2d32bde50ba48.mp4

that points to a standalone MP4 file (these weren't available when I started the channel; just check the history of this document). Therefore, if a single-threaded download can saturate your download bandwidth, or if you're comfortable with a segmented downloader like aria2, you may choose to directly download this standalone file and not bother with merging. Sample command line with aria2:

    aria2c -x 16 -s 16 http://ts.snh48.com/vod/z1.chaoqing.9999/20170630/594b43460cf2d32bde50ba48.mp4

Note that this MP4 file will have its moov atom at the end of the file, so you still want to remux it to move the moov atom to the beginning (FFmpeg: `-movflags faststart`) in order to facilitate streaming and [easier processing on YouTube's part](https://support.google.com/youtube/answer/1722171?hl=en).

From my limited testing from US East, performance of `parallel -j20 wget` chunks and `aria2c -x16 -s16` single file are similar on cache miss, usually averaging to ~50Mbps; on cache hit aria2 is a fair bit faster, likely due to much less overhead. For certain (religious?) reasons I'm not a big fan of aria2, and when I first wrote my downloader there was no such standalone MP4 yet, so I'll continue to download chunks and concatenate them myself.

At the moment (08/06/2017), the highest quality streams offered by live.snh48.com contain 1080p H.264 video streams at 25fps and a bitrate of ~3500 kbps, and ~128 kbps AAC audio streams. The resulting video files measure ~1.5 GiB per hour. I always upload the uncut original streams to YouTube (with at most timestamp fixes done by FFmpeg, except when certain segments are damaged and unsalvageable, in which case they are removed with a notice).

The actual highest quality as served by YouTube appears to vary accross browsers, but `youtube-dl --list-formats` should almost always find you the highest quality streams.
