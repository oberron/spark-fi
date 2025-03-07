import sys
# pathlib.Path.walk introduced in py 3.12
# https://docs.python.org/3.12/library/pathlib.html#pathlib.Path.walk
assert sys.version_info >= (3, 12)

from pathlib import Path
import jinja2
import datetime
import ffmpeg as myff
from shutil import copyfile

"""podcast_header=<?xml version="1.0" encoding="UTF-8" ?>
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:rawvoice="http://www.rawvoice.com/rawvoiceRssModule/"
     xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">
  <channel>
    <title>Papa lit et au lit</title>
    <atom:link href="http://dallas.example.com/rss.xml" rel="self" type="application/rss+xml" />
    <rawvoice:rating>TV-G</rawvoice:rating>
    <rawvoice:location>Au clair de la lune</rawvoice:location>
    <rawvoice:frequency>Weekly</rawvoice:frequency>
    <itunes:author>Aubéron Vacher</itunes:author>
    <itunes:summary>De petites histoires, a lire ou a ecouter avant d'aller au lit.
    Des contes merveilleux classiques, ou parfois adaptees librement, occidentaux mais aussi d'autres regions du monde.
    Pour les curieux, le lien a la classification ATU est presente pour permettre d'explorer toutes le variantes au dela de ce que l'industrie des loisir peut parfois presenter comme une histoire unique.</itunes:summary>
    <itunes:category text="Kids &amp; Family" >
    <itunes:category text="Stories for Kids" />
    </itunes:category>
    <itunes:subtitle>Seulement pour les enfants sages !</itunes:subtitle>
    <image>
      <url>https://oberron.github.io/spark-fi/static/img/moon.png</url>
      <title>Papa lit et au lit</title>
      <link>https://oberron.github.io/spark-fi/</link>
    </image>
    <itunes:owner>
      <itunes:name>Aubéron Vacher</itunes:name>
      <itunes:email>one.annum@gmail.com</itunes:email>
    </itunes:owner>
    <itunes:keywords>comptines, histoires</itunes:keywords>
    <copyright>Entolusis - 2004 - 2020</copyright>
    <description>Une petite histoire avant d'aller au lit</description>
    <language>fr-fr</language>
    <itunes:explicit>false</itunes:explicit>
    <pubDate>Sat, 10 Oct 2020 11:00:00 GMT</pubDate>
    <link>https://oberron.github.io/spark-fi/</link>
    <itunes:image href="https://oberron.github.io/spark-fi/static/img/moon.png" />"""

def make_podcast(fpo,dpo=None):

    temp_dp = "C:/git/spark-fi/static/theme/templates"
    templateLoader = jinja2.FileSystemLoader(searchpath=temp_dp)
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_CHANNEL_fn = "podcast_channel.j2"
    TEMPLATE_ITEM_fn = "podcast_item.j2"
    template_channel = templateEnv.get_template(TEMPLATE_CHANNEL_fn)
    template_item = templateEnv.get_template(TEMPLATE_ITEM_fn)
    title = "Le loup le renard et le pot de miel"
    pubdate = datetime.datetime(2020,10,10,19,0,0).strftime("%a, %d %b %Y %H:%M:%S GMT")

    if not dpo is None:
        if not Path(dpo).exists():
            Path(dpo).mkdir(parents=True, exist_ok=True)

    dp = Path(__file__).parents[0] / "player"/ "web"/ "audio"
    items = {}
    for root, fold, files in dp.walk():
        for f in files:
            if str(f).find(".mp3")<0:
                continue
            fp = dp/f
            size = fp.stat().st_size  # getsize(fp)
            guid = Path(fp).stem
            print(72, fp)
            duration = float(myff.probe(str(fp))['format']['duration'])
            dur_mn = int(float(duration) // 60)
            print("dur mn", duration, dur_mn)
            dur_sec = int(float(duration) - 60*dur_mn)
            duration = f"{dur_mn:02d}:{dur_sec:02d}"
            print(f"files mp3: {guid}", size, duration)
            items[guid.upper()]={"size": size, "duration": duration, "fn":f, "fp": fp}

    dp = Path("C:\\git\\spark-fi\\content")
    atus = {}
    def _get_meta(fc, meta):
        meta+=": "
        start = fc.find(meta)
        end = fc.find("\n", start)
        if end>-1:
            res = fc[start+len(meta):end]
        else:
            res = ""
        return res
    for root, fold, files in dp.walk():
        for f in files:
            fn = str(f)
            if fn.find(".md")<0:
                continue
            fp = str(root / f)

            try:
                with open(fp, encoding="utf-8") as fi:
                    fc = fi.read()
            except:
                raise
            res = _get_meta(fc,"category")
            if _get_meta(fc,"category") == "ATU":
                atu=_get_meta(fc,"tags")
                title = _get_meta(fc,"title")
                date = _get_meta(fc,"date")
                summary = _get_meta(fc,"summary")
                atus[atu.upper()]={"fp": fp, "title": title, "date": date, "summary": summary}
    podcast_items = ""

    for guid in items:
        if guid == "HISTOIRE_01":
            continue
        size = items[guid]["size"]
        duration = items[guid]["duration"]
        fn = items[guid]["fn"]
        #if guid=="HISTOIRE_02":
        #    guid="ATU15"
        title = atus[guid]["title"]
        summary = atus[guid]["summary"]
        summary += """
        Aubéron Vacher - @oberron
        (C) 2020-2025
        https://twitter.com/oberron
        https://github.com/oberron
        Our podcast player:
        https://github.com/oberron/spark-fi/podcast-player/"""

        title = f"{title} - ({guid})"
        pubdate = datetime.datetime.strptime(atus[guid]["date"],"%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S GMT")

        conf_item={"AUTHOR":"OBERRON",
                   "ITEM_TITLE": title,
                   "ITEM_SUBTITLE": title,
                   "ITEM_SUMMARY": summary,
                   "ITEM_DESCRIPTION": atus[guid]["summary"],
                   "ITEM_PUBDATE": pubdate,
                   "ITEM_SIZE": size,
                   "ITEM_FN":fn,
                   "ITEM_DURATION": duration,
                   "ITEM_GUID": guid}
        outputText = template_item.render(conf_item)
        fpo = str(Path(dpo) / items[guid]["fn"])
        print("fpo", fpo)
        copyfile(items[guid]["fp"], fpo)
        podcast_items += outputText

    conf_channel = {"CHANNEL_TITLE":"Papa lit et au lit",
                    "CHANNEL_GUID":"a22393c8-12a8-5ce3-8c61-0beebb73ad7f",
                    "CHANNEL_URL": "http://51.38.114.108/player/web/feed_new2.xml",
                    "CHANNEL_AUTHOR_NAME":"Aubéron Vacher",
                    "CHANNEL_AUTHOR_EMAIL":"one.annum@gmail.com"}
    podcast_channel = template_channel.render(conf_channel)
    podcast = podcast_channel+"\n"+podcast_items+"\n"+"</channel>\n</rss>"
    fpo = str(Path(dpo) /"papa-lit-et-au-lit.xml")

    with open(fpo, "w", encoding="utf-8") as fo:
        fo.write(podcast)
    print("podcast written at", fpo)
