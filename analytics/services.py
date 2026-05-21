import logging
from collections import defaultdict
from datetime import datetime

from django.db import transaction

from interviews.models import Interview, InterviewQuestion
from resumes.models import Resume
from ai_engine.services.groq_service import GroqService
from .models import AverageScore, InterviewStat, StrongTopic, WeakTopic

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Builds analytics and recommendation context for dashboard insights."""

    TOPIC_KEYWORDS = [
        ('System design', ['design', 'architecture', 'system', 'scalability', 'microservices']),
        ('Debugging', ['debug', 'troubleshoot', 'bug', 'issue', 'fix']),
        ('Algorithms', ['algorithm', 'data structure', 'complexity', 'sorting', 'search']),
        ('Communication', ['communicate', 'stakeholder', 'explain', 'presentation', 'clarity']),
        ('Leadership', ['leadership', 'mentor', 'guide', 'coordinate', 'ownership']),
        ('Behavioral', ['team', 'culture', 'challenge', 'feedback', 'adaptability']),
        ('Testing', ['test', 'coverage', 'unit test', 'integration', 'quality']),
        ('Problem solving', ['problem', 'solve', 'approach', 'strategy', 'trade-off']),
        ('Interview readiness', ['interview', 'preparation', 'confidence', 'practice']),
    ]

    def __init__(self, user):
        self.user = user
        try:
            self.groq = GroqService()
        except Exception as exc:
            self.groq = None
            logger.warning(f'GroqService unavailable for analytics: {exc}')

    def refresh_user_analytics(self) -> dict:
        interviews = Interview.objects.filter(user=self.user).order_by('created_at')

        topic_summary = self._score_topics(interviews)
        weak_topics, strong_topics = self._rank_topics(topic_summary)
        trend_summary = self._build_trend_summary(interviews)
        improvement_areas = self._build_improvement_areas(weak_topics)
        recommendations = self._build_recommendations(
            interviews,
            weak_topics,
            strong_topics,
            improvement_areas,
            trend_summary,
        )

        analytics_payload = {
            'weak_topics': weak_topics,
            'strong_topics': strong_topics,
            'recommendations': recommendations,
            'improvement_areas': improvement_areas,
            'trend_summary': trend_summary,
        }

        self._persist_analytics(interviews, analytics_payload)

        return analytics_payload

    def _score_topics(self, interviews):
        topic_data = defaultdict(lambda: {'scores': [], 'count': 0, 'weak_count': 0})
        for interview in interviews:
            for question in interview.questions.all():
                topic = self._infer_topic(question.question)
                if not topic:
                    topic = 'General interview skills'

                score = question.score or 0
                topic_record = topic_data[topic]
                topic_record['scores'].append(score)
                topic_record['count'] += 1
                if score < 70:
                    topic_record['weak_count'] += 1

        scored_topics = []
        for topic, data in topic_data.items():
            average = round(sum(data['scores']) / len(data['scores'])) if data['scores'] else 0
            scored_topics.append({
                'topic': topic,
                'average_score': average,
                'question_count': data['count'],
                'weak_count': data['weak_count'],
            })

        return scored_topics

    def _rank_topics(self, scored_topics):
        weak_sorted = sorted(
            [topic for topic in scored_topics if topic['average_score'] < 80],
            key=lambda item: (item['average_score'], -item['weak_count']),
        )
        strong_sorted = sorted(
            [topic for topic in scored_topics if topic['average_score'] >= 80],
            key=lambda item: (-item['average_score'], -item['question_count']),
        )

        return weak_sorted[:4], strong_sorted[:4]

    def _build_trend_summary(self, interviews):
        scores = [interview.overall_score for interview in interviews if interview.overall_score is not None]
        if len(scores) < 2:
            return 'Collect more interview sessions to reveal score trends.'

        recent = scores[-3:]
        if recent[-1] >= recent[0]:
            direction = 'upward'
        else:
            direction = 'downward'

        return (
            f'Your latest interview trend is {direction}. '
            f'Latest score: {recent[-1]}%. '
            f'Average of last {len(recent)} sessions: {round(sum(recent)/len(recent))}%.'
        )

    def _build_improvement_areas(self, weak_topics):
        areas = []
        for topic in weak_topics:
            if topic['weak_count'] > 1:
                areas.append(
                    f"Repeat practice on '{topic['topic']}' using targeted exercises and review fundamentals."
                )
            else:
                areas.append(
                    f"Strengthen your knowledge in '{topic['topic']}' with short, focused study sessions."
                )
        return areas[:4]

    def _build_recommendations(self, interviews, weak_topics, strong_topics, improvement_areas, trend_summary):
        summary = self._build_recommendation_summary(interviews, weak_topics, strong_topics, trend_summary)
        if not self.groq:
            return [
                'Prioritize weak topics from recent interview sessions.',
                'Pair technical practice with communication and behavioral preparation.',
                'Review your latest resume and align it with your strongest interview topics.',
            ]

        try:
            result = self.groq.generate_analytics_recommendations(summary)
            return result.get('recommended_topics', []) + result.get('practice_suggestions', []) + result.get('improvement_roadmap', [])
        except Exception as exc:
            logger.warning(f'AI recommendations unavailable: {exc}')
            fallback = [
                'Prioritize weak topics from recent interview sessions.',
                'Pair technical practice with communication and behavioral preparation.',
                'Review your latest resume and align it with your strongest interview topics.',
            ]
            return fallback

    def _build_recommendation_summary(self, interviews, weak_topics, strong_topics, trend_summary):
        latest_resume = Resume.objects.filter(user=self.user).order_by('-created_at').first()
        resume_note = ''
        if latest_resume and getattr(latest_resume, 'ats_score', None) is not None:
            resume_note = f"Latest resume ATS score: {latest_resume.ats_score}%. "

        weak_titles = ', '.join(topic['topic'] for topic in weak_topics[:3]) or 'none yet'
        strong_titles = ', '.join(topic['topic'] for topic in strong_topics[:3]) or 'none yet'
        interview_count = interviews.count()

        return (
            f"User has completed {interview_count} interview sessions. "
            f"Weak topics include: {weak_titles}. "
            f"Strong topics include: {strong_titles}. "
            f"{trend_summary} {resume_note}"
        )

    def _infer_topic(self, text):
        text_lower = text.lower()
        for topic_name, keywords in self.TOPIC_KEYWORDS:
            if any(keyword in text_lower for keyword in keywords):
                return topic_name
        return 'General interview skills'

    @transaction.atomic
    def _persist_analytics(self, interviews, analytics_payload):
        total_interviews = interviews.count()
        average_score = round(sum(i.overall_score for i in interviews) / total_interviews) if total_interviews else 0

        AverageScore.objects.update_or_create(
            user=self.user,
            defaults={
                'average_score': average_score,
                'interview_count': total_interviews,
                'updated_at': datetime.utcnow(),
            },
        )

        InterviewStat.objects.update_or_create(
            user=self.user,
            defaults={
                'total_interviews': total_interviews,
                'average_score': average_score,
                'weak_topics': analytics_payload['weak_topics'],
                'strong_topics': analytics_payload['strong_topics'],
                'improvement_areas': analytics_payload['improvement_areas'],
                'trend_summary': analytics_payload['trend_summary'],
                'recommendations': '\n'.join(analytics_payload['recommendations']),
                'updated_at': datetime.now(),
            },
        )

        WeakTopic.objects.filter(user=self.user).delete()
        StrongTopic.objects.filter(user=self.user).delete()

        for topic in analytics_payload['weak_topics']:
            WeakTopic.objects.create(
                user=self.user,
                topic=topic['topic'],
                severity=topic['average_score'],
                notes=f"Appears in {topic['question_count']} question(s).",
            )

        for topic in analytics_payload['strong_topics']:
            StrongTopic.objects.create(
                user=self.user,
                topic=topic['topic'],
                confidence=topic['average_score'],
                notes=f"Consistently strong across {topic['question_count']} question(s).",
            )
