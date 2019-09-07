=========
pythecamp
=========


.. image:: https://img.shields.io/pypi/v/pythecamp.svg
        :target: https://pypi.python.org/pypi/pythecamp

.. image:: https://img.shields.io/travis/youngminz/pythecamp.svg
        :target: https://travis-ci.org/youngminz/pythecamp

인터넷 편지를 보낼 수 있게 해 주는 파이썬 라이브러리입니다.

.. code:: python

    import pythecamp

    client = pythecamp.TheCampClient()
    client.login('<TheCamp Login ID>', '<TheCamp Login Password>')
    groups = client.get_group_list()
    trainees = client.get_trainee(groups[0]['group_id'])
    client.write_letter(
        '제목',
        '편지 내용',
        groups[0]['unit_code'],
        groups[0]['group_id'],
        trainees['trainee_name'],
        trainees['birth'],
        trainees['relationship'])
    client.logout()
