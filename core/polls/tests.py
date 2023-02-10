from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from polls.models import Question, Choice

class PollsViewTests(TestCase):

    def setUp(self):
        # create a question with choices
        self.question = Question.objects.create(question_text='What is your favorite color?', pub_date=timezone.now())
        self.choice1 = Choice.objects.create(question=self.question, choice_text='Blue', votes=0)
        self.choice2 = Choice.objects.create(question=self.question, choice_text='Red', votes=0)

    def test_detail_view(self):
        response = self.client.get(reverse('polls:detail', args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['question'], self.question)

    def test_vote_view_with_valid_choice(self):
        choice_id = self.choice1.id
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': choice_id})
        self.assertRedirects(response, reverse('polls:results', args=(self.question.id,)))
        choice = Choice.objects.get(id=choice_id)
        self.assertEqual(choice.votes, 1)

    def test_vote_view_with_invalid_choice(self):
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': 9999})
        self.assertEqual(response.status_code, 200)
        

    def test_vote_view_with_nonexistent_question(self):
        response = self.client.post(reverse('polls:vote', args=(9999,)), {'choice': self.choice1.id})
        self.assertEqual(response.status_code, 404)

    def test_results_view(self):
        response = self.client.get(reverse('polls:results', args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['question'], self.question)
        
class PollsViewsTestCase(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question_text='What is your favorite food?',
            pub_date=timezone.now()
        )
        self.choice_1 = Choice.objects.create(
            question=self.question,
            choice_text='Pizza'
        )
        self.choice_2 = Choice.objects.create(
            question=self.question,
            choice_text='Hamburger'
        )
        self.choice_3 = Choice.objects.create(
            question=self.question,
            choice_text='Tacos'
        )
        
    def test_index_view(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.question, response.context['questions'])
        self.assertTemplateUsed(response, 'polls/index.html')

    def test_detail_view(self):
        response = self.client.get(reverse('polls:detail', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['question'], self.question)
        self.assertTemplateUsed(response, 'polls/detail.html')
        
    def test_vote_view(self):
        response = self.client.post(reverse('polls:vote', args=[self.question.id]), {'choice': self.choice_1.id})
        self.assertEqual(response.status_code, 302)
        
    def test_results_view(self):
        response = self.client.get(reverse('polls:results', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['question'], self.question)
        self.assertTemplateUsed(response, 'polls/results.html')
        
    def test_404_for_question_not_exist(self):
        response = self.client.get(reverse('polls:detail', args=[999]))
        self.assertEqual(response.status_code, 404)
   
    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('polls:index'))
        self.assertTemplateUsed(response, 'polls/index.html')

    def test_index_view_has_questions(self):
        Question.objects.create(question_text="What is your favorite color?", pub_date=timezone.now())
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "What is your favorite color?")

    
    def test_detail_view_uses_correct_template(self):
        question = Question.objects.create(question_text="What is your favorite color?", pub_date=timezone.now())
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertTemplateUsed(response, 'polls/detail.html')

    def test_detail_view_has_question(self):
        question = Question.objects.create(question_text="What is your favorite color?", pub_date=timezone.now())
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertContains(response, "What is your favorite color?")

    def test_vote_view_redirects_to_results(self):
        question = Question.objects.create(question_text="What is your favorite color?", pub_date=timezone.now())
        choice = Choice.objects.create(question=question, choice_text="Blue")
        response = self.client.post(reverse('polls:vote', args=(question.id,)), {'choice': choice.id})
        self.assertRedirects(response, reverse('polls:results', args=(question.id,)))
