# Video source

Performance recordings on the SNH48 Live channel come directly from on-demand recordings provided by [live.snh48.com](http://live.snh48.com/).

Each VOD page, e.g. <http://live.snh48.com/Index/invedio/id/148>, embeds three M3U8 streams directly in the HTML, corresponding to qualities "超清", "高清" and "普清". The highest quality "超清" stream, currently at 1080p (details below), matches the regex `https?://ts.snh48.com/[^"]*chaoqing[^"]*\.m3u8(?=")`, e.g.,

    http://ts.snh48.com/recordings/z1.chaoqing.9999/20170324/58c8af6d0cf2189f10317548.m3u8

so it should be very easy to extract. Once we have the .m3u8 file, the rest is trivial. Personally, I use a massive number of concurrent Wget processes to download the segments (made easy with GNU Parallel), then join them with FFmepg.

At the moment (03/24/2017), the highest quality streams offered by live.snh48.com contain 1080p H.264 video streams at 25fps and a bitrate of ~3800 kbps, and ~128 kbps AAC audio streams. The resulting video files measure ~1.6 GiB per hour. I always upload the uncut original streams to YouTube (with at most timestamp fixes done by FFmpeg, except when certain segments are damaged and unsalvageable, in which case they are removed with a notice).

The actual highest quality as served by YouTube appears to vary accross browsers, but `youtube-dl --list-formats` should almost always find you the highest quality streams.
