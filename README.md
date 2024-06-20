# Ollama running Mixtral/Mistral with LLamaIndex

Following the blog tutorial in https://blog.llamaindex.ai/running-mixtral-8x7-locally-with-llamaindex-e6cebeabe0ab with the exception of fixing the deprecated `download_loader()` calls, which run into timeouts. 

## Source code updates 

Inside the source code, the deprecation note for `download_loader()` is visible, but the docs are not updated yet.

To load a JSON file, use the following snippet:

```python
from llama_hub.file.json import JSONReader

# load the JSON off disk
loader = JSONReader()
documents = loader.load_data(Path('./data/tweets.json'))
```

You can read the full analysis in this blog post. 

## Requirements

Install [Ollama](https://ollama.ai/) and ensure it is running. Download run either `mixtral` (requires 48 GB RAM to work properly) or `mistral` (used in this example).

```
ollama run mistral
```

Python packages:

```
pip3 install llama-index qdrant_client torch transformers

# download_loader() is deprecated. Use llama-hub instead 
pip3 install llama-hub
```

Or shorter:
```
pip3 install -r requirements.txt 
```

### Twitter archive

1. Download your archive from Twitter/X.
1. Extract the archive and follow the instructions from https://gist.github.com/duner/8b1dc63c26eb774d43a21c0faa2fa9aa?permalink_comment_id=3666012#gistcomment-3666012 to convert the JS files into JSON.

```
cd data 

rsync -I --backup --suffix='.json' --backup-dir='json' --exclude='manifest.js' ./*.js ./\nsed -i -r 's/^window.*\ \=\ (.*)$/\1/' json/*
```

Test

```
cd json/

jq '.[] | .tweet | select(.entities.urls != []) | .entities | .urls | map(.expanded_url) | .[]' tweets.js.json | cut -d'/' -f3 | sed 's/\"//g' | sort | uniq -c | sort -g
```

You can do the same in the `data/` directory.

```shell
cd data

jq '.[] | .tweet | select(.entities.urls != []) | .entities | .urls | map(.expanded_url) | .[]' *.json | cut -d'/' -f3 | sed 's/\"//g' | sort | uniq -c | sort -g

      8 www.everyonecancontribute.com
     10 grafana.com
     10 news.ycombinator.com
     10 open.spotify.com
     10 www.meetup.com
     13 www.linkedin.com
     14 stackoverflow.com
     14 t.co
     16 docs.google.com
     19 m.xkcd.com
     22 xkcd.com
     25 dev.to
     26 GitLab.com
     33 opsindev.news
     39 everyonecancontribute.com
     44 dnsmichi.at
     52 forum.gitlab.com
     61 docs.gitlab.com
     62 bit.ly
    122 www.youtube.com
    130 github.com
    216 youtu.be
    236 about.gitlab.com
    269 buff.ly
    348 gitlab.com
   1134 twitter.com
```

### Replace existing tweets.json

Delete the symlink, and create a new one for your data sets.

```shell
cd data/
rm tweets.json

ln -s your_tweets.json tweets.json
```

This allows to test and load different data sets, without changing the source code, or renaming files.