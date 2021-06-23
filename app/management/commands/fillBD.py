import random

from django.core.management.base import BaseCommand
from app.models import User, Tag, Like, Question, Answer
from faker import Faker


class Command(BaseCommand):
    faker = Faker()

    def add_arguments(self, parser):
        parser.add_argument('--users')
        parser.add_argument('--tags')
        parser.add_argument('--question')
        parser.add_argument('--answer')
        parser.add_argument('--likesQ')
        parser.add_argument('--likesA')

    def fill_users(self, count):
        users = []
        for i in range(count):
            users.append(User(username=self.faker.user_name() + str(i)))
        User.objects.bulk_create(users, count)

    def fill_tags(self, count):
        tags = []
        for i in range(count):
            tags.append(Tag(name=self.faker.word() + str(i)))
        Tag.objects.bulk_create(tags, count)

    def fill_question(self, count):
        question = []
        all_users_id = list(
            User.objects.values_list(
                'id', flat=True
            )
        )

        for i in range(count):
            question.append(Question(author=User.objects.all().get(id=random.choice(all_users_id)),
                                     title=self.faker.sentence()[:30], text=self.faker.paragraph(nb_sentences=5),
                                     rating=random.randint(0, 1000)))
        Question.objects.bulk_create(question, count)

        question = Question.objects.all()
        all_tags = Tag.objects.all()
        for q in question:
            for i in range(random.randint(1, 3)):
                q.tags.add(random.choice(all_tags))

    def fill_answer(self, count):
        all_user_id = list(
            User.objects.values_list(
                'id', flat=True
            )
        )

        all_question_id = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        answer = []
        for i in range(count):
            answer.append(Answer(author=User.objects.all().get(id=random.choice(all_user_id)),
                                 what_question=Question.objects.all().get(id=random.choice(all_question_id)),
                                 text=self.faker.paragraph(nb_sentences=3),
                                 rating=random.randint(0, 1000)))
        Answer.objects.bulk_create(answer, count)

    def fill_like_question(self, count):
        all_user_id = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        all_question_id = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )

        likes = []
        for i in range(count):
            likes.append(Like(author=User.objects.all().get(id=random.choice(all_user_id)),
                              status=True, content_object=Question.objects.get(id=random.choice(all_question_id))))
        Like.objects.bulk_create(likes, count)

    def fill_like_answer(self, count):
        all_user_id = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        all_answer_id = list(
            Answer.objects.values_list(
                'id', flat=True
            )
        )
        likes = []
        for i in range(count):
            likes.append(Like(author=User.objects.all().get(id=random.choice(all_user_id)),
                              status=True, content_object=Answer.objects.get(id=random.choice(all_answer_id))))
        Like.objects.bulk_create(likes, count)

    def handle(self, *args, **options):
        if options['users']:
            self.fill_users(1000)
        if options['tags']:
            self.fill_tags(1000)
        if options['question']:
            self.fill_question(1000)
        if options['answer']:
            self.fill_answer(1000)
        if options['likesQ']:
            self.fill_like_question(1000)
        if options['likesA']:
            self.fill_like_answer(1000)
