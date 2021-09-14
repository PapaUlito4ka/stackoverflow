from django.test import TestCase

# Create your tests here.
QUESTIONS = [
    {
        'title': 'Title1',
        'views': 0,
        'votes': 0,
        'text': 'Some very long text with a lot of words in it bla bla bla bla bla bla bla bla bla bla bla bla',
        'answers': [1, 2, 3],
        'tags': ['Tag1', 'Tag2', 'Tag3'],
        'author': 'Artem'
    },
    {
        'title': 'Title2',
        'views': 2,
        'votes': -2,
        'text': 'Some very long text with a lot of words in it bla bla',
        'answers': [1, 2],
        'tags': ['Tag1', 'Tag2'],
        'author': 'Artem'
    },
    {
        'title': 'Title3',
        'views': 10,
        'votes': 5,
        'text': 'Some very long text with a lot of words in it',
        'answers': [1],
        'tags': ['Tag1'],
        'author': 'Artem'
    },
    {
        'title': 'Title1',
        'views': 0,
        'votes': 0,
        'text': 'Some very long text with a lot of words in it bla bla bla bla bla bla bla bla bla bla bla bla',
        'answers': [1, 2, 3],
        'tags': ['Tag1', 'Tag2', 'Tag3'],
        'author': 'Artem'
    },
    {
        'title': 'Title2',
        'views': 2,
        'votes': -2,
        'text': 'Some very long text with a lot of words in it bla bla',
        'answers': [1, 2],
        'tags': ['Tag1', 'Tag2'],
        'author': 'Artem'
    },
    {
        'title': 'Title3',
        'views': 10,
        'votes': 5,
        'text': 'Some very long text with a lot of words in it',
        'answers': [1],
        'tags': ['Tag1'],
        'author': 'Artem'
    },
    {
        'title': 'Title1',
        'views': 0,
        'votes': 0,
        'text': 'Some very long text with a lot of words in it bla bla bla bla bla bla bla bla bla bla bla bla',
        'answers': [1, 2, 3],
        'tags': ['Tag1', 'Tag2', 'Tag3'],
        'author': 'Artem'
    },
    {
        'title': 'Title2',
        'views': 2,
        'votes': -2,
        'text': 'Some very long text with a lot of words in it bla bla',
        'answers': [1, 2],
        'tags': ['Tag1', 'Tag2'],
        'author': 'Artem'
    },
    {
        'title': 'Title3',
        'views': 10,
        'votes': 5,
        'text': 'Some very long text with a lot of words in it',
        'answers': [1],
        'tags': ['Tag1'],
        'author': 'Artem'
    }
]