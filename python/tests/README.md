# Tests details

They are aimed to be done using pytest.  
A pytest.ini is present to ensure the configuration.  

Requirements :

```
/code # pip3 install pytest
```

Run the Tests :

```
/code # pytest
======================== test session starts ========================
platform linux -- Python 3.8.2, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /code
collected 10 items

tests/test_00_vars.py ..                                      [ 20%]
tests/test_01_auth.py ......                                  [ 80%]
tests/test_02_data.py ..                                      [100%]

======================== 10 passed in 0.30s =========================
```

tests/test_00_vars.py:  
- If env var containing the tokens exists
- If test token is inside

tests/test_01_auth.py:
- If with wrong token, every production route return a 401 Unauthorized
- If with right token, every production route return a 200 OK

tests/test_02_data.py:
- If returned data are JSON & containing an expected element
