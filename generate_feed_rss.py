import boto3
import os
import re
import json
from botocore.client import Config
from feedgen.feed import FeedGenerator

BUCKET_NAME = 'depoisdocafe'
DO_SPACES_URL = 'https://ams3.digitaloceanspaces.com'
DO_SPACES_CDN = 'http://media.blubrry.com/depois_do_caf_com_airton_zanon/conteudo.depois.cafe/{uri}'

session = boto3.session.Session()
client = session.client('s3',
                        region_name='ams3',
                        endpoint_url=DO_SPACES_URL,
                        aws_access_key_id=os.environ['DO_ACCESS_KEY'],
                        aws_secret_access_key=os.environ['DO_SECRET_KEY'])

bucket_content = client.list_objects(Bucket=BUCKET_NAME)

files = [content['Key'] for content in bucket_content['Contents']]

extras = []
episodes = []

for file in files:
    if not re.search('extras/([\w-]+).mp3', file):
        continue

    file_name = re.findall('(extras/[\w-]+).mp3', file)[0]
    details_json = client.get_object(
        Bucket=BUCKET_NAME,
        Key=file_name + '.json'
    )

    details_mp3 = client.get_object(
        Bucket=BUCKET_NAME,
        Key=file
    )

    extras.append({
        **{
            'mp3_link': DO_SPACES_CDN.format(
                uri=file
            ),
            'mp3_size': details_mp3['ContentLength'],
            'mp3_type': details_mp3['ContentType']
        },
        **json.loads(details_json['Body'].read().decode())
    })

podcast_description = """Episódios exclusivos com audios cortados e/ou conteúdo novinho"""

podcast_author = 'Airton Zanon'
podcast_email = 'depoisdocafe@airton.dev'
podcast_cover = 'https://conteudo.depois.cafe/depois-do-cafe-exclusivo.png'

fg = FeedGenerator()
fg.load_extension('podcast')

fg.id('https://episodios.depois.cafe')
fg.title('Depois do Café Exclusivo')
fg.subtitle(podcast_description)
fg.author({'name': podcast_author, 'email': podcast_email})
fg.link(href='https://episodios.depois.cafe', rel='alternate')
fg.link(
    href='https://episodios.depois.cafe',
    rel='self', type='application/rss+xml'
)
fg.logo(podcast_cover)
fg.language('pt-BR')
fg.generator('https://github.com/lkiesow/python-feedgen')
fg.copyright(podcast_author)

fg.podcast.itunes_author(podcast_author)
fg.podcast.itunes_category('Technology')
fg.podcast.itunes_subtitle(podcast_description)
fg.podcast.itunes_summary(podcast_description)
fg.podcast.itunes_owner(
    name=podcast_author,
    email=podcast_email
)
fg.podcast.itunes_explicit('no')
fg.podcast.itunes_image(podcast_cover)


for ep_extra in extras:
    entry = fg.add_entry()
    entry.title(ep_extra['title'])
    entry.id(ep_extra['mp3_link'])
    entry.link(href=ep_extra['mp3_link'], rel='alternate')
    entry.enclosure(
        ep_extra['mp3_link'],
        str(ep_extra['mp3_size']),
        ep_extra['mp3_type']
    )
    entry.pubDate(ep_extra['pub_date'])
    entry.description(ep_extra['description'])

    entry.podcast.itunes_explicit('no')
    entry.podcast.itunes_image(podcast_cover)
    entry.podcast.itunes_author(podcast_author)
    entry.podcast.itunes_summary(ep_extra['description'])
    entry.podcast.itunes_subtitle(ep_extra['description'])
    entry.podcast.itunes_duration('00:00:00')


rssfeed = fg.rss_str(pretty=True)

client.put_object(
    Bucket=BUCKET_NAME,
    Body=rssfeed,
    Key='extras-feed.xml',
    ACL='public-read',
    ContentType='text/xml'
)

