# pythecamp

인터넷 편지를 Python으로 보낼 수 있게 해 주는 라이브러리입니다.

```python
import pythecamp

client = pythecamp.TheCampClient()
client.login('<TheCamp Login ID>', '<TheCamp Login Password>')
groups = client.get_group_list()
trainees = client.get_trainee(groups[0]['group_id'])
client.write_letter(
    title='Letter Title',
    content='Letter Content',
    unit_code=groups[0]['unit_code'],
    group_id=groups[0]['group_id'],
    name=trainees['trainee_name'],
    birth_date=trainees['birth'],
    relationship=trainees['relationship'])
client.logout()
```
