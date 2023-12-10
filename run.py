import os

import requests


def download_pdf(url, name):
    pdf_name = '%s.pdf' % name
    if os.path.exists(pdf_name) and os.path.getsize(pdf_name) >= 0:
        print('Already there', pdf_name)
        return

    r = requests.get(url, stream=True)

    with open(pdf_name, 'wb') as f:
        for chunck in r.iter_content(1024):
            f.write(chunck)
    r.close()


from tqdm import tqdm
def loop(save_dir_nips):
    import openreview

    # API V2
    client = openreview.api.OpenReviewClient(
        baseurl='https://api2.openreview.net',
        username='yba@g.ucla.edu',
        password=''
    )

    i = 0
    for type in ['Conference', 'Track/Datasets_and_Benchmarks']:
        save_dir = os.path.join(save_dir_nips, type.replace('/', '_'))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)


        accepted_submissions = client.get_all_notes(content={'venueid': f'NeurIPS.cc/2023/{type}'})

        for accepted_submission in tqdm(sorted(accepted_submissions, key=lambda x: x.number)):
            i += 1 # 1-based indexing
            title = accepted_submission.content['title']['value']

            title = title.replace('/', '_')
            filename = f'{i} {accepted_submission.number} {title}'
            print(accepted_submission.id, filename)
            download_pdf(f'https://openreview.net/pdf?id={accepted_submission.id}', os.path.join(save_dir, filename))
            # author_profiles = openreview.tools.get_profiles(client, accepted_submission.content['authorids']['value'])
            # for author_profile in author_profiles:
            #     print(author_profile.get_preferred_name(pretty=True), author_profile.content.get('history', [{}])[0])

if __name__ == '__main__':
    year = 2023
    save_dir_nips = f'/Users/yba/Documents/Work/paper/neurips_crawler/openreview_scraper/papers/{year}'
    loop(save_dir_nips)
