# Kerbor
Kerbor is a kerberos-like protocol implementation

# Installation
```
git clone https://github.com/kibach/kerbor.git && cd kerbor
pip install -r requirements.txt
python serve.py
```

Now, open http://127.0.0.1:5000/newuser in your browser and register new user. For example: test/123098

In separate terminal:

```
python client.py test 123098
```

If auth is successful, it just outputs `True`.
