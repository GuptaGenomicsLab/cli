import click
import json
from io import FileIO
from requests import Session
from sseclient import SSEClient

BASE_URL = 'https://api.appindels.com'


@click.command()
@click.argument('genome', type=click.File('r'))
@click.option('--output', '-o', default='results.json')
@click.option('--username', type=str, prompt=True, required=True)
@click.option('--description', type=str, default='Single Query - CLI')
@click.password_option(confirmation_prompt=False)
def single_query(
        genome: FileIO,
        username: str,
        password: str,
        output: str,
        description: str
) -> None:

    session = login(username, password)
    query_id = start_query(genome, description, session)
    await_query(query_id, session)
    results = fetch_results(query_id, session)

    with open(output, 'w') as f:
        f.write(json.dumps(results, indent=4))

    tree = json.loads(results['data']['tree'])

    click.secho(f"Results written to {output}. {count_csis(tree)} CSIs found.", fg='green')


def login(
        username: str,
        password: str
) -> Session:
    session = Session()
    res = session.post(
        f'{BASE_URL}/auth/login',
        json={
            'username': username,
            'password': password,
            'rememberMe': False
        }
    )

    if res.json()['username'] != username:
        raise RuntimeError('Login failed')

    return session


def start_query(
        genome: FileIO,
        description: str,
        session: Session
) -> str:
    res = session.post(
        f'{BASE_URL}/blast/start-query',
        files=dict(file=genome),
        data=dict(description=description, sequenceType='Nucleotide')
    )

    query_id = res.content.decode('utf-8')
    return query_id


def await_query(query_id: str, session: Session) -> None:
    res = session.get(
        f'{BASE_URL}/blast/query-progress/{query_id}',
        stream=True
    )

    client = SSEClient(res)
    for msg in client.events():
        print(msg.data)
        if 'Completed' in msg.data:
            client.close()
            break
    res.close()


def fetch_results(query_id: str, session: Session):
    res = session.get(f'{BASE_URL}/blast/query/{query_id}')
    return res.json()


def count_csis(node: dict[str, any]) -> int:
    cnt = len(node['specificHits'])
    for child in node['children'].values():
        cnt += count_csis(child)
    return cnt
