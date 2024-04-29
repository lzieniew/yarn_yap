from shared_components.db_init import init_db
from shared_components.models import Sentence
from shared_components.utils import run_async
from shared_components import Job


run_async(init_db())
jobs = run_async(Job.find(fetch_links=True, nesting_depth=1).to_list())
job = jobs[0]
# here put debug things and call from inside docker container:
# docker exec -it yarn_yap-web-1 /bin/bash
# and then
# python debug_script.py

sentence = job.sentences[0]

run_async(sentence.fetch_all_links())
print(sentence.audio_data)
