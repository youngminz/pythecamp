import json
import logging

import requests

logger = logging.getLogger(__name__)


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/76.0.3809.132 Safari/537.36"
    })
    session.hooks = {
        'response': [
            lambda r, *args, **kwargs: logger.info(f'RESPONSE {r.status_code} {r.text}'),
            lambda r, *args, **kwargs: r.raise_for_status(),
        ]
    }

    return session


class TheCampRequestError(Exception):
    ...


class TheCampClient:
    API_HOST = 'https://www.thecamp.or.kr'

    def __init__(self):
        self.session = build_session()

    def _request(self, endpoint: str, data: dict) -> dict:
        without_credential = data.copy()
        if 'user-pwd' in without_credential:
            without_credential['user-pwd'] = '********'
        logger.info(f'REQUEST {endpoint} with data {without_credential}')
        res = self.session.post(f'{self.API_HOST}{endpoint}', json=data)

        if res.json()['resultCode'] != 200:
            raise TheCampRequestError(f'TheCamp 응답 코드가 예상 응답 코드와 다릅니다. {res.text}')

        return res.json()

    def login(self, username: str, password: str) -> None:
        logger.info(f'로그인을 시도합니다. username: {username}')
        self._request('/pcws/common/login.do', {'subsType': '1', 'user-id': username, 'user-pwd': password})
        logger.info('로그인에 성공하였습니다.')

    def get_group_list(self) -> dict:
        logger.info('가입 카페 목록을 가져옵니다.')
        res = self._request('/pcws/troop/group/getMyGroupList.do', {})
        logger.info(f"가입 카페 목록을 가져왔습니다.")
        return json.loads(res['resultData']['list2'])['my_group']

    def get_trainee(self, group_id: str) -> dict:
        logger.info(f'그룹 {group_id}의 훈련생을 조회합니다.')
        res = self._request('/pcws/camppack/getList.do', {'group_id': group_id})
        logger.info(f'그룹 {group_id}의 훈련생을 가져왔습니다.')
        # 리스트를 조회하는데 결과로 리스트가 안 내려오는 건 좀 이상하다..
        return json.loads(res['resultData']['data'])['trainee_info']

    def write_letter(
        self,
        title: str,
        content: str,
        unit_code: str,
        group_id: str,
        name: str,
        birth_date: str,
        relationship: str
    ) -> None:

        logger.info(f'편지를 씁니다.')
        self._request('/pcws/message/letter/insert.do', {
            'unit_code': unit_code,
            'group_id': group_id,
            'trainee_name': name,
            'birth': int(birth_date),
            'relationship': relationship,
            'fileInfo': [],
            'title': title,
            'content': content,
        })
        logger.info('편지 쓰기 완료!')

    def logout(self) -> None:
        logger.info('로그아웃을 시도합니다.')
        self.session.get(f'{self.API_HOST}/pcws/common/logout.do', allow_redirects=False)
        logger.info('로그아웃 성공!')
