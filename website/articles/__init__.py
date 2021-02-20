from model_utils import Choices

ARTICLE_STATUS_CHOICES = Choices(
    ('Draft', 'Draft'),
    ('Published', 'Published')
)

PREFERRED_LANGUAGE_EMPTY_LIST_MESSAGE = 'There are no articles for your preferred language! Please add a filter for ' \
                                        'another language to possibly view other articles.'

EMPTY_LIST_MESSAGE = 'There are no articles! Please add/edit language filter to possibly view other articles.'
