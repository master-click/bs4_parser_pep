import errno
import logging
import re
from collections import Counter
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEP_URL
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'})
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Список с версиями Python на странице не найден.')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_link = a_tag.text
        text_match = re.search(pattern, text_link)
        if text_match is not None:
            version = text_match.group('version')
            status = text_match.group('status')
        else:
            version = text_link
            status = ''
        results.append((link, version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    soup = BeautifulSoup(response.text, 'lxml')
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    try:
        downloads_dir.mkdir(exist_ok=True)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    try:
        with open(archive_path, 'wb') as file:
            file.write(response.content)
        logging.info(f'Архив был загружен и сохранён: {archive_path}')
    except EnvironmentError as error:
        logging.error(f'Архив не был загружен. Ошибка: {error}')


def pep(session):
    response = get_response(session, PEP_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    section_tag = find_tag(soup, 'section', {'id': 'numerical-index'})
    tbody_tag = find_tag(section_tag, 'tbody')
    tr_tag = tbody_tag.find_all('tr')
    data = []
    for tr in tqdm(tr_tag):
        preview_status = find_tag(tr, 'abbr').text[1:]
        a_tag = tr.find('a')
        href = a_tag['href']
        link = urljoin(PEP_URL, href)
        response = get_response(session, link)
        soup = BeautifulSoup(response.text, 'lxml')
        dl = find_tag(soup, 'dl')
        for dt in soup.find_all('dt'):
            if 'Status:' in dt.text:
                status_page = find_tag(dl, 'abbr')
                data.append(
                    (link, preview_status, status_page.text)
                )
    all_status = []
    for item in data:
        if item[1] == item[2][0]:
            all_status.append(item[2])
        else:
            if item[1] == '' and item[2] == 'Draft' or item[2] == 'Active':
                all_status.append(item[2])
            else:
                logging.info(f'Несовпадающие статусы: \n'
                             f'{item[0]} \n'
                             f'Статус в карточке: {item[2]} \n'
                             f'Ожидаемые статусы: '
                             f'{EXPECTED_STATUS[item[1]]}'
                             )
    results = [('Статус', 'Количество')]
    counter = dict(Counter(all_status))
    results.extend((counter.items()))
    results.append(('Total', len(all_status)))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
